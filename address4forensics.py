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

debug=True

def cmd_logical():
	if arguments['-p'] or arguments ['--physical-known']:
		pass
	elif arguments['-c'] and arguments['-k'] and arguments['-r'] and arguments['-t'] and arguments['-f']:
		pass






if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	if debug:
		print 'arguments:\n{0}'.format(arguments)
	if arguments['-L']:
		if arguments['-c'] or arguments['-p']:
			cmd_logical()
