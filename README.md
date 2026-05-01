# Networked-Game-Hub
This is my final project for my Networking class in my junior year of college.


# Setup
- The only setup is to make sure all the files are in the same root directory.

- Once they are all there you can first run the final-server.py

- After running the server up to five people can connect to it using the client.

- For Running the project run these files
```bash
py final-server.py
py final-client.py
```

# Features
This project features a minal ui chat hub/lobby and offers two games to play, those games being rock paper scissors and tic tac toe.



While in the lobby you can also dm other player by using </dm> <player_name> <msg>

There is also a "queuing" feature in the for of typing ready will put you in a ready state for what ever game you chose until two ppl are ready you can also unready by typing unready.

## Lobby Commands
```
rps          # pick Rock Paper Scissors
ttt          # pick Tic Tac Toe
ready        # ready up
unready      # cancel ready
/dm <name> <message>   # private message
quit         # disconnect
```

The code using an rpc-tcp connection and maniulates function through a transport layer and package and unpackage the data using pickle.

## How RPC Works
```python
# client sends a move
send_msg(client, pack_procedure('make_move', 5))

# server receives and evaluates it
name, args = unpack_procedure(recv_msg(conn))
result = evaluate_procedure(name, args)
send_msg(conn, pack_result(result))
```

## How the lobby tracks game choices
```python
clients = []      # connection objects
names = []        # usernames
game_choice = []  # 'rps', 'ttt', or None
ready_RPS = []    # clients ready for RPS (Rock Paper Scissors)
ready_TTT = []    # clients ready for TTT (Tic Tac Toe)
```

# Future things to add
The few things I wanted to but did not get to are making a single player mode which puts you up against an ai and also figure out how to set this up on a server.