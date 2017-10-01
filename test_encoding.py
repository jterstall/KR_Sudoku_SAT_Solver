import pycosat
import numpy as np
import solver_efficient
import solver_naive
import solver_pair
import time
import sudoku_encoding
import check_sudoku

# Test and time the encodings on a certain difficulty
def test_sudokus(sudoku_number, N, difficulty):
	# Opens file with set difficulty
	filename = "data\{0}\sudoku-{0}-{1}.npy".format(difficulty, sudoku_number)
	
	sudoku = np.load(filename)
	
	# Naive encoding
	start_naive = time.time()
	naive_encoding = solver_naive.encoding(sudoku, N)
	solved_naive = pycosat.solve(naive_encoding)
	end_naive = time.time()

	# Efficient encoding
	start_eff = time.time()
	eff_encoding = solver_efficient.encoding_efficient(sudoku, N)
	solved_eff = pycosat.solve(eff_encoding)
	end_eff = time.time()

	# Efficient encoding with recursion
	start_eff_recursive = time.time()
	eff_encoding_recursive = solver_efficient.encoding_efficient_recursion(sudoku, N)
	solved_eff_recursive = pycosat.solve(eff_encoding_recursive)
	end_eff_recursive = time.time()

	# Pair encoding
	start_pair = time.time()
	pair_encoding = solver_pair.encoding_pair(sudoku, N)
	solved_pair = pycosat.solve(pair_encoding)
	end_pair = time.time()

	time_naive = (end_naive - start_naive)
	time_eff = (end_eff - start_eff)
	time_eff_recursive = (end_eff_recursive - start_eff_recursive)
	time_pair = (end_pair - start_pair)

	print("Solved correctly naive: {0}".format(check_sudoku.validate_sudoku(sudoku_encoding.reverse_encoding(solved_naive, N), N)))
	print("Solved correctly efficient: {0}".format(check_sudoku.validate_sudoku(sudoku_encoding.reverse_encoding(solved_eff, N), N)))
	print("Solved correctly efficient with recursion: {0}".format(check_sudoku.validate_sudoku(sudoku_encoding.reverse_encoding(solved_eff_recursive, N), N)))
	print("Solved correctly pair: {0}".format(check_sudoku.validate_sudoku(sudoku_encoding.reverse_encoding(solved_pair, N), N)))
	print("\n")

	# Time for naive and efficient
	# time_naive, time_eff = test_current_sudoku(eff_encoding, naive_encoding, sudoku, N)
	return time_naive, time_eff, time_eff_recursive, time_pair

# Get time for current sudoku with both naive and efficient encoding
def test_current_sudoku(eff_encoding, naive_encoding, sudoku, N):
	start_eff = time.time()
	solved_eff = pycosat.solve(eff_encoding)
	end_eff = time.time()

	start_naive = time.time()
	solved_naive = pycosat.solve(naive_encoding)
	end_naive = time.time()

	sudoku_naive = sudoku_encoding.reverse_encoding(solved_naive, 9)
	sudoku_eff = sudoku_encoding.reverse_encoding(solved_eff, 9)

	naive_correct = check_sudoku.validate_sudoku(sudoku_naive, N)
	eff_correct = check_sudoku.validate_sudoku(sudoku_eff, N)

	# print(start_eff, end_eff)
	return (end_naive - start_naive), (end_eff - start_eff)
 
def test_encoding(N):
	easy_time = [0, 0, 0, 0]
	medium_time = [0, 0, 0, 0]
	hard_time = [0, 0, 0, 0]
	insane_time = [0, 0, 0, 0]

	for i in range(0, 10):
		easy_time_naive, easy_time_eff, easy_time_eff_recursive, easy_time_pair = test_sudokus(i, N, "Easy")
		easy_time[0] += easy_time_naive
		easy_time[1] += easy_time_eff
		easy_time[2] += easy_time_eff_recursive
		easy_time[3] += easy_time_pair

		medium_time_naive, medium_time_eff, medium_time_eff_recursive, medium_time_pair = test_sudokus(i, N, "Medium")
		medium_time[0] += medium_time_naive
		medium_time[1] += medium_time_eff
		medium_time[2] += medium_time_eff_recursive
		medium_time[3] += medium_time_pair

		hard_time_naive, hard_time_eff, hard_time_eff_recursive, hard_time_pair = test_sudokus(i, N, "Hard")
		hard_time[0] += hard_time_naive
		hard_time[1] += hard_time_eff
		hard_time[2] += hard_time_eff_recursive
		hard_time[3] += hard_time_pair

		insane_time_naive, insane_time_eff, insane_time_eff_recursive, insane_time_pair = test_sudokus(i, N, "Insane")
		insane_time[0] += insane_time_naive
		insane_time[1] += insane_time_eff
		insane_time[2] += insane_time_eff_recursive
		insane_time[3] += insane_time_pair

	print(easy_time)
	print(medium_time)
	print(hard_time)
	print(insane_time)

	return easy_time, medium_time, hard_time, insane_time


easy, medium, hard, insane = test_encoding(9)