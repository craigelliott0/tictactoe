from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


row1 = ['1', '2', '3']
row2 = ['4', '5', '6']
row3 = ['7', '8', '9']
print(f"{row1}\n{row2}\n{row3}")


@app.route("/")
def home():
    return render_template('index.html', row1=row1, row2=row2, row3=row3)


winning_combos = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
chosen_numbers = []
p1_nums = []
p2_nums = []

game_over = False


# This function checks the board for a win #
# If a win is detected this function will end the game #
def check_for_win(player_nums):
    for combo in winning_combos:
        score = 0
        for num in combo:
            if num in player_nums:
                score += 1
        if score == 3:
            global game_over
            game_over = True
            if player_nums == p1_nums:
                print("Player 1 wins! Xs 4 lyf")
            else:
                print("Player 2 wins! OOO m g!")


# Game loop #
# Takes players' inputs and executes the above functions until a win is detected #
def run_game():
    while not game_over:
        # player_move('player1')
        player_is_choosing = True
        while player_is_choosing:
            p1_move = int(input("Player 1, pick a number: "))
            current_player = 'Player 1'
            if not is_chosen(p1_move):
                player_is_choosing = False
                add_to_board(p1_move, current_player)
                check_for_win(p1_nums)

        if not game_over:
            # player_move('player2')
            player_is_choosing = True
            while player_is_choosing:
                p2_move = int(input("Player 2, pick a number: "))
                current_player = 'Player 2'
                if not is_chosen(p2_move):
                    player_is_choosing = False
                    add_to_board(p2_move, current_player)
                    check_for_win(p2_nums)


# This function applies the player's symbol to the chosen spot on the board #
def add_to_board(player_move, current_player):
    # if player_move == p1_move:
    if current_player == 'Player 1':
        p1_nums.append(player_move)
        symbol = 'X'
    else:
        p2_nums.append(player_move)
        symbol = 'O'
    if player_move < 4:
        row1[player_move - 1] = symbol
    elif player_move < 7:
        row2[player_move - 4] = symbol
    else:
        row3[player_move - 7] = symbol
    print(f"{row1}\n{row2}\n{row3}")


# Checks if the chosen number has already been selected #
def is_chosen(player_move):
    if player_move in chosen_numbers:
        print("You wish. Already taken. Pick again bey.")
        return True
    else:
        chosen_numbers.append(player_move)
        return False


# NOTE TO SELF: trying to get this function to replace the repeated code in the Game Loop below.
# Not sure if it's actually less readable though. #
# def player_move(player):
#     player_is_choosing = True
#     while player_is_choosing:
#         if player == 'player1':
#             p_nums = p1_nums
#             p1_move = int(input("Player 1, pick a number: "))
#             p_move = p1_move
#         else:
#             p_nums = p2_nums
#             p2_move = int(input("Player 2, pick a number: "))
#         if not is_chosen(p_move):
#             player_is_choosing = False
#             add_to_board(p_move)
#             check_for_win(p_nums)


# run_game()

if __name__ == "__main__":
    app.run(debug=True)