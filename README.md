# Networked-Game-Hub
This is my final project for my Networking class in my junior year of college.


# Setup
- The only setup is to make sure all the files are in the same root directory.

- Once they are all there you can first run the final-server.py

- After running the server up to five people can connect to it using the client.

# Features
This project features a minal ui chat hub/lobby and offers two games to play, those games being rock paper scissors and tic tac toe.

While in the lobby you can also dm other player by using </dm> <player_name> <msg>

There is also a "queuing" feature in the for of typing ready will put you in a ready state for what ever game you chose until two ppl are ready you can also unready by typing unready.

The code using an rpc-tcp connection and maniulates function through a transport layer and package and unpackage the data using pickle.

# Future things to add
The few things I wanted to but did not get to are making a single player mode which puts you up against an ai and also figure out how to set this up on a server.

T