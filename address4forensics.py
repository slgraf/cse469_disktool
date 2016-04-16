"""Usage: address4forensics.py  -L|-P|-C [-b offset] [-B [-s bytes]] [-l address] [-p address] 
	[-c address -k sectors -r sectors -t tables -f sectors]
	
Options:
	-L, --logical	Calculate the logical address from either
			the cluster address or the physical address.
			Either -c or -p must be given.
	-P, --physical	Calculate the physical address from either
			the cluster address or the physical address.
			Either -c or -l must be given.
	-C, --cluster	Calculate the cluster address from either
			the cluster address or the physical address.
			Either -l or -p must be given.
	-b offset, --partition-start=offset
	-B, --byte-address
	-s bytes, --sector-size=bytes
	-l address, --logical-known=address
	-p address, --physical-known=address
	-c address, --cluster-known=address
	-k sectors, --cluster-size=sectors
	-r sectors, --reserved=sectors
	-t tables, --fat-tables=tables
	-f sectors, --fat-length=sectors
"""
import docopt


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	offset = int(arguments['--partition-start'])
	print offset
