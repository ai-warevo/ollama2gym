from typing import List, Optional, Literal
from core.logger import get_logger

logger = get_logger("tictactoe.engine")

class TicTacToeEngine:
    """
    Core game logic for a 3x3 Tic-Tac-Toe game.
    Designed to be decoupled from any UI for potential Gymnasium integration.
    """

    EMPTY = 0
    PLAYER_X = 1
    PLAYER_O = 2

    def __init__(self) -> None:
        logger.debug("Initializing engine")
        self.board: List[int] = [self.EMPTY] * 9
        self.current_player: Literal[self.PLAYER_X, self.PLAYER_O] = self.PLAYER_X
        self.winner: Optional[int] = None
        self.is_draw: bool = False

    def reset(self) -> None:
        """Resets the game state to default."""
        logger.info("Resetting engine")
        self.board = [self.EMPTY] * 9
        self.current_player = self.PLAYER_X
        self.winner = None
        self.is_draw = False

    def make_move(self, position: int) -> bool:
        """
        Attempts to make a move at the specified position (0-8).
        Returns True if the move was successful, False otherwise.
        """
        logger.debug(f"Making move at position {position}")
        if not (0 <= position < 9):
            logger.warning(f"Invalid move position: {position}")
            return False
        
        if self.board[position] != self.EMPTY or self.winner is not None or self.is_draw:
            logger.debug(f"Move at {position} is invalid (board full, winner exists, or draw)")
            return False

        self.board[position] = self.current_player
        logger.info(f"Player {self.current_player} moved to position {position}")
        
        if self._check_winner(position):
            self.winner = self.current_player
            logger.info(f"Winner declared: Player {self.winner}")
        elif self._check_draw():
            self.is_draw = True
            logger.info("Game resulted in a draw")
        else:
            self._switch_turn()
            
        return True

    def _switch_turn(self) -> None:
        """Switches the active player."""
        if self.current_player == self.PLAYER_X:
            self.current_player = self.PLAYER_O
        else:
            self.current_player = self.PLAYER_X

    def _check_winner(self, last_move_pos: int) -> bool:
        """Checks if the last move resulted in a win."""
        # Winning combinations (indices)
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]

        for combo in win_combinations:
            if all(self.board[i] == self.board[combo[0]] and self.board[i] != self.EMPTY for i in combo):
                return True
        return False

    def _check_draw(self) -> bool:
        """Checks if the board is full without a winner."""
        return all(cell != self.EMPTY for cell in self.board)

    def get_board(self) -> List[int]:
        """Returns the current state of the board."""
        return list(self.board)

    def get_current_player(self) -> int:
        """Returns the ID of the current player."""
        return self.current_player

    def get_winner(self) -> Optional[int]:
        """Returns the winner (1 or 2) or None if no winner yet."""
        return self.winner

    def is_game_over(self) -> bool:
        """Checks if the game has ended due to a win or draw."""
        return self.winner is not None or self.is_draw
