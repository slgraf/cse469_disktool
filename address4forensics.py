"""
Usage: 	address4forensics.py  -L [-b offset] [-B [-s bytes]] [-p address] [-c address -k sectors -r sectors -t tables -f sectors]
	address4forensics.py -P [-b offset] [-B [-s bytes]] [-l address] [-c address -k sectors -r sectors -t tables -f sectors]
	address4forensics.py -C [-b offset] [-B [-s bytes]] [-l address] [-p address]
	
-h, --help
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

def cmd_logical():
	if arguments['--physical-known']:
		p_address = int(arguments['--physical-known'])
		offset = 0
		if arguments['--partition-start'] is not None:
			offset = int(arguments['--partition-start'])
		if arguments['--byte-address']:
			sector_sz = 512
			if arguments['--sector-size'] is not None:
				sector_sz = int(arguments['--sector-size'])
			return sector_sz*(p_address-offset)
		return p_address-offset

	elif arguments['--cluster-known'] and arguments['--cluster-size'] and arguments['--reserved'] and arguments['--fat-tables'] and arguments['--fat-length']:
		c_address = int(arguments['--cluster-known'])
		c_sz = int(arguments['--cluster-size'])
		reserved_sec = int(arguments['--reserved'])
		fat_tables = int(arguments['--fat-tables'])
		fat_length = int(arguments['--fat-length'])
		offset=0

		if arguments['--byte-address']:
			offset = 512
			if arguments['--sector-size']:
				offset = int(arguments['--sector-size'])

		p_address = (c_address-2)*c_sz+reserved_sec+(fat_tables*fat_length)+offset
		return p_address-offset

def cmd_physical():
	if arguments['--logical-known']:
		address=int(arguments['--logical-known'])
		offset=0
		if arguments['--partition-start'] is not None:
			offset=int(arguments['--partition-start'])
		if arguments['--byte-address']:
			sector_sz = 512
			if arguments['--sector-size'] is not None:
				sector_sz = int(arguments['--sector-size'])
			return sector_sz*(p_address-offset)
		return address

	elif arguments['--cluster-known'] and arguments['--cluster-size'] and arguments['--reserved'] and arguments['--fat-tables'] and arguments['--fat-length']:
		c_address = int(arguments['--cluster-known'])
		c_sz = int(arguments['--cluster-size'])
		reserved_sec = int(arguments['--reserved'])
		fat_tables = int(arguments['--fat-tables'])
		fat_length = int(arguments['--fat-length'])
		offset=0

		if arguments['--partition-start']:
			offset=int(arguments['--partition-start'])

		p_address = (c_address-2)*c_sz+reserved_sec+(fat_tables*fat_length)+offset
		return p_address
	
def cmd_cluster():
	address = None
	sector_sz = 1
	offset = 0
	if arguments['--physical-known']:
		address=int(arguments['--physical-known'])
	elif arguments['logical-known']:
		address=int(arguments['--logical-known'])
	if arguments['--byte-address']:
		sector_sz = 512
		if arguments['--sector-size']:
			sector_sz = int(arguments['--sector-size'])
	if arguments['--partition-start']:
		offset = int(arguments['--partition-start'])
	return (address-offset)*sector_sz


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)

	resp = -1
	if arguments['--logical']:
		if arguments['--cluster-known'] or arguments['--physical-known']:
			resp = cmd_logical()
	elif arguments['--cluster']:
		if arguments['--logical-known'] or arguments['--physical-known']:
			resp = cmd_cluster()
	elif arguments['--physical']:
		if arguments['--logical-known'] or arguments['--cluster-known']:
			resp = cmd_physical()

	print resp

