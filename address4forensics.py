"""Usage: address4forensics.py  --partition-start=offset

Options:
	--partition-start=offset
"""
import docopt


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	offset = int(arguments['--partition-start'])
	print offset
