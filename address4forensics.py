"""Usage: address4forensics.py  -L [-p address] [-c address]
	
-L, --logical
-P, --physical
-C, --cluster
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
	if arguments['--physical-known']:
		print '_physical-known'
		print int(arguments['--partition-known'])
	elif arguments['--cluster-known'] and arguments['--cluster-size'] and arguments['--reserved'] and arguments['--fat-tables'] and arguments['--fat-length']:
		pass



if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)
	if debug:
		print 'arguments:\n{0}'.format(arguments)
	if arguments['--logical']:
		print '_logical'
		if arguments['--cluster-known'] or arguments['--physical-known']:
			print '_cmd_logical'
			cmd_logical()

























