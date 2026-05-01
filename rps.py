from rpc import pack_result, pack_procedure, unpack_result, unpack_procedure, send_msg, recv_msg
 
choices = ['rock', 'paper', 'scissors']

def determine_winner(p1_choice, p2_choice, name1, name2):
    """Compare choices and return a result string for each player."""
    if p1_choice == p2_choice:
        return "It's a tie!", "It's a tie!"
 
    p1_wins = (
        (p1_choice == 'rock'     and p2_choice == 'scissors') or
        (p1_choice == 'scissors' and p2_choice == 'paper')    or
        (p1_choice == 'paper'    and p2_choice == 'rock')
    )
 
    summary = f'\n--- Results ---\n{name1} chose: {p1_choice}\n{name2} chose: {p2_choice}\n'
    if p1_wins:
        return summary + 'You win!', summary + 'You lose!'
    else:
        return summary + 'You lose!', summary + 'You win!'

# RPS Server Game Loop
def start_rps(client1, client2, player1, player2):
    try:
        # Ask players for their choice
        send_msg(client1, pack_result('RPS: Enter rock, paper, or scissors: '))
        send_msg(client2, pack_result('RPS: Enter rock, paper, or scissors: '))


        # Receive choices from clients
        _, args1 = unpack_procedure(recv_msg(client1))
        _, args2 = unpack_procedure(recv_msg(client2))

        choice1 = args1[0].lower()
        choice2 = args2[0].lower()

        # Validate
        if choice1 not in choices or choice2 not in choices:
            send_msg(client1, pack_result('Game Over: Invaild choice made.'))
            send_msg(client2, pack_result('Game Over: Invaild choice made.'))

        # Determine winner
        result1, result2 = determine_winner(choice1, choice2, player1, player2)
        send_msg(client1, pack_result(result1))
        send_msg(client2, pack_result(result2))
        print(f'RPS: {player1}={choice1}, {player2}={choice2}')
        
    except Exception as e:
        print(f'RPS error: {e}')

# RPS Client Game Loop
def play_rps(client):
    # Server sends a prompt unpack and display it
    prompt = unpack_result(recv_msg(client))
    choice = input(prompt)

    # pack choice and send back to server
    send_msg(client, pack_procedure('submit_choice', choice))

    # waiting for result
    result = unpack_result(recv_msg(client))
    print(result)
