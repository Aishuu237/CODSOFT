"""
Tic-Tac-Toe AI — Minimax with Alpha-Beta Pruning
═══════════════════════════════════════════════════
An unbeatable AI agent that uses the Minimax algorithm with
Alpha-Beta Pruning to play optimal Tic-Tac-Toe.

Concepts demonstrated:
  • Game tree search (Minimax)
  • Alpha-Beta Pruning (optimisation)
  • Terminal state evaluation
  • Game theory: zero-sum games

Run: python tictactoe.py
"""

import math
import time
import os



HUMAN = "X"
AI    = "O"
EMPTY = "."

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # cols
    (0, 4, 8), (2, 4, 6),              # diagonals
]



def make_board() -> list:
    """Return a fresh empty board (list of 9 cells)."""
    return [EMPTY] * 9


def display_board(board: list, nodes_evaluated: int = 0, elapsed: float = 0.0):
    """Render the board with coordinates guide."""
    os.system("cls" if os.name == "nt" else "clear")

    print("\n" + "═" * 38)
    print("      TIC-TAC-TOE  AI vs HUMAN ")
    print("═" * 38)

    symbols = {HUMAN: "X", AI: "O", EMPTY: "·"}
    colors  = {HUMAN: "\033[94m", AI: "\033[91m", EMPTY: "\033[90m"}
    RESET   = "\033[0m"

    print("\n  Board              Position Guide")
    print(" ┌───┬───┬───┐      ┌───┬───┬───┐")
    for row in range(3):
        cells = ""
        guide = ""
        for col in range(3):
            idx = row * 3 + col
            s   = symbols[board[idx]]
            c   = colors[board[idx]]
            cells += f" {c}{s}{RESET} │"
            guide += f" {idx+1} │"
        print(f" │{cells[:-1]}      │{guide[:-1]}")
        if row < 2:
            print(" ├───┼───┼───┤      ├───┼───┼───┤")
    print(" └───┴───┴───┘      └───┴───┴───┘")

    print(f"\n  \033[94mX\033[0m = You (Human)     \033[91mO\033[0m = AI")
    if nodes_evaluated:
        print(f"  🔍 Nodes evaluated : {nodes_evaluated:,}")
        print(f"  ⚡ Time taken      : {elapsed*1000:.1f} ms")
    print()


