"""
Usage: cse469_task2.py FILE
"""

import sys
import hashlib
import struct
import binascii
import docopt

global EXECUTABLE_CODE, FIRST_PARTITION, SECOND_PARTITION, THIRD_PARTITION, FOURTH_PARTITION, BOOT_SIG

arguments = docopt.docopt(__doc__)

with open(arguments['FILE'], 'rb') as f:
	content=f.read()
	EXECUTABLE_CODE = binascii.hexlify(content[0:446])
	FIRST_PARTITION = binascii.hexlify(content[446:462])
	SECOND_PARTITION = binascii.hexlify(content[462:478])
	THIRD_PARTITION = binascii.hexlify(content[478:494])
	FOURTH_PARTITION = binascii.hexlify(content[494:510])
	BOOT_SIG = binascii.hexlify(content[510:512])


PartitionTypes = { 
    0x00:"Empty",
    0x01:"DOS 12-bit FAT",
    0x04:"DOS 16-bit FAT for partitions larger than 32 MB",
    0x05:"Extended partition",
    0x06:"DOS 16-bit FAT for partitions larger than 32 MB",
    0x07:"NTFS",
    0x08:"AIX bootable partition",
    0x09:"AIX data partition",
    0x0b:"DOS 32-bit FAT",
    0x0c:"DOS 32-bit FAT for 13 support",
    0x17:"Hidden NTFS partition",
    0x1b:"Hidden FAT32 partition",
    0x1e:"Hidden VFAT partition",
    0x3c:"Partition Magic recovery partition",
    0x66:"Novell partition",
    0x67:"Novell partition",
    0x68:"Novell partition",
    0x69:"Novell partition",
    0x81:"Linux",
    0x82:"Solaris x86 or Linux Swap",
    0x83:"Linux native file system",
    0x86:"FAT16 volum/stripe set (Windows NT)",
    0x87:"High Performance File System",
    0xa5:"FreeBSD and BSD/386",
    0xa6:"OpenBSD",
    0xa9:"NetBSD",
    0xc7:"Corrupted NTFS volume/stripe set"
    0xeb:"BeOS"
}

def PartitionEntry(data):   
    state_of_partition = data[:1]
    beg_head = data[1:2]
    beg_sec = data[2:4]
    type_par = data[4:5]
    end_head = data[5:6]
    end_sec = data[6:8]
    num_sec_MBR = data[8:12]
    num_sec_par = data[12:16]

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


