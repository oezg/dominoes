import random
import itertools
DOMINO = 7


def display():
    print("="*70)
    print("Stock size:", len(stock))
    print("Computer pieces:", len(computer_pieces))
    print()
    print(make_snake_string())
    print()
    print("Your pieces:")
    for i, piece in enumerate(player_pieces):
        print("{0}:[{1}, {2}]".format(i+1, piece[0], piece[1]))
    print()


def make_snake_string():
    snake_string = ""
    if len(snake) > 6:
        for i in range(3):
            snake_string += repr(snake[i])
        snake_string += "..."
        for i in range(3, 0, -1):
            snake_string += repr(snake[-i])
    else:
        for piece in snake:
            snake_string += repr(piece)
    return snake_string


def update_status():
    global status
    if not computer_pieces:
        status = "computer_won"
    elif not player_pieces:
        status = "player_won"
    elif snake[0][0] == snake[-1][1]:
        occurrences = sum(piece.count(snake[0][0]) for piece in snake)
        if occurrences >= 8:
            status = "draw"


def count_appearances():
    counts = {}.fromkeys(range(DOMINO), 0)
    for piece in snake + computer_pieces:
        for side in piece:
            counts[side] += 1
    return counts



all_pieces = [list(t) for t in list(itertools.combinations_with_replacement(range(DOMINO), 2))]
random.shuffle(all_pieces)
stock = all_pieces[:2*DOMINO]
status_messages = { "computers_turn": "Status: Computer is about to make a move. Press Enter to continue...",
                    "players_turn": "Status: It's your turn to make a move. Enter your command.",
                    "player_won": "Status: The game is over. You won!",
                    "computer_won": "Status: The game is over. The computer won!",
                    "draw": "Status: The game is over. It's a draw!"}


if all([i, i] in stock for i in range(DOMINO)):
    stock = all_pieces[2*DOMINO:]
    computer_pieces = all_pieces[:DOMINO]
    player_pieces = all_pieces[DOMINO:2*DOMINO]
else:
    computer_pieces = all_pieces[2*DOMINO:3*DOMINO]
    player_pieces = all_pieces[3*DOMINO:]

for i in range(DOMINO - 1, -1, -1):
    if [i, i] in computer_pieces:
        computer_pieces.remove([i, i])
        snake = [[i, i]]
        status = "players_turn"
        break
    elif [i, i] in player_pieces:
        player_pieces.remove([i, i])
        snake = [[i, i]]
        status = "computers_turn"
        break

while True:
    display()
    update_status()
    message = status_messages[status]
    print(message)
    if status == "computers_turn":
        hand_size = len(computer_pieces)
        _ = input()
        counts = {}.fromkeys(range(DOMINO), 0)
        for piece in snake + computer_pieces:
            for side in piece:
                counts[side] += 1

        scores = {}.fromkeys(range(hand_size), 0)
        for ind, piece in enumerate(computer_pieces):
            for side in piece:
                scores[ind] += counts[side]
        while scores:
            max_score = max(scores, key=scores.get)
            if computer_pieces[max_score][0] == snake[0][0]:
                computer_pieces[max_score].reverse()
                snake.insert(0, computer_pieces.pop(max_score))
                break
            elif computer_pieces[max_score][1] == snake[0][0]:
                snake.insert(0, computer_pieces.pop(max_score))
                break
            elif computer_pieces[max_score][0] == snake[-1][1]:
                snake.append(computer_pieces.pop(max_score))
                break
            elif computer_pieces[max_score][1] == snake[-1][1]:
                computer_pieces[max_score].reverse()
                snake.append(computer_pieces.pop(max_score))
                break
            else:
                del scores[max_score]
        else:
            if stock:
                computer_pieces.append(stock.pop())
        status = "players_turn"
    elif status == "players_turn":
        hand_size = len(player_pieces)
        invalid = True
        while invalid:
            command = input()
            try:
                command = int(command)
            except ValueError:
                print("Invalid input. Please try again.")
            else:
                if command == 0:
                    invalid = False
                    if stock:
                        player_pieces.append(stock.pop())
                elif -hand_size <= command < 0:
                    if snake[0][0] in player_pieces[-command-1]:
                        invalid = False
                        if snake[0][0] == player_pieces[-command-1][0]:
                            player_pieces[-command-1].reverse()
                        snake.insert(0, player_pieces.pop(-command-1))
                    else:
                        print("Illegal move. Please try again.")
                elif 0 < command <= hand_size:
                    if snake[-1][1] in player_pieces[command-1]:
                        invalid = False
                        if snake[-1][1] == player_pieces[command-1][1]:
                            player_pieces[command-1].reverse()
                        snake.append(player_pieces.pop(command-1))
                    else:
                        print("Illegal move. Please try again.")
                else:
                    print("Invalid input. Please try again.")
        status = "computers_turn"
    else:
        break
