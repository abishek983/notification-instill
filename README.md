# notification-instill

Steps to run the application:- 

0. Make sure docker is installed & running in your system
1. Run docker compose up --build to build and run the application.
2. Go to http://localhost:8000/ 
3. You will get your unique user id which will be used to send message to the user.
4. Copy the user id and head over to http://localhost:8000/docs#/default/send_notification_send_notification__post
5. Send the message to the user using the send_notification post api call.
 Sample Send notification api request 

 ```
 {
  "user": "1693227828308",
  "title": "expiring soon",
  "description": "tester hello I ma",
  "identifier": "whatsapp"
}
 ```


 6. Go back to the http://localhost:8000/ you have opened in Step 2.
 7. You will be able to the see the message send from the post API call. 
