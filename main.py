from fastapi import FastAPI, WebSocket, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import models
import schemas
from models import Notification
from database import SessionLocal, engine
from notification import notification, notificationSystem
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            function getQueryParam(name) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
            }
            var client_id = Date.now();
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

app = FastAPI()

class NotificationCreate(BaseModel):
    user: str
    title: str
    description: str
    identifier: str = None

# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
websocket_connections = {}

@app.get("/")
async def get():
    return HTMLResponse(html)



@app.post("/notifications/", response_model=schemas.Notification)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification


@app.post("/send-notification/")
async def send_notification(notification_request: NotificationCreate):
    notification_obj = notification.notification_factory.create_notification(
        title=notification_request.title,
        description=notification_request.description,
        identifier=notification_request.identifier
    )

    user=notification_request.user
    notification_system = notificationSystem.NotificationSystem()
    notification_system.add_user(notification_request.user)
    notification_system.send_notification(get_db(), notification_obj)
    print(websocket_connections)
    websocket = websocket_connections.get(user)
    print(websocket)
    if websocket is not None:
        await websocket.send_text(f"Server to Client {user}: {notification_obj.description}")
        return {"message": "Message sent"}
    else:
        return {"message": f"Client {user} not found"}
    


@app.get("/notifications/")
def get_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Notification).offset(skip).limit(limit).all()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    websocket_connections[str(client_id)] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        del websocket_connections[str(client_id)]
        await manager.broadcast(f"Client #{client_id} left the chat")