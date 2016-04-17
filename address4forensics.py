"""Usage: address4forensics.py  -L | --logical [-b OFFSET | --partition-start=offset] 
			
		  address4forensics.py  -P | --physical [-b OFFSET | --partition-start=offset]
		  	 [[-l ADDRESS | --logical-known=address] | [[-c ADDRESS | --clusterknown=address] [
			 -k SECTORS | --cluster-size=sectors] [-r SECTORS | --reserved=sectors] [
			 -t TABLES | --fat-tables=tables] [-f SECTORS | --fat-length=sectors]]]
		  address4forensics.py  -C | --cluster [-b OFFSET | --partition-start=offset]
		  	 [[-l ADDRESS | --logical-known=address] | [-p ADDRESS | --physical-known=address]]

Options:
	-L, --logical	:Calculate the logical address from either
			the cluster address or the physical address.
			Either -c or -p must be given.
	-P, --physical	:Calculate the physical address from either
			the cluster address or the physical address.
			Either -c or -l must be given.
	-C, --cluster	:Calculate the cluster address from either
			the cluster address or the physical address.
			Either -l or -p must be given.
	-b --partition-start=offset
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

#[[-p ADDRESS | --physical-known=address] | [[-c ADDRESS | --cluster-known=address]
#			 [-k SECTORS | --cluster-size=sectors] [-r SECTORS | --reserved=sectors]
#			 [-t TABLES | --fat-tables=tables] [-f SECTORS | --fat-length=sectors]]]
			 
import docopt

if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)

#beginning of --logical section of arguments
	if arguments["--logical"]:
		if arguments['--partition-start']:
			offset = int(arguments['--partition-start'])
			print(offset)
			# if arguments['--physical-known']:
			# 	phy_address = int(arguments['--physical-known'])
			# 	print(phy_address)

			# elif arguments['--cluster-known']:
			# 	clus_address = int(arguments['--cluster-known'])
			# 	if arguments['--cluster-size']:
			# 		sec_per_clus = int(arguments['--cluster-size'])
			# 		if arguments['--reserved']:
			# 			reser_sec = int(arguments['-reserved'])
			# 			if arguments['--fat-tables']:
			# 				FAT_tables = int(arguments['-fat-tables'])
			# 				if arguments['--fat-length']:
			# 					len_of_FAT = int(arguments['--fat-length'])
			# 					print(len_of_FAT)
	elif arguments["-L"]:
		if arguments['-b']:
			offset = int(arguments['-b'])
			print(offset)
			# if arguments['-p']:
			# 	phy_address = int(arguments['-p'])
			# 	print(phy_address)

#beginning of --physical section of arguments
	elif arguments["--physical"]:
		if arguments['--partition-start']:
			offset = int(arguments['--partition-start'])
			if arguments['--logical-known']:
				log_address = int(arguments['--logical-known'])
				print(log_address)

			elif arguments['--cluster-known']:
				clus_address = int(arguments['--cluster-known'])
				if arguments['--cluster-size']:
					sec_per_clus = int(arguments['--cluster-size'])
					if arguments['--reserved']:
						reser_sec = int(arguments['-reserved'])
						if arguments['--fat-tables']:
							FAT_tables = int(arguments['-fat-tables'])
							if arguments['--fat-length']:
								len_of_FAT = int(arguments['--fat-length'])
								print(len_of_FAT)

#beginning of --cluster section of arguments
	elif arguments["--cluster"]:
		if arguments['--partition-start']:
			offset = int(arguments['--partition-start'])
			if arguments['--logical-known']:
				log_address = int(arguments['--logical-known'])
				print(log_address)
			elif arguments["--physical-known"]:
				phy_address = int(arguments['--physical-known'])
				print(phy_address)

	#if arguments["-P"]

	#address4forensics.py  --logical [-b OFFSET | --partition-start=offset]