from rpc import pack_result, pack_procedure, unpack_result, unpack_procedure, send_msg, recv_msg

def board_to_string(game_board):
    """Convert board to a string to send over the network."""
    return (
        f'\n-------------\n'
        f'| {game_board[0]} | {game_board[1]} | {game_board[2]} |\n'
        f'|---|---|---|\n'
        f'| {game_board[3]} | {game_board[4]} | {game_board[5]} |\n'
        f'|---|---|---|\n'
        f'| {game_board[6]} | {game_board[7]} | {game_board[8]} |\n'
        f'-------------\n'
    )

def verify_win(game_board):
    r = ''.join(game_board)
    
    lines = [
        r[0:3], r[3:6], r[6:9],             # horizontals
        r[0]+r[3]+r[6],                     # verticals
        r[1]+r[4]+r[7],
        r[2]+r[5]+r[8],
        r[0]+r[4]+r[8],                     # diagonals
        r[2]+r[4]+r[6],
    ]

    for line in lines:
        if line == 'XXX' or line == 'OOO':
            return True
        

    for item in game_board:
        if item not in ['X', 'O']: # Verify if each field was filled            
            # If it finds an Empty field it returns False so the game can continue
            return False
    
    # If it run all verifications and all positions are filled return Tie
    return 'Tie'
  

# Server Game Loop
def start_ttt(client1, client2, player1, player2):
    """ Server: Run a game of tic tac toe between clients"""
    game_board = ['1','2','3','4','5','6','7','8','9']

    # assign X to client1, O to client2
    markers = {client1: 'X', client2: 'O'}
    player_names = {client1: player1, client2: player2}

    # Tell each player their letter
    send_msg(client1, pack_result(f'You are X. You go first!\n'))
    send_msg(client2, pack_result(f'You are O. Waiting for {player1} to move...\n'))

    current, other = client1, client2

    try:
        while True:
            # send board to both players
            board_str = board_to_string(game_board)
            send_msg(client1, pack_result(board_str))
            send_msg(client2, pack_result(board_str))

            # prompt current player
            send_msg(current, pack_result(f'Your Turn ({markers[current]}). Pick a position (1-9): '))
            send_msg(other, pack_result(f'Waiting for {player_names[current]} to move...\n'))

            # receive move from current player -> validate in a loop
            while True:
                _, args = unpack_procedure(recv_msg(current))
                position = args[0].strip()

                if not position.isdigit() or position not in [str(i) for i in range(1, 10)]:
                    send_msg(current, pack_result('Position taken. Pick another (1-9): '))
                    continue

                break # on valid move

            # apply move
            game_board[int(position) - 1] = markers[current]
            print(f'TTT: {player_names[current]} played {position}')
            
            # check result
            result = verify_win(game_board)
            board_str = board_to_string(game_board)

            if result == 'Tie':
                send_msg(client1, pack_result(board_str + "It's a tie! No winners.\n"))
                send_msg(client2, pack_result(board_str + "It's a tie! No winners.\n"))
                print('TTT: Tie game')
                break
            
            elif result == True:
                winner_name = player_names[current]
                send_msg(current, pack_result(board_str + f'You win!\n'))
                send_msg(other, pack_result(board_str + f'{winner_name} wins! You lose.\n'))
                print(f'TTT: {winner_name} wins!')
                break

            # swap turns
            current, other = other, current

    except Exception as e:
        print(f'TTT error: {e}')


def play_ttt(client):
    """ Client Game Loop """
    try:
        while True:
            message = unpack_result(recv_msg(client))
            print(message)

            # if it's clients turn, send a move
            if 'Your turn' in message or 'Pick a position' in message or 'Pick another' in message or 'Invalid' in message:
                move = input('> ')
                send_msg(client, pack_procedure('make_move', move))

            # game over cond
            if 'win' in message.lower() or 'lose' in message.lower() or 'tie' in message.lower():
                break
    
    except Exception as e:
        print(f'TTT error: {e}')


if __name__ == '__main__':
    import random
    game_board = ['1','2','3','4','5','6','7','8','9']
    player_turn = random.randint(1, 2)
    markers = {1: 'X', 2: 'O'}
 
    print('Welcome to Tic Tac Toe!')
    print(board_to_string(game_board))
 
    while True:
        position = input(f'Player {player_turn} ({markers[player_turn]}), pick a position (1-9): ')
        if not position.isdigit() or position not in [str(i) for i in range(1, 10)]:
            print('Invalid position.')
            continue
        if game_board[int(position) - 1] in ['X', 'O']:
            print('Position taken.')
            continue
 
        game_board[int(position) - 1] = markers[player_turn]
        print(board_to_string(game_board))
 
        result = verify_win(game_board)
        if result == 'Tie':
            print("It's a tie!")
            break
        elif result == True:
            print(f'Player {player_turn} wins!')
            break
 
        player_turn = 2 if player_turn == 1 else 1
