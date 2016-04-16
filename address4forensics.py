"""
Usage:
	address4forensics.py <files>
Options:
	-L --logical	Calculate the logical address from either
			the cluster address or the physical address.
			Either -c or -p must be given.
	-P --physical	Calculate the physical address from either
			the cluster address or the physical address.
			Either -c or -l must be given.
	-C --cluster	Calculate the cluster address from either
			the cluster address or the physical address.
			Either -l or -p must be given.
	-b OFFSET --partition-start=OFFSET
"""
import docopt


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	print arguments
