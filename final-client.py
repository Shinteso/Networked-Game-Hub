from rps import play_rps
from tic_tac_toe import play_ttt
import socket
import threading
 
username = input('Choose your name: ')
 
host, port = '127.0.0.1', 3000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
game_to_play = None # tracks game that as picked



def receive():
    global game_to_play
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if message == 'USERNAME':
                client.send(username.encode('ascii'))

            elif message == 'GAME_START:rps':
                print('\n--- Both players are ready! Launching Rock Paper Scissors... ---')
                game_to_play = 'rps'
                in_game.set()
                break

            elif message == 'GAME_START:ttt':
                print('\n--- Both players are ready! Launching Tic Tac Toe... ---')
                game_to_play = 'ttt'
                in_game.set()
                break

            else:
                print(message)

        except:
            client.close()
            break

in_game = threading.Event()

def write():
    while True:
        text = input('')
        if in_game.is_set():
            break
        message = f'{username}: {text}'
        client.send(message.encode('ascii'))

        # Stop write loop locally when a player says quit
        if text.strip().lower() == 'quit':
            print('Disconnecting...')
            client.close()
            break

while True:
    in_game.clear()
    game_to_play = None
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write()

    # wait for receve thead
    receive_thread.join()

    # Main thread now owns socket so do rps
    if game_to_play == 'rps':
        play_rps(client)
    elif game_to_play == 'ttt':
        play_ttt(client)
    elif game_to_play is None:
        # receive thread exited without a game — disconnected or quit
        break

    print('\n--- Game over! Returning to lobby... ---\n')

print('Goodbye!')
 