def get_available_moves(board: list) -> list[int]:
    """Return list of empty cell indices."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def check_winner(board: list) -> str | None:
    """Return HUMAN, AI, 'draw', or None if game is still on."""
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c] != EMPTY:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


def apply_move(board: list, idx: int, player: str) -> list:
    """Return a new board with the move applied (non-destructive)."""
    new_board = board[:]
    new_board[idx] = player
    return new_board





nodes_counter = [0]   # mutable counter shared across recursive calls


def minimax(board: list, depth: int, is_maximising: bool,
            alpha: float, beta: float) -> int:
    """
    Minimax with Alpha-Beta Pruning.

    Parameters
    ----------
    board          : current board state
    depth          : current recursion depth (used to prefer faster wins)
    is_maximising  : True → AI's turn (maximise), False → Human's (minimise)
    alpha          : best score the maximiser can guarantee so far
    beta           : best score the minimiser can guarantee so far

    Returns
    -------
    int : heuristic score of the board
    """
    nodes_counter[0] += 1

    winner = check_winner(board)
    if winner == AI:
        return 10 - depth          
    if winner == HUMAN:
        return depth - 10          
    if winner == "draw":
        return 0

    moves = get_available_moves(board)

    if is_maximising:
        best = -math.inf
        for move in moves:
            score = minimax(apply_move(board, move, AI),
                            depth + 1, False, alpha, beta)
            best  = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:          
                break
        return best
    else:
        best = math.inf
        for move in moves:
            score = minimax(apply_move(board, move, HUMAN),
                            depth + 1, True, alpha, beta)
            best  = min(best, score)
            beta  = min(beta, best)
            if beta <= alpha:          
                break
        return best


def best_ai_move(board: list) -> tuple[int, int, float]:
    """
    Find the best move for the AI using Minimax + Alpha-Beta Pruning.

    Returns (best_index, nodes_evaluated, elapsed_seconds)
    """
    nodes_counter[0] = 0
    start = time.perf_counter()

    best_score = -math.inf
    best_move  = -1

    for move in get_available_moves(board):
        score = minimax(apply_move(board, move, AI),
                        depth=0, is_maximising=False,
                        alpha=-math.inf, beta=math.inf)
        if score > best_score:
            best_score = score
            best_move  = move

    elapsed = time.perf_counter() - start
    return best_move, nodes_counter[0], elapsed




def get_human_move(board: list) -> int:
    """Prompt the human for a valid move (1-9)."""
    available = [str(m + 1) for m in get_available_moves(board)]
    while True:
        try:
            raw = input(f"  Your move (available: {', '.join(available)}): ").strip()
            idx = int(raw) - 1
            if 0 <= idx <= 8 and board[idx] == EMPTY:
                return idx
            else:
                print("   Invalid move. Pick an empty cell (1-9).")
        except (ValueError, KeyboardInterrupt):
            print("   Please enter a number between 1 and 9.")



def find_winning_line(board: list) -> list[int] | None:
    """Return the winning cell indices, or None."""
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c] != EMPTY:
            return [a, b, c]
    return None


def display_result(board: list, winner: str):
    """Show the final board with the winning line highlighted."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" + "═" * 38)
    print("      TIC-TAC-TOE  AI vs HUMAN  ")
    print("═" * 38)

    win_cells = find_winning_line(board) or []
    symbols   = {HUMAN: "X", AI: "O", EMPTY: "·"}
    RESET     = "\033[0m"

    print("\n  Final Board\n")
    print(" ┌───┬───┬───┐")
    for row in range(3):
        cells = ""
        for col in range(3):
            idx = row * 3 + col
            s   = symbols[board[idx]]
            if idx in win_cells:
                color = "\033[92;1m"   # bright green for winning cells
            elif board[idx] == HUMAN:
                color = "\033[94m"
            elif board[idx] == AI:
                color = "\033[91m"
            else:
                color = "\033[90m"
            cells += f" {color}{s}{RESET} │"
        print(f" │{cells[:-1]}")
        if row < 2:
            print(" ├───┼───┼───┤")
    print(" └───┴───┴───┘\n")

    if winner == AI:
        print("   \033[91mAI wins!\033[0m The Minimax algorithm is unbeatable.")
    elif winner == HUMAN:
        print("   \033[94mYou win!\033[0m That's... actually impossible. ")
    else:
        print("  \033[93mIt's a draw!\033[0m You played perfectly.")

    print()



def choose_who_goes_first() -> str:
    """Let the player choose who moves first."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" + "═" * 38)
    print("    TIC-TAC-TOE  AI vs HUMAN  ")
    print("═" * 38)
    print("\n  Who goes first?")
    print("  1. Human (X)")
    print("  2. AI    (O)\n")
    while True:
        choice = input("  Enter 1 or 2: ").strip()
        if choice == "1":
            return HUMAN
        if choice == "2":
            return AI
        print("   Please enter 1 or 2.")


def play_game():
    board       = make_board()
    current     = choose_who_goes_first()
    last_nodes  = 0
    last_elapsed = 0.0

    while True:
        display_board(board, last_nodes, last_elapsed)
        last_nodes   = 0
        last_elapsed = 0.0

        winner = check_winner(board)
        if winner:
            display_result(board, winner)
            return winner

        if current == HUMAN:
            print("  \033[94m● Your turn (X)\033[0m")
            move = get_human_move(board)
            board = apply_move(board, move, HUMAN)
        else:
            print("  \033[91m● AI is thinking...\033[0m")
            move, last_nodes, last_elapsed = best_ai_move(board)
            board = apply_move(board, move, AI)
            print(f"  AI chose cell {move + 1}")
            time.sleep(0.4)   # brief pause so the move is visible

        # Flip turn
        current = AI if current == HUMAN else HUMAN


def play_again() -> bool:
    ans = input("  Play again? (y/n): ").strip().lower()
    return ans in ("y", "yes")


def main():
    scores = {HUMAN: 0, AI: 0, "draw": 0}

    while True:
        winner = play_game()
        scores[winner] = scores.get(winner, 0) + 1

        print(f"  Score — You: {scores[HUMAN]}  AI: {scores[AI]}  Draws: {scores['draw']}\n")

        if not play_again():
            print("\n  Thanks for playing! \n")
            break



if __name__ == "__main__":
    main()