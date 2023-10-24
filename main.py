from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from board import Board

app = Flask(__name__)
Bootstrap(app)

board = Board()
winning_combos = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
winning_combo = []

game_over = False
player_one_move = True
player_one_win = False
player_two_win = False

p1_score = 0
p2_score = 0


def start():
    global board, game_over, winning_combo
    board = Board()
    game_over = False
    winning_combo = []


game_status = "Test"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        start()
    turn = request.args.get("turn")
    global game_status, player_one_move, p1_score, p2_score, winning_combo
    if player_one_move:
        status('p1')
    else:
        status('p2')
    if turn:
        chosen_square = int(turn)
        run_game(chosen_square)
    all_rows = [board.row1, board.row2, board.row3]
    all_squares = []
    for row in all_rows:
        for num in row:
            all_squares.append(num)
    if len(winning_combo) == 3:
        print(winning_combo)
    return render_template('index.html',
                           status=game_status,
                           p1_score=p1_score,
                           p2_score=p2_score,
                           all_squares=all_squares,
                           winning_combo=winning_combo)


# This function checks the board for a win #
# If a win is detected this function will end the game #
def check_for_win(player_nums):
    for combo in winning_combos:
        score = 0
        for num in combo:
            if num in player_nums:
                score += 1
        if score == 3:
            global game_over, winning_combo
            game_over = True
            print(combo)
            winning_combo = combo
            print(winning_combo)
            if player_nums == board.p1_nums:
                status('p1win')
            else:
                status('p2win')


def run_game(chosen_square):
    global player_one_move
    if not game_over:
        player_is_choosing = True
        while player_is_choosing:
            p_move = chosen_square
            if player_one_move:
                current_player = 'P1'
                status('p2')
                if not is_chosen(p_move):
                    player_is_choosing = False
                    add_to_board(p_move, current_player)
                    check_for_win(board.p1_nums)
                    player_one_move = False
                else:
                    player_is_choosing = False
            else:
                current_player = 'P2'
                status('p1')
                if not is_chosen(p_move):
                    player_is_choosing = False
                    add_to_board(p_move, current_player)
                    check_for_win(board.p2_nums)
                    player_one_move = True
                else:
                    player_is_choosing = False
    else:
        status('game_over')


# This function applies the player's symbol to the chosen spot on the board #
def add_to_board(player_move, current_player):
    if current_player == 'P1':
        board.p1_nums.append(player_move)
        symbol = 'X'
    else:
        board.p2_nums.append(player_move)
        symbol = 'O'
    if player_move < 4:
        board.row1[player_move - 1] = symbol
    elif player_move < 7:
        board.row2[player_move - 4] = symbol
    else:
        board.row3[player_move - 7] = symbol


# Checks if the chosen square has already been selected #
def is_chosen(player_move):
    if player_move in board.chosen_numbers:
        status('pick_again')
        return True
    else:
        board.chosen_numbers.append(player_move)
        return False


def status(current_status):
    global game_status, p1_score, p2_score
    if current_status == 'p1win':
        game_status = 'We have a winner! Xs 4 lyf!'
        p1_score += 1
    elif current_status == 'p2win':
        game_status = 'Winner! Team O, bad boy!'
        p2_score += 1
    elif current_status == 'pick_again':
        game_status = 'You wish. Already taken. Pick again bey.'
    elif current_status == 'p1':
        game_status = 'Team X, hit it'
    elif current_status == 'p2':
        game_status = 'Team O, get loose'
    elif current_status == 'game_over':
        game_status = 'Brah, the game is over. Start again dummy.'


if __name__ == "__main__":
    app.run(debug=True)