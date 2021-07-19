# %%

import numpy as np

# Function that imports text file and returns the number of puzzles as well as
# an array of puzzles
def getPuzzles():

        # Request file name from user input            
        filename = input("Please enter a file name: ")
        file = open(filename).read()
                
        # Open Input File
        # file = open('prog1_input.txt').read()
        
        # Split lines using newline character as delimiter
        file = [item.split() for item in file.split('\n')[:-1]]
        
        # Remove empty rows
        file2 = [x for x in file if x != []]
        
        # Extract Number of puzzles from first line
        num_puzzles = int(file2[0][0])
        # Initialize list of puzzles
        puzzles = list(np.ones(num_puzzles))
        
        # Loop through file
        for i in range(len(file2)):
            for j in range(len(file2[i])):
                
                # Check for E's and replace with zeros
                if (file2[i][j] == 'E'):
                    file2[i][j] = 0    
                # Otherwise convert to integer
                else:
                    file2[i][j] = int(file2[i][j])
                    
        # Loop through file from lines 4 to end of file, in steps of 3, saving 
        # values into puzzles array
        for i in range(3,len(file2), 3):          
            puzzles[int(i/3)-1] = file2[i-2] + file2[i-1] + file2[i]
            
        # Reshape each puzzle in puzzles to a 3x3 matrix
        for i in range(len(puzzles)):
            puzzles[i] = np.reshape(puzzles[i], (3,3))
        
        # Extract num_puzzles from first line
        num_puzzles = file2[0][0] 
        
        return puzzles, num_puzzles
    
#Function that checks inversion count to detect if puzzle is solvable 
def isSolvable(puzzle):
    
    # Flatten puzzle into 1D array
    puzzle = puzzle.flatten()
    
    # Initialize inversion count            
    inv_count = 0
    
    # Calculate inversion count
    for i in range(0,len(puzzle)-1):
        for j in range(i+1, len(puzzle)):
               
            #if (puzzle[i] != 0 and puzzle[i] > puzzle[j]):
            if (i<j and puzzle[i] > puzzle[j]):
                inv_count += 1 
                
    #print(inv_count)
    # Return bool            
    return (inv_count % 2 == 0)

