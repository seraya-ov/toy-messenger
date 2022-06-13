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

* `/register`: register a new user with given login
* `/send_message`: send a text message 
* `/fetch_new_messages`: fetch new messages
* `/fetch_messages`: fetch all messages
* `/delete_message`: delete one message
* `/delete_messages`: delete multiple messages


## How to run:
`docker-compose up --build`
Now you can access the project running on http://127.0.0.1:5000/
