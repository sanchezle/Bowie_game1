# Bowie-game
#### Video Demo:  <URL HERE>
#### Description:BOWIE GAME
 
My final project is a game about a wire haired sausages dog popping bubbles, and hitting pigeons in Ciutadella Park in Barcelona, I got inspiration from all the days that I walked my dog in that beautiful park, during those moments I felt so alive and happy to share with him that space and time that now that he is living in another country with my mother I can remember him vividly, those moments at the park where my break from all sort of troubles that daily live can put you into.
 
 The game dynamic is simple and broadly used for simple video games in general and for mobile games, the user has to make the dog jump to pop the bubbles or hit the pigeons that fly three times during the span of the game that lasts 60 seconds, each bubble popped counts for 2 points in the score count, and each pigeon hit counts a total of 40 points. De idea is to get the higher score possible. 
The users have two different ways of moving the dog depending on the device type. If the user is using a desktop the dog can be moved with the arrow key to the left or to the right, and the down arrow key to stop the dog from moving, and the jump movement is triggered by the space bar key. On the other hand, if the user is using a mobile phone the user can use four arrow buttons that appear at the bottom right corner of the screen, each bottom describes its purpose. At the top of the screen, the game has a time display,  a score display, and a mute button that mutes the sound of the game which is the background music, I chose to use the background music of angry birds since I enjoyed that video game a lot, the bubble pop sound, and the bark sound which is the sound of my actual dog barking.
 
As for the aesthetic, I chose an actual picture of my dog cropped and an actual picture of the fountain in Ciutadella Park, located in Barcelona. I decided to use bubbles because there are often street artists that perform in front of the fountain creating bubbles for people to see and pop them.
 
The program does not only perform the video game dynamic but also has a register and database system that is actually working and live, hosted in pythonanywhere.com  the database keeps track of username, passwords and scores. Tracking users and scores data allows the program to display all-time records and the higher scores of the user, such data is displayed on different pages, the index page displays the last score of the user, and the five higher scores the user has achieved. Meanwhile, on the records page, the all-time ten higher scores of all users are displayed while displaying also the top five scores of the user.   
 
The program initially takes you to a login page, which allows you to get the register page from there as well, the user can register easily and quickly just by providing a username and password and password confirmation. The user clicks the register button and the database is updated with the new user data.
 
The program renders an apology message as well when the user has not met the requirements for registration, and login.
 
Apart from the files generated for Flask and for the virtual environment and the media files, The whole program consists of sixteen files, distribute in three directories,  the main folder, and two other directories, static and templates. In the main directory, it has 2 Python files, app.py and helpers.py, and the database file bowie-game.db.  In the static directory apart from pictures (sixteen pictures) and sounds (three sounds files),  there is one javascript file script.js, four CSS files, instructions.css,  style.css, styles_game.css, styles2.css.  In the templates directory, there are nine html files, apology.html, bowie_game.html, index.html, instructions.html, layout.html, login.html, records.html, register.html, and success.html.
 
 
Description of files.
 
App.py:
 
This is the most important file since is where the web application is programmed. The file has several routes that connect the database with the javascript file and the HTML file allowing users to register, log in, and store their data.
 
The file starts importing several tools provided in CS50 lectures such as OS, CS50 ibrary, SQL from CS50 library, session from flask_session, mkdtemp from tempfile, check_password_hash, generate_password_hash from werkseug.security, apology from helpers, flask_socketio , and datetime from datetime.
 
It defines bowiegame.db as a database and connects initiates the flask app and connects it to the database,  then the “/login” route is defined, checking password and username. The “/logout” route clears the session and takes the user to “/”.
 
Then the route “/register” is defined, and takes the user“register.html” where the user fills a form and submits it. Once the user submitted the form updates the database and sends the user to success.html where the user gets a message “you have registered successfully”.
 
 In the game route “/game” the route takes the user to bowie_game.html and at the end of the game updates the score table and takes the user and executes index function that takes the user to index.html.
The route “/” takes the user to index and displays the last score of the user and the  5 higher scores of the user.
The route records “/record “ takes the user to records.html where the route displays 10 higher scores of all users and the user 5 higher scores.
 
The route” /instruction” takes you to instructions.html where the instructions are displayed in an unordered list.
 
There are several other routes that are still in the production process.
 
Helpers.py:
 
Helpers.py contains an apology function that renders an apology message when the user makes a mistake while registering or while login. also, if some of the pages are failing apology function is used.
The program contains also the loging_requires function which blocks unauthorized access to users that have not login.
 
 
 
DATA BASE:
 
Bowiegame.db:
 
The database was built using SQLite, and it is quite simple,  the database consists of only two tables users tables that stores id, username, and password hash. And the other table scores, stores id, user_id as a foreign key, score, and timestamp.
 
 
GAME PROGRAM:
 
Script.js:
 
It contains the whole dynamic of the game, the update timer function that starts the countdown and when the variable time reaches 0 calls the function times up that sends the sends score data to flask.
 
The update score function is in charge of updating the score every time the user pops a bubble or hits one of the pigeons.
 
It also contains the Jump function, the slideleft function, slideright function, and stop function, which controls the movements of the dog.
 
The create bubble function creates a number of bubbles with random sizes and at random heights taking colors values from a list of five different bubbles created in styles_game.css file. Inside is the animatebubble function that moves at random speeds and random heights the bubbles then it is the collisionwithdog function that sets the conditions for when the dog collides with the bubbles.
 
It also contains the animatesprite function that animates the pigeons, inside this function are flightanimationscheldule, function frameChange, functionflightanimation, and collitionwithdog, that set the movement for the pigeons, the height, the speed and the time when the pigeons appear.
 


TODO