class State:
    
    # Initialize State with Variables:
    # puzzle = current puzzle state
    # level = level of search tree that State lies in
    # fval = value of f(x) or total estimated cost to goal state including
    #        heuristic
    # parent = parent state to allow for backtracking of moves
    
    def __init__(self,puzzle,level,fval,parent):
        self.puzzle = puzzle
        self.level = level
        self.fval = fval
        self.parent = parent
        
    # Function that gets possible states branching from current state    
    def getChildren(self):
        
        # Use search function to get x and y coordinates of 0 in the puzzle
        x,y = self.search(self.puzzle,0)
        
        # Create list of coordinates that surround the 0
        coor_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        
        # Create empty children array
        children = []
        
        # Loop through coordinate list
        for i in coor_list:
            # Check coordinate is a valid position, meaning it exists on the
            # puzzle
            child = self.isValid(self.puzzle,x,y,i[0],i[1])
            
            # If child is valid...
            if child != False:
                # Create State instance for the child, incrementing level
                child_node = State(child,self.level+1,0,self.puzzle)
                #print(child_node.level)
                
                # Append new child_node to children array
                children.append(child_node)
                
        # Return children array        
        return children
      
    # Function that searches the puzzle for x    
    def search(self,puzzle,x):
        for i in range(0,len(self.puzzle)):
            for j in range(0,len(self.puzzle)):
                if puzzle[i][j] == x:
                    return i,j
                
    # Checks if input coordinate is a valid position    
    def isValid(self,puzzle,x1,y1,x2,y2):
        
        # if coordinate is in bounds
        if x2 >= 0 and x2 < len(self.puzzle) and y2 >= 0 and y2 < len(self.puzzle):
            # Create temporary puzzle to return
            temp_puzzle = []
            temp_puzzle = self.copy_matrix(puzzle)
            temp = temp_puzzle[x2][y2]
            temp_puzzle[x2][y2] = temp_puzzle[x1][y1]
            temp_puzzle[x1][y1] = temp
            return temp_puzzle
        else:
            return False
        
    # Function that makes a copy of the matrix to avoid unwanted replacement    
    def copy_matrix(self,root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    

class Puzzle:
    
    # Initialize with lists for open and closed states
    def __init__(self):
        self.open_states = []
        self.closed_states = []        
    
    # Function that calculates manhattan distance for use as the heuristic.    
    def h_dist(self,initial_state,goal_state):
        
        # Initialize empty variables
        manh_dist = []
        manhattan_dist = 0
        
        # Loop through puzzle creating array of manhattan distances for each
        # coordinate
        for i in range (0,3):
            for j in range (0,3):
                manh_dist.append(goal_state[i][j])
                
        # Loop through puzzle 
        for i in range (0,3):
            for j in range (0,3):
                
                # Get value of puzzle at coordinate i,j
                current_coord = initial_state[i][j]
                x_coor = i
                y_coor = j
                
                # Get index of current coordinate in list of manhattan
                # distances
                index = manh_dist.index(current_coord)                
                
                # Calculate row and column coordinates of goal state from 
                # index of array
                x_goal, y_goal = index//3,index%3
                # print("index and goal:", index, x_goal, y_goal)
                
                # If current coordinate is not zero, calculate manhattan
                # distance and add to total manhattan distance
                if current_coord != 0:
                    manhattan_dist += (np.abs(x_goal - x_coor) + np.abs(y_goal - y_coor))
        
        return manhattan_dist
    
    # Function that calculates total distance using level and manhattan distance    
    def f_dist(self,initial_state,goal_state):
        g = initial_state.level
        h = self.h_dist(initial_state.puzzle,goal_state)
        f = g + h
        # print("g(x): ",g)
        # print("h(x): ",h)
        # print("f(x): ",f)
        return f


    # Main function that runs A*    
    def astar(self, puzzle):
            counter = 0 

            initial_state = puzzle.tolist()
            
            
            # Puzzle 3 hard coded for debugging
            #initial_state = [[4, 2, 0], [5, 1, 6], [7, 3, 8]]
            #print(initial_state)
            
            # Initialize goal state
            goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]                    
            
            # Create State instance for initial state
            initial_state = State(initial_state,0,0, -1)
            # print(initial_state.value)
            
            # Calculate total estimated distance from initial state to goal state
            initial_state.fval = self.f_dist(initial_state,goal_state)

            # Append initial state to list of open states            
            self.open_states.append(initial_state)
            print("\n\n")
            
            # Initialize iterations
            iterations = 0
            
            while True:
                
                # Increment iterations and print error if iteration count
                # reaches certain value.
                iterations += 1
                if iterations >= 50000:
                    print("Could not solve puzzle in", iterations, "iterations. There must have been an error calculating inversions.")
                    break
                
                
                current_state = self.open_states[0]
                if counter == 0:
                    counter = 1
                else:
                    print("\n")
                    
                for i in current_state.puzzle:
                    for j in i:
                        print(j,end=" ")
                    print("")
                
                # Break loop if current state of puzzle equals goal state
                if(self.h_dist(current_state.puzzle,goal_state) == 0):
                    break
                        
                # Loop through children of current state
                for i in current_state.getChildren():
                    # Calculate total distance from current child to goal state
                    i.fval = self.f_dist(i,goal_state)
                    # Append child to open states list                        
                    self.open_states.append(i)
                # Append current state to closed states list and delete from
                # list of open states
                self.closed_states.append(current_state)
                del self.open_states[0] 
                
                # Sort open states list by lowest distance to goal state
                # to prepare for next iteration
                self.open_states.sort(key = lambda x:x.fval,reverse=False)
            
            # Calculate path cost
            f = self.f_dist(current_state, goal_state)
            print("Iterations: ", iterations)
            print("Path Cost: ",f)
            print("Open States: ",len(self.open_states))
            print("Closed States: ",len(self.closed_states))          
        
                


#%% Run this cell to check inversions and solve only the ones calculated to 
#   be solvable

puzzles = getPuzzles()

for i in range(len(puzzles[0])):
    current_puzzle = puzzles[0][i]
    if isSolvable(current_puzzle):
        print("Puzzle", i+1, "IS solvable")
        puzzle = Puzzle()
        puzzle.astar(current_puzzle)
        input("Press Enter to continue to next puzzle")
    else:
        print("Puzzle", i+1, "is NOT solvable")
        input("Press Enter to continue to next puzzle")
        

#%% Run this cell to brute force until max iterations is reached.
#   Max Iterations currently set to 50,000

puzzles = getPuzzles()
current_puzzle = puzzles[0][4] ## Change value to reflect desired puzzle
Puzzle = Puzzle()
Puzzle.astar(current_puzzle)
