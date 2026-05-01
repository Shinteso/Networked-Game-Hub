import socket
import threading
from rps import start_rps
from tic_tac_toe import start_ttt
import os


port = 3000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', port))
server.listen(5)

# Lists 
clients = [] # Players
names = [] # usernames
game_choice = [] # ttt, rps, or None

# ready list per game (players who are ready)
ready_TTT = []
ready_RPS = []

# Clients currently in a game
in_game_clients = set()


# ready lists
def broadcast(message):
    for client in clients:
        client.send(message.encode('ascii'))

def send_private(client, message):
    """Send message to one client only."""
    client.send(message.encode('ascii'))

def return_to_lobby(client1, client2):
    """ Reset state for both clients send back to lobby"""
    for client in [client1, client2]:
        if client not in clients:
            continue
        index = clients.index(client)
        # reset game state
        game_choice[index] = None
        if client in ready_RPS:
            ready_RPS.remove(client)
        if client in ready_TTT:
            ready_TTT.remove(client)
        in_game_clients.discard(client)
        # welcome back message
        send_private(client, '\nYou are back in the lobby!\nType "rps" to play Rock Paper Scissors or "ttt" to play Tic Tac Toe.\n')
        # start new handle thread
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
    print(f'Players returned to lobby | Choices: {list(zip(names, game_choice))}')


def check_ready():
    """Run GAME_START if exactly 2 players are both ready"""
    if len(ready_RPS) == 2:
        broadcast('GAME_START:rps')
        print('Launching Rock Paper Scissors')
        c1, c2 = ready_RPS[0], ready_RPS[1]

        in_game_clients.add(c1)
        in_game_clients.add(c2)

        c1.settimeout(None)
        c2.settimeout(None)

        p1 = names[clients.index(c1)]
        p2 = names[clients.index(c2)]
        
        def rps_then_lobby():
            start_rps(c1, c2, p1, p2)
            return_to_lobby(c1, c2)
        threading.Thread(target=rps_then_lobby, daemon=True).start()
        
    
    elif len(ready_TTT) == 2:
        broadcast('GAME_START:ttt')
        print('Launching Tic Tac Toe!')
        c1, c2 = ready_TTT[0], ready_TTT[1]

        in_game_clients.add(c1)
        in_game_clients.add(c2)

        c1.settimeout(None)
        c2.settimeout(None)

        p1 = names[clients.index(c1)]
        p2 = names[clients.index(c2)]
        
        def ttt_then_lobby():
            start_ttt(c1, c2, p1, p2)
            return_to_lobby(c1, c2)
        threading.Thread(target=ttt_then_lobby, daemon=True).start()

def handle(client):
    client.settimeout(0.5)
    while True:
        # stop lobby handler if client in game
        if client in in_game_clients:
            break

        try:
            message = client.recv(1024).decode('ascii')
            index = clients.index(client)
            name = names[index]
            text = message.split(': ', 1)[-1].strip().lower()
            
            if text == 'rps':
                game_choice[index] = 'rps'
                send_private(client, 'You picked Rock Paper Scissors! Type "ready" when ready to play.\n')
                print(f'{name} picked rps | Choices: {list(zip(names, game_choice))}')
            
            elif text == 'ttt':
                game_choice[index] = 'ttt'
                send_private(client, 'You picked Tic Tac Toe! Type "ready" when ready to play.\n')
                print(f'{name} picked ttt | Choices: {list(zip(names, game_choice))}')

            elif text == 'ready':
                if game_choice[index] is None:
                    send_private(client, 'You must pick a game first! Type "rps" for Rock Paper Scissors or "ttt" for Tic Tac Toe. \n')
                else:
                    if game_choice[index] == 'rps':
                        ready_RPS.append(client)
                    else:
                        ready_TTT.append(client)
                broadcast(f'[{name} is ready!]')
                print(f'Ready rps: {[names[clients.index(c)] for c in ready_RPS]}')
                print(f'Ready ttt: {[names[clients.index(c)] for c in ready_TTT]}')
                check_ready()

            elif text.startswith('/dm '):
                parts = message.split(': ', 1)[-1].split(' ', 2) # ['\dm', 'target_name', 'msg']
                if len(parts) < 3:
                    send_private(client, 'Usage: /dm <name> <message>\n')
                else:
                    _, target_name, dm_msg = parts
                    if target_name in names:
                        target_client = clients[names.index(target_name)]
                        send_private(target_client, f'[DM from {name}]: {dm_msg}\n')
                        send_private(client, f'[DM to {target_name}]: {dm_msg}\n')
                    else:
                        send_private(client, f'Player "{target_name}" not found.\n')
            
            
            else:
                broadcast(message)

        except socket.timeout:
            continue

        except:
            index = clients.index(client)
            name = names[index]
            # clean up all lists
            if client in ready_RPS:
                ready_RPS.remove(client)
            if client in ready_TTT:
                ready_TTT.remove(client)
            in_game_clients.discard(client)
            clients.remove(client)
            names.remove(name)
            game_choice.pop(index)
            client.close()
            broadcast(f'{name} has left')
            print(f'Choices: {list(zip(names, game_choice))}')
            if len(clients) == 0:
                print('No players connected. Shutting down server...')
                server.close()
                os._exit(0)

            break


def receive():
    print(f'Server listening on port {port}...')
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        # request username
        client.send('USERNAME'.encode('ascii'))
        username = client.recv(1024).decode('ascii')

        clients.append(client)
        names.append(username)
        game_choice.append(None)

        print(f'{username} has joined | Choices: {list(zip(names, game_choice))}')
        broadcast(f'{username} has joined')
        client.send('Welcome to the lobby!  Here you can chat freely with other players. \nType "rps" to play Rock Paper Scissors or "ttt" to play Tic Tac Toe.\n'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()