"""
Usage: cse469_task2.py FILE
"""

import sys
import hashlib
import struct
import binascii
import docopt

# global variables
global EXECUTABLE_CODE, FIRST_PARTITION, SECOND_PARTITION, THIRD_PARTITION, FOURTH_PARTITION, BOOT_SIG

PartitionTypes = { 
    00:"Empty",
    01:"DOS 12-bit FAT",
    04:"DOS 16-bit FAT for partitions larger than 32 MB",
    05:"Extended partition",
    06:"DOS 16-bit FAT for partitions larger than 32 MB",
    07:"NTFS",
    08:"AIX bootable partition",
    09:"AIX data partition",
    0b:"DOS 32-bit FAT",
    0c:"DOS 32-bit FAT for 13 support",
    17:"Hidden NTFS partition",
    1b:"Hidden FAT32 partition",
    1e:"Hidden VFAT partition",
    3c:"Partition Magic recovery partition",
    66:"Novell partition",
    67:"Novell partition",
    68:"Novell partition",
    69:"Novell partition",
    81:"Linux",
    82:"Solaris x86 or Linux Swap",
    83:"Linux native file system",
    86:"FAT16 volum/stripe set (Windows NT)",
    87:"High Performance File System",
    a5:"FreeBSD and BSD/386",
    a6:"OpenBSD",
    a9:"NetBSD",
    c7:"Corrupted NTFS volume/stripe set"
    eb:"BeOS"
}

class PartitionEntry(self, data):
	def __init__(self):   
	    self.state_of_partition = data[:1]
	    self.beg_head = data[1:2]
	    self.beg_sec = data[2:4]
	    self.type_par = PartitionType[data[4:5]]
	    self.end_head = data[5:6]
	    self.end_sec = data[6:8]
	    self.num_sec_MBR = data[8:12]
	    self.num_sec_par = data[12:16]

def starting_sec(data):
    hex1 = data[:2]
    hex2 = data[2:4]
    hex3 = data[4:6]
    hex4 = data[6:8]
    final_hex = hex4+hex3+hex2+hex1
    scale = 16
    num_of_bits2 = len(final_hex)*4
    binary_rep2 = ( bin(int(final_hex, scale))[2:]).zfill(num_of_bits2)
    starting_sector = int(binary_rep2, 2)

def size_of_par(data):
    hex1 = data[:2]
    hex2 = data[2:4]
    hex3 = data[4:6]
    hex4 = data[6:8]
    final_hex = hex4+hex3+hex2+hex1
    scale = 16
    num_of_bits2 = len(final_hex)*4
    binary_rep2 = ( bin(int(final_hex, scale))[2:]).zfill(num_of_bits2)
    size_par = int(binary_rep2, 2)


if __name__ == '__main__':
	arguments = docopt.docopt(__doc__)

	with open(arguments['FILE'], 'rb') as f:
		content=f.read()
		EXECUTABLE_CODE = binascii.hexlify(content[0:446])
		FIRST_PARTITION = binascii.hexlify(content[446:462])
		SECOND_PARTITION = binascii.hexlify(content[462:478])
		THIRD_PARTITION = binascii.hexlify(content[478:494])
		FOURTH_PARTITION = binascii.hexlify(content[494:510])
		BOOT_SIG = binascii.hexlify(content[510:512])

	partition1 = PartitionEntry(FIRST_PARTITION)
	partition2 = PartitionEntry(SECOND_PARTITION)
	partition3 = PartitionEntry(THIRD_PARTITION)
	partition4 = PartitionEntry(FOURTH_PARTITION)
	print(partition1.type_par)
