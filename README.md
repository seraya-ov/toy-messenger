# toy-messenger
TriOptima test assignment

## Requirements:

Build	a	service	for	sending	and	retrieving	messages.	The	service	should	support	
the	following	functions.
* 1. Submit	a	message	to	a	defined	recipient, identified	with	some	identifier,	
e.g.	email-address,	phone-number,	user	name	or	similar.
* 2. Fetch new messages (meaning	the	service	must know	what	has	already	
been	fetched).
* 3. Delete	a	single	message.
* 4. Delete	multiple messages.
* 5. Fetch messages (including	previously	fetched) ordered	by time,	according	to start	and	stop index. 
The	service	must	be	implemented	in	the	form	of a	REST-API

## API:

* `/register`: (POST) register a new user with given login 

    JSON request:
    ```
    {
        "login": string, between 3 and 128 symbols
    }
    ```
    JSON response (201):
    ```
      {
          "OK": "created user with login {login}"
      }
    ```
* `/send_message`: (POST) send a text message 

    JSON request:
    ```
    {
        "sender": sender login
        "recipient": recipient login
        "message": message
    }
    ```
    JSON response (201):
    ```
      {
          "OK": "message sent successfully"
      }
    ```
* `/fetch_new_messages`: (PUT) fetch new messages 

    JSON request:
    ```
        {
            "sender": sender login
            "recipient": recipient login
        }
    ```
    JSON response (200):
    ```
      {
            "messages": [
                {
                    "sender": sender login
                    "recipient": recipient login
                    "timestamp": timestamp
                    "message": message text
                }
            ]
        }
    ```
* `/fetch_messages`: (PUT) fetch all messages

    JSON request:
    ```
      {
            "sender": sender login
            "recipient": recipient login
            "period_start": period start timestamp
            "period_end": period end timestamp
      }
    ```
    JSON response (200):
    ```
      {
            "messages": [
                {
                    "sender": sender login
                    "recipient": recipient login
                    "timestamp": timestamp
                    "message": message text
                }
            ]
        }
    ```
* `/delete_message`: (DELETE) delete one message

    JSON request:
    ```
      {
          "sender": sender login
          "recipient": recipient login
          "timestamp": message timestamp
      }
    ```
    JSON response (201):
    ```
      {
          "OK": "message deleted"
      }
    ```
* `/delete_messages`: (DELETE) delete multiple messages

    JSON request:
    ```
    {
        "sender": sender login
        "recipient": recipient login
        "timestamps": [message timestamps]
    }
    ```
    JSON response (201):
    ```
      {
          "OK": "message deleted"
      }
    ```


## How to run:
`docker-compose up --build`
Now you can access the project running on http://127.0.0.1:5000/
