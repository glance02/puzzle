ROWS = 3
COLS = 3
TOKEN = {'PLAYER': 'x', 'BOT': 'o'}

def move_available(game_board, x, y):
    return game_board[x][y] == '*'

def is_move_end(game_board):
    for i in range(ROWS):
        for j in range(COLS):
            if game_board[i][j] == '*':
                return False
    return True

def is_victory(player, game_board):
    for i in range(COLS):
        if game_board[i][0] == player and game_board[i][1] == player and game_board[i][2] == player:
            return True

    for i in range(ROWS):
        if game_board[0][i] == player and game_board[1][i] == player and game_board[2][i] == player:
            return True
    
    if (game_board[0][0] == player and game_board[1][1] == player and game_board[2][2] == player) or (game_board[0][2] == player and game_board[1][1] == player and game_board[2][0] == player):
        return True

    return False

def print_board(game_board):
    board_string = ''
    for i in range(ROWS):
        board_string += ' '.join(game_board[i]) + '\n'
    print(board_string)

def fill_first_spot(game_board):
    for i in range(ROWS):
        for j in range(COLS):
            if game_board[i][j] == '*':
                game_board[i][j] = 'x'
                return

def minimax(game_board, depth, is_maximizing):
    if is_victory(TOKEN['BOT'], game_board):
        return float('inf')
    elif is_victory(TOKEN['PLAYER'], game_board):
        return float('-inf')
    elif is_move_end(game_board):
        return 0
    else:
        if is_maximizing:
            best_score = float('-inf')
            for i in range(ROWS):
                for j in range(COLS):
                    if game_board[i][j] == '*':
                        game_board[i][j] = 'o'
                        current_score = minimax(game_board, depth+1, False)
                        game_board[i][j] = '*'
                        best_score = max(best_score, current_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(ROWS):
                for j in range(COLS):
                    if game_board[i][j] == '*':
                        game_board[i][j] = 'x'
                        current_score = minimax(game_board, depth+1, True)
                        game_board[i][j] = '*'
                        best_score = min(best_score, current_score)
            return best_score            

def find_best_move(game_board):
    best_score = float('-inf')
    best_move = (-1, -1)
    for i in range(ROWS):
        for j in range(COLS):
            if game_board[i][j] == '*':
                game_board[i][j] = 'o'
                score = minimax(game_board, 0, False)
                game_board[i][j] = '*'
                if score > best_score:
                    best_move = (i, j)
    if best_move != (-1, -1):
        game_board[best_move[0]][best_move[1]] = 'o'
        return True
    return False


if __name__ == '__main__':
    board = [['*' for _ in range(COLS)] for _ in range(ROWS)]
    player = 'PLAYER'
    game_over = False
    game_winner = 'In Progress'

    while(not game_over):
        if player == 'PLAYER':
            print("Please enter a space separated matrix coordinate of where you want to make you token be placed")
            [row_coord, col_coord] = list(map(int, input().split(" ")))
            if move_available(board, row_coord, col_coord):
                board[row_coord][col_coord] = 'x'
                if is_victory(TOKEN[player], board):
                    game_over = True
                    game_winner = 'PLAYER'
                player = 'BOT'
        else:
            if find_best_move(board):
                if is_victory(TOKEN[player], board):
                    game_over = True
                    game_winner = 'BOT'
                player = 'PLAYER'
        
        if not game_over:
            if is_move_end(board):
                game_over = True
                game_winner = 'Tie'
        
        print_board(board)
    print(f'Winner of the game: {game_winner}')
    

            