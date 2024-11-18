"""
Sophie Agbekpenou
uni: saa2255
"""

import copy
import time
from BaseAI import BaseAI

# infinity
INF = float('inf')

class IntelligentAgent(BaseAI):
    def __init__(self):
        self.time_limit = 0.18
        self.start_time = None
        
    def getMove(self, grid):
        """
        Determines the best move for the agent using the Expectiminimax algorithm
        """
        self.start_time = time.process_time()
        best_move = None
        depth = 1

        # keep searching deeper until we run out of time
        while time.process_time() - self.start_time < self.time_limit:
            try:
                current_best_move = None
                best_score = -INF
                
                # try each possible move at current depth
                for move in grid.getAvailableMoves():
                    if time.process_time() - self.start_time >= self.time_limit:
                        raise TimeoutException()
                        
                    new_grid = grid.clone()
                    new_grid.move(move[0])
                    
                    score = self.expectiminimax(new_grid, depth - 1, False)
                    
                    if score > best_score:
                        best_score = score
                        current_best_move = move[0]
                
                if current_best_move is not None:
                    best_move = current_best_move
                    
                depth += 1
                
            except TimeoutException:
                break

        # return the best move found so far, or the first available move if none found
        if best_move is None and grid.getAvailableMoves():
            return grid.getAvailableMoves()[0][0]
        return best_move

    def expectiminimax(self, grid, depth, is_maximizing):
        """
        Implements the Expectiminimax algorithm with a depth limit
        """
        if time.process_time() - self.start_time >= self.time_limit:
            raise TimeoutException()

        # if no available moves -> game over
        if not grid.getAvailableMoves():
            return -INF
        
        # else if depth limit is reached -> evaluate current grid state
        elif depth == 0:
            return self.evaluate_grid(grid)

        # player tries to maximize the evaluation score
        if is_maximizing:
            max_eval = -INF

            # explore all possible moves for the maximizing player
            for move in grid.getAvailableMoves():
                # copy grid & stimulate the move
                new_grid = grid.clone()
                new_grid.move(move[0])

                # update the highest score achievable by the maximizing player
                eval = self.expectiminimax(new_grid, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        
        # chance node (ai simulates random tile placement)
        else: 
            total_eval = 0

            # get all available cells to simulate placement of a new tile
            open_tiles = grid.getAvailableCells()
            prob_per_cell = 1.0 / len(open_tiles)
            
            for cell in open_tiles:
                # placing a '2' tile with 90% probability
                new_grid = grid.clone()
                new_grid.insertTile(cell, 2)
                total_eval += 0.9 * prob_per_cell * self.expectiminimax(new_grid, depth - 1, True)
                
                # placing a '4' tile with 10% probability
                new_grid = grid.clone()
                new_grid.insertTile(cell, 4)
                total_eval += 0.1 * prob_per_cell * self.expectiminimax(new_grid, depth - 1, True)

            return total_eval

    def snakeHeuristic(self, grid):
        """
        Calculates a heuristic score based on a snake pattern

        Source: Nie, Y., Hou, W., & An, Y. "AI Plays 2048."
        """
        PERFECT_SNAKE = [
            [2**15, 2**14, 2**13, 2**12],
            [2**8, 2**9, 2**10, 2**11],
            [2**7, 2**6, 2**5, 2**4],
            [2**0, 2**1, 2**2, 2**3]
        ]
        score = 0
        
        for i in range(4):
            for j in range(4):
                score += grid.map[i][j] * PERFECT_SNAKE[i][j]
        return score

    def count_empty_cells(self, grid):
        """
        Counts the number of empty cells on the grid
        """
        return len(grid.getAvailableCells())

    def monotonicity(self, grid):
        """
        Calculates monotonicity score by checking both rows and columns
        in both increasing and decreasing directions.
        
        Returns higher score if numbers are arranged in a consistent
        increasing or decreasing pattern in both directions.
        """
        score = 0
        
        # check rows
        for i in range(4):
            # left to right monotonicity
            increasing = 0
            decreasing = 0
            for j in range(1, 4):
                if grid.map[i][j-1] != 0 and grid.map[i][j] != 0:
                    if grid.map[i][j] >= grid.map[i][j-1]:
                        increasing += grid.map[i][j] - grid.map[i][j-1]
                    if grid.map[i][j] <= grid.map[i][j-1]:
                        decreasing += grid.map[i][j-1] - grid.map[i][j]
            score += max(increasing, decreasing)
        
        # check columns
        for j in range(4):
            # top to bottom monotonicity
            increasing = 0
            decreasing = 0
            for i in range(1, 4):
                if grid.map[i-1][j] != 0 and grid.map[i][j] != 0:
                    if grid.map[i][j] >= grid.map[i-1][j]:
                        increasing += grid.map[i][j] - grid.map[i-1][j]
                    if grid.map[i][j] <= grid.map[i-1][j]:
                        decreasing += grid.map[i-1][j] - grid.map[i][j]
            score += max(increasing, decreasing)
        
        return score

    def smoothness(self, grid):
        """
        Calculates smoothness score based on value differences between adjacent tiles
        """
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if grid.map[i][j] != 0:
                    # check horizontal neighbor
                    if j < 3 and grid.map[i][j+1] != 0:
                        smoothness -= abs(grid.map[i][j] - grid.map[i][j+1])
                    # heck vertical neighbor
                    if i < 3 and grid.map[i+1][j] != 0:
                        smoothness -= abs(grid.map[i][j] - grid.map[i+1][j])
        return smoothness

    def evaluate_grid(self, grid):
        """
        Combines multiple heuristics to evaluate the grid state
        """
        empty_cells_score = self.count_empty_cells(grid) * 100
        snake_pattern_score = self.snakeHeuristic(grid) * 1
        monotonicity_score = self.monotonicity(grid) * 10
        smoothness_score = self.smoothness(grid) * 5

        h_sum = empty_cells_score + snake_pattern_score + monotonicity_score + smoothness_score
        
        return h_sum

class TimeoutException(Exception):
    pass