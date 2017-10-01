import pycosat
import numpy as np
import solver_efficient
import solver_naive
import time
import sudoku_encoding

def test_sudokus(sudoku_number, N, difficulty):
	# Opens file with set difficulty
	filename = "data\{0}\sudoku-{0}-{1}.npy".format(difficulty, sudoku_number)
	sudoku = np.load(filename)

	# Efficient encoding
	eff_encoding = solver_efficient.encoding_efficient(sudoku, N)

	# Naive encoding
	naive_encoding = solver_naive.encoding(sudoku, N)

	# Time for naive and efficient
	time_naive, time_eff = test_current_sudoku(eff_encoding, naive_encoding)
	return time_naive, time_eff

# Get time for current sudoku with both naive and efficient encoding
def test_current_sudoku(eff_encoding, naive_encoding):
	start_eff = time.time()
	solved_eff = pycosat.solve(eff_encoding)
	end_eff = time.time()
	# print(start_naive, end_naive)
	start_naive = time.time()
	solved_naive = pycosat.solve(naive_encoding)
	end_naive = time.time()
	# if solved_eff == solved_naive:
	# 	print("Yes")
	# print(sudoku_encoding.reverse_encoding(solved_naive, 9))
	# print(sudoku_encoding.reverse_encoding(solved_eff, 9))
	# print(start_eff, end_eff)
	return (end_naive - start_naive), (end_eff - start_eff)

def test_encoding(N):
	easy_time = [0, 0]
	medium_time = [0, 0]
	hard_time = [0, 0]
	insane_time = [0, 0]

	for i in range(0, 1):
		easy_time_naive, easy_time_eff = test_sudokus(i, N, "Easy")
		easy_time[0] += easy_time_naive
		easy_time[1] += easy_time_eff

		medium_time_naive, medium_time_eff = test_sudokus(i, N, "Medium")
		medium_time[0] += medium_time_naive
		medium_time[1] += medium_time_eff

		hard_time_naive, hard_time_eff = test_sudokus(i, N, "Hard")
		hard_time[0] += hard_time_naive
		hard_time[1] += hard_time_eff

		insane_time_naive, insane_time_eff = test_sudokus(i, N, "Insane")
		insane_time[0] += insane_time_naive
		insane_time[1] += insane_time_eff
	print(easy_time)
	print(medium_time)
	print(hard_time)
	print(insane_time)
	return easy_time, medium_time, hard_time, insane_time


easy, medium, hard, insane = test_encoding(9)