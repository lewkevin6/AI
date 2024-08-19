from sudoku import Sudoku
import queue
import copy
import math

'''
Parameters: Takes as input the curr_board state and the puzzle
Returns: True if the current board state is the goal and False if not
Note: Existing version solves the puzzle everytime you test for goal
      feel free to change the implementation to save time
'''
def test_goal(curr_board,puzzle):
    puzzle_solution=puzzle.solve()
    try:
        solution_board=puzzle_solution.board
        for i in range(len(solution_board)):
            for j in range(len(solution_board[i])):
                assert(curr_board[i][j]==solution_board[i][j])
        return True
    except Exception as e:
        return False

'''
Parameters: Takes as input a puzzle board and puzzle size
Returns: True if the puzzle board is valid and False if not
'''    
def valid_puzzle(puzzle_size,puzzle_board):
    puzzle=Sudoku(puzzle_size,board=puzzle_board)
    return puzzle.validate()

'''
Parameters: Takes as input a puzzle board
Returns: Returns all the cells in the grid that are empty
'''
def empty_cells(puzzle_board):
    empty_cell_list=[]
    for i in range(len(puzzle_board)):
        for j in range(len(puzzle_board[i])):
            if puzzle_board[i][j] is None:
                empty_cell_list.append([i,j])
    return empty_cell_list

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs(puzzle):
    frontier = queue.Queue() 

    explored = []  #Initalize empty explored data structure
    
    frontier.put(puzzle) #Initialize frontier with puzzle

    for x in range(len(empty_cells(puzzle.board)) + 1): # How many empty slots are there in the original (Depth control)
        for y in range(frontier.qsize()): # How many nodes are there per depth layer

            current_puzzle = copy.deepcopy(frontier.get()) #Copy current popped node
            
            empty = empty_cells(current_puzzle.board) #How many empty nodes are in the current popped node

            explored.append(current_puzzle)# Add the node to explored

            for i in range(len(empty)): #For every empty cell
                for j in range(1,len(puzzle.board)+1):    #Fill it in with 1-4
                    copy_puzzle = copy.deepcopy(current_puzzle)
                    copy_puzzle.board[empty[i][0]][empty[i][1]] = j

                    if test_goal(copy_puzzle.board, puzzle) == True: #Check goal before adding to frontier
                        return copy_puzzle
                    
                    if copy_puzzle not in explored: #If not in explored, add it in
                        frontier.put(copy_puzzle)
                
    return None #Return failure

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs(puzzle):
    frontier = queue.LifoQueue()

    explored = []  #Initalize empty explored data structure

    frontier.put(puzzle) #Initialize frontier with puzzle

    failure = None

    while not frontier.empty():
        current_puzzle = copy.deepcopy(frontier.get())
        empty = empty_cells(current_puzzle.board)

        if test_goal(current_puzzle.board, puzzle) == True: #Check goal before expanding
            return current_puzzle
        
        for i in range(len(empty)): #Populate
            for j in range(1,len(puzzle.board)+1):    
                copy_puzzle = copy.deepcopy(current_puzzle)
                copy_puzzle.board[empty[i][0]][empty[i][1]] = j
                
                if copy_puzzle not in explored: #If not in explored, add it in
                    frontier.put(copy_puzzle)

    return failure

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def bfs_with_prunning(puzzle):
    frontier = queue.Queue() 

    explored = []  #Initalize empty explored data structure
    
    frontier.put(puzzle) #Initialize frontier with puzzle

    for x in range(len(empty_cells(puzzle.board)) + 1): # How many empty slots are there in the original (Depth control)
        for y in range(frontier.qsize()): # How many nodes are there per depth layer

            current_puzzle = copy.deepcopy(frontier.get()) #Copy current popped node
            
            empty = empty_cells(current_puzzle.board) #How many empty nodes are in the current popped node

            explored.append(current_puzzle)# Add the node to explored

            for i in range(len(empty)): #For every empty cell
                for j in range(1,len(puzzle.board)+1):    #Fill it in with 1-4
                    copy_puzzle = copy.deepcopy(current_puzzle)
                    copy_puzzle.board[empty[i][0]][empty[i][1]] = j

                    if test_goal(copy_puzzle.board, puzzle) == True: #Check goal before adding to frontier
                        return copy_puzzle
                    
                    if copy_puzzle not in explored and valid_puzzle(int(math.sqrt(len(puzzle.board))),copy_puzzle.board): #If not in explored, add it in, check if its valid puzzle board
                        frontier.put(copy_puzzle)
                
    return None #Return failure

'''
params: Takes the current puzzle as input
Return: The puzzle board corresponding to the goal
Note: You can modify the function definition as you see fit
'''
def dfs_with_prunning(puzzle):
    frontier = queue.LifoQueue()

    explored = []  #Initalize empty explored data structure

    frontier.put(puzzle) #Initialize frontier with puzzle

    failure = None

    while not frontier.empty():
        current_puzzle = copy.deepcopy(frontier.get())
        empty = empty_cells(current_puzzle.board)

        if test_goal(current_puzzle.board, puzzle) == True: #Check goal before expanding
            return current_puzzle
        
        for i in range(len(empty)): #Populate
            for j in range(1,len(puzzle.board)+1):    
                copy_puzzle = copy.deepcopy(current_puzzle)
                copy_puzzle.board[empty[i][0]][empty[i][1]] = j

                if copy_puzzle not in explored and valid_puzzle(int(math.sqrt(len(puzzle.board))),copy_puzzle.board): #If not in explored, add it in and check if its valid puzzle board
                    frontier.put(copy_puzzle)
    

    return failure


if __name__ == "__main__":

    
    puzzle=Sudoku(2,2).difficulty(0.2) # Constructs a 2 x 2 puzzle
    puzzle.show() # Pretty prints the puzzle
    print(valid_puzzle(2,puzzle.board)) # Checks if the puzzle is valid
    print(test_goal(puzzle.board,puzzle)) # Checks if the given puzzle board is the goal for the puzzle
    print(empty_cells(puzzle.board)) # Prints the empty cells as row and column values in a list for the current puzzle board

    print("Solution")
    print(puzzle.solve())

    print("BFS Solution")
    print(bfs(puzzle))

    print("DFS Solution")
    print(dfs(puzzle))

    print("BFS Prunning Solution")
    print(bfs_with_prunning(puzzle))

    print("DFS Prunning Solution")
    print(dfs_with_prunning(puzzle))




    #Evaluation

    # import time
    # import numpy as np

    # time_list = []
    # eval_puzzle=Sudoku(2,2).difficulty(0.7)
    # eval_puzzle.show()

    # for i in range(10):
    #     start = time.time()
    #     dfs_with_prunning(eval_puzzle)
    #     end = time.time()
    #     time_taken = end - start
    #     time_list.append(time_taken)

    # time_list = np.array(time_list)
    # print(time_list.mean())

    #Single run to determine if it goes over the run time limit of 100 seconds
    # start = time.time()
    # bfs(eval_puzzle)
    # end = time.time()
    # print(end - start)