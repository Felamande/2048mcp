import random
import copy

class GameLogic:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.game_over = False
        # Add two initial tiles
        self._add_random_tile()
        self._add_random_tile()

    def get_status(self):
        """Returns the current state of the game."""
        return {
            "board": self.board,
            "score": self.score,
            "game_over": self.game_over,
            "size": self.size
        }

    def _get_empty_cells(self):
        """Returns a list of coordinates (row, col) of empty cells."""
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))
        return empty_cells

    def _add_random_tile(self):
        """Adds a random tile (2 or 4) to an empty cell."""
        empty_cells = self._get_empty_cells()
        if not empty_cells:
            return False # No space left

        r, c = random.choice(empty_cells)
        # 90% chance of 2, 10% chance of 4
        self.board[r][c] = 2 if random.random() < 0.9 else 4
        return True

    def _compress(self, row):
        """Compresses non-zero numbers to the left."""
        new_row = [i for i in row if i != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def _merge(self, row):
        """Merges adjacent identical numbers, moving left."""
        new_row = self._compress(row)
        score_increase = 0
        for i in range(self.size - 1):
            if new_row[i] != 0 and new_row[i] == new_row[i+1]:
                new_row[i] *= 2
                score_increase += new_row[i]
                new_row[i+1] = 0
        final_row = self._compress(new_row)
        return final_row, score_increase

    def _rotate_board_clockwise(self):
        """Rotates the board 90 degrees clockwise."""
        new_board = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size):
                new_board[c][self.size - 1 - r] = self.board[r][c]
        self.board = new_board

    def _rotate_board_counter_clockwise(self):
        """Rotates the board 90 degrees counter-clockwise."""
        new_board = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size):
                new_board[self.size - 1 - c][r] = self.board[r][c]
        self.board = new_board

    def _move_left(self):
        """Performs the 'left' move logic."""
        moved = False
        total_score_increase = 0
        new_board = []
        for r in range(self.size):
            original_row = self.board[r][:]
            new_row, score_increase = self._merge(original_row)
            new_board.append(new_row)
            total_score_increase += score_increase
            if original_row != new_row:
                moved = True
        self.board = new_board
        self.score += total_score_increase
        return moved

    def move(self, direction):
        """
        Performs a move in the specified direction ('up', 'down', 'left', 'right').
        Returns True if the board changed, False otherwise.
        """
        if self.game_over:
            return False

        original_board = copy.deepcopy(self.board)
        moved = False

        if direction == 'left':
            moved = self._move_left()
        elif direction == 'right':
            self._rotate_board_clockwise()
            self._rotate_board_clockwise()
            moved = self._move_left()
            self._rotate_board_clockwise()
            self._rotate_board_clockwise()
        elif direction == 'up':
            self._rotate_board_counter_clockwise()
            moved = self._move_left()
            self._rotate_board_clockwise()
        elif direction == 'down':
            self._rotate_board_clockwise()
            moved = self._move_left()
            self._rotate_board_counter_clockwise()
        else:
            # Invalid direction
            return False

        if moved:
            self._add_random_tile()
            if not self._can_move():
                self.game_over = True
        
        # Check again if board actually changed after adding tile potentially
        # This handles cases where a move merges tiles but doesn't shift anything,
        # and then the new tile fills the only empty spot, making the board look unchanged
        # compared to the very start, but a valid move occurred.
        # A simpler check is just if 'moved' was true.
        # return self.board != original_board 
        return moved


    def _can_move(self):
        """Checks if any moves are possible."""
        if self._get_empty_cells():
            return True # Can always add a tile if empty cells exist

        # Check for possible merges horizontally
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.board[r][c] == self.board[r][c+1]:
                    return True

        # Check for possible merges vertically
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.board[r][c] == self.board[r+1][c]:
                    return True

        return False

    def try_move(self, direction):
        """
        Simulates a move in the specified direction without changing the actual game state.
        Returns a dictionary with the simulated board state and whether the move was valid.
        """
        if self.game_over:
            return {
                "valid": False,
                "board": copy.deepcopy(self.board),
                "score": self.score,
                "game_over": self.game_over
            }

        # Create a deep copy of the current game state
        temp_game = GameLogic(self.size)
        temp_game.board = copy.deepcopy(self.board)
        temp_game.score = self.score
        temp_game.game_over = self.game_over

        # Perform the move on the temporary game state
        moved = temp_game.move(direction)

        # Return the simulated result
        return {
            "valid": moved,
            "board": temp_game.board,
            "score": temp_game.score,
            "game_over": temp_game.game_over
        }

# Example Usage (for testing)
if __name__ == "__main__":
    game = GameLogic()
    print("Initial Board:")
    for row in game.board:
        print(row)
    print(f"Score: {game.score}")

    game.move('left')
    print("\nAfter moving left:")
    for row in game.board:
        print(row)
    print(f"Score: {game.score}")

    game.move('up')
    print("\nAfter moving up:")
    for row in game.board:
        print(row)
    print(f"Score: {game.score}")

    while not game.game_over:
        # Simulate some moves
        moves = ['left', 'up', 'right', 'down']
        moved = game.move(random.choice(moves))
        if moved:
            print(f"\nMoved {moves[-1]}:")
            for row in game.board:
                print(row)
            print(f"Score: {game.score}")
        if not game._can_move():
            game.game_over = True
            print("\nGame Over!")

    print("\nFinal Board:")
    for row in game.board:
        print(row)
    print(f"Final Score: {game.score}")