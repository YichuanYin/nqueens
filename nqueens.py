# Program: an n-queens solver that can take in partially-filled boards using CP-SAT solver
# Dependency: The CP-SAT solver from python ortools library
# Usage:   { python nqueens.py [board_size] | python nqueens.py [board_size] [prefill.txt] }
#           [board_size] is the size of the board, is has dimension [board_size] x [board_size]
#           [prefill.txt] should contain a pair of integers on each line separated by a space character,
#           the pair of integers denote the location of a prefilled queen on the board,
#           the first number is the row index, the second number is the column index



#------------------- Library Imports ------------------------
from __future__ import print_function
from ortools.sat.python import cp_model
#------------------------------------------------------------



#----------------- Solution output routine ------------------
class Solution_board_output (cp_model.CpSolverSolutionCallback):
    
    def __init__ (self, variables):
        cp_model.CpSolverSolutionCallback.__init__ (self)
        self.vars = variables
        self.num_solutions = 0
        
    # Return the number of solutions
    def SolutionCount (self):
        return self.num_solutions
    
    # Print the first solution to console, save all solutions to file
    def OnSolutionCallback (self):
        self.num_solutions += 1

        if self.num_solutions == 1:
            print ('First solution:')
            
        for var in self.vars:
            col_indx = int (self.Value (var))

            for x in range (board_size):
                if x == col_indx:
                    if self.num_solutions == 1:
                        print ('Q ', end='')
                    solution_file.write ('Q ')
                else:
                    if self.num_solutions == 1:
                        print ('- ', end='')
                    solution_file.write ('- ')
                    
            if self.num_solutions == 1:
                print ()
            solution_file.write ('\n')
                
        solution_file.write ('\n')
        solution_file.write ('\n')
#------------------------------------------------------------



#-------------------- Function main -------------------------
def main (board_size):
    
    # Declare a CP-SAT solver model
    nqueens_model = cp_model.CpModel ()
    
    # Create the SAT variables for the column and row constraints
    # We encode the column index of a queen into the index of a variable,
    # the value of the variable denotes the row index for a queen
    grid_vars = []
    for x in range (board_size):
        grid_vars.append (nqueens_model.NewIntVar (0, board_size - 1, 'x%i' % x))
    
    # Check if we need to prefill the board with some given queens
    if prefill_flag == 1:
        for x in pos_dict:
            nqueens_model.Add (grid_vars [x] == pos_dict [x])
    
    # Add the row constraints, the column constraints need not be added because the
    # indices of queens sat variables are already all different
    nqueens_model.AddAllDifferent (grid_vars)
    
    # Add the diagonal constraints
    for x in range (board_size):
        diagonal_vars_1 = []
        diagonal_vars_2 = []
        
        for y in range (board_size):
        
            # Create the first variable list
            queens_vars_1 = nqueens_model.NewIntVar (-board_size, board_size, 'diagonal_vars_1_%x' % x)
            nqueens_model.Add (- y + grid_vars[y] == queens_vars_1)
            diagonal_vars_1.append (queens_vars_1)
        
            # Create the second variable list
            queens_vars_2 = nqueens_model.NewIntVar (0, 2*board_size, 'diagonal_vars_2_%x' % x)
            nqueens_model.Add (y + grid_vars[y] == queens_vars_2)
            diagonal_vars_2.append (queens_vars_2)
        
        # Enforce the constraints
        nqueens_model.AddAllDifferent (diagonal_vars_1)
        nqueens_model.AddAllDifferent (diagonal_vars_2)
            
    # Declare a CP-Sat Solver
    nqueens_solver = cp_model.CpSolver ()
    
    # Set up solution output
    solution_output = Solution_board_output (grid_vars)
        
    # Solve for solutions
    nqueens_solver.SearchForAllSolutions (nqueens_model, solution_output)
    
    # Print solution messages
    print ('Total number of solutions: %i' % solution_output.SolutionCount ())
    print ('Wrote to file: ' + 'solutions_n=' + str (board_size) + '.txt')
    print ('Solver time:', nqueens_solver.WallTime () * solution_output.SolutionCount (), 'ms')
#------------------------------------------------------------



#------------------ Pre-main preprocessing ------------------
import sys
if __name__ == '__main__':
    
    # Flag for whether a prefilled board exists
    prefill_flag = 0
    
    arg_len = len (sys.argv)
    
    # No prefilled board
    if arg_len > 1:
        board_size = int (sys.argv [1])
    
    # Yes prefilled board
    if arg_len > 2:
        filename = str (sys.argv [2])
        prefill_flag = 1
        
        # Read a prefilled board from file
        pos_dict = {}
        with open (filename) as f:
            for line in f:
                data = line.split()
                pos_dict [int (data[0])] = int (data[1])
                
        # Verify the prefilled board for the user
        print ('Received prefilled coordinates:')
        for i in range (board_size):
            for j in range (board_size):
                if i in pos_dict and pos_dict [i] == j:
                    print ('Q ', end='')
                else:
                    print ('- ', end='')
            print ()
            
    # Open a solution file for output printing, with board_size in the file name
    solution_file = open ('./solutions/sol_n=' + str (board_size) + '.txt', 'w')
    
    # Calls main function
    main (board_size)
#------------------------------------------------------------
