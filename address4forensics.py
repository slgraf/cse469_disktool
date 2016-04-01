# project imports
import argparse
import os

# cmd=[]

# put at end of code
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-L', '--logical')
	parser.add_argument('-P', '--physical')
	parser.add_argument('-C', '--cluster')
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()
	# parser.add_argument()

	args = parser.parse_args()
	print args
