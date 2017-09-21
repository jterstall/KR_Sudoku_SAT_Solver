import sudoku_generator
import numpy as np

def generate_sudokus(level, amount):
	try:
		dir_name = "data/{0}/".format(level)
		for i in range(1, amount+1):
			file_name =  "{0}sudoku-{1}-{2}".format(dir_name, level, i) 
			np.save(file_name, sudoku_generator.main(level))
	except TypeError as e:
		print(e)
		print("Invald amount to be generated given")
	except ValueError as e:
		print(e)
		print("Invalid sudoku level input given")

def main():
	amount = 100
	levels = ["Insane"]
	for level in levels:
		generate_sudokus(level, amount)

if __name__ == '__main__':
	main()