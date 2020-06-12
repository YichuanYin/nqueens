This n-queens solver has two modes:
1. Solves the standard n-queens given a board size
2. Solves the n-queens on a board partially filled with some queens

Dependencies:
	This solves uses CP-Sat solver which is part of the python ortools library.
	For example, it can be installed with the following command:
		python -m pip install --upgrade --user ortools

Usage:
	{ python nqueens.py [board_size] | python nqueens.py [board_size] [prefill.txt] }
          [board_size] is the size of the board, is has dimension [board_size] x [board_size]
          [prefill.txt] should contain a pair of integers on each line separated by a space character,
          the pair of integers denote the location of a prefilled queen on the board,
          the first number is the row index, the second number is the column index

Output:
	All solutions are outputted in a file named solutions_n=[board_size].txt where [board_size] is the size of the board.
	The solution is of ASCII format that resembles a chess board.
	The character 'Q' represents a queen.
	The character '-' represents a blank.