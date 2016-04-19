# uses python 2.7.11
"""
Usage: cse469_task2.py FILE
"""

import sys
import hashlib
import struct
import binascii
import docopt

# global variables
global EXECUTABLE_CODE_MBR, FIRST_PARTITION_MBR, SECOND_PARTITION_MBR, THIRD_PARTITION_MBR, FOURTH_PARTITION_MBR, BOOT_SIG_MBR

PartitionTypes = { 
    "0x00":"Empty",
    "0x01":"DOS 12-bit FAT",
    "0x04":"DOS 16-bit FAT for partitions larger than 32 MB",
    "0x05":"Extended partition",
    "0x06":"DOS 16-bit FAT for partitions larger than 32 MB",
    "0x07":"NTFS",
    "0x08":"AIX bootable partition",
    "0x09":"AIX data partition",
    "0x0b":"DOS 32-bit FAT",
    "0x0c":"DOS 32-bit FAT for 13 support",
    "0x17":"Hidden NTFS partition",
    "0x1b":"Hidden FAT32 partition",
    "0x1e":"Hidden VFAT partition",
    "0x3c":"Partition Magic recovery partition",
    "0x66":"Novell partition",
    "0x67":"Novell partition",
    "0x68":"Novell partition",
    "0x69":"Novell partition",
    "0x81":"Linux",
    "0x82":"Solaris x86 or Linux Swap",
    "0x83":"Linux native file system",
    "0x86":"FAT16 volum/stripe set (Windows NT)",
    "0x87":"High Performance File System",
    "0xa5":"FreeBSD and BSD/386",
    "0xa6":"OpenBSD",
    "0xa9":"NetBSD",
    "0xc7":"Corrupted NTFS volume/stripe set",
    "0xeb":"BeOS"
}

class PartitionEntryMBR:
	def __init__(self, data):   
	    self.state_of_partition = data[:2]
	    self.beg_head = data[2:4]
	    self.beg_sec = data[4:8]
	    self.type_par = data[8:10]
	    self.end_head = data[10:12]
	    self.end_sec = data[12:16]
	    self.num_sec_MBR = data[16:24]
	    self.num_sec_par = data[24:32]
        # self.fat16_32 = True/False

class PartitionEntryVBR:
	def __init__(self, data):
		self.bootCode = data[:4]
		self.FAT_name = data[4:20]
		self.byte_per_sec = data[20:24]
		self.sec_per_clus = data[24:26]
		self.size_in_sec = data[26:30]
		self.num_FAT = data[30:32]
		self.num_files_root = data[32:36]
		self.bit16_num_sec = data[36:40]
		self.med_type = data[40:42]
		self.bit16_size_sec = data[42:46]
		self.sec_per_track = data[46:50]
		self.num_heads = data[50:54]
		self.num_sec_b4_start = data[54:62]
		self.bit32_num_sec = data[62: 72]

#takes in filename, opens and parses through it
def MD5(filename):
	hashcode = hashlib.new("MD5")
	with open(filename, "rb") as file:
		for part in iter(lambda: file.read(4096), b""):
			hashcode.update(part)
	return hashcode.hexdigest()

#takes in filename, opens and parses through it
def SHA1(filename):
	hashcode = hashlib.new("SHA1")
	with open(filename, "rb") as file:
		for part in iter(lambda: file.read(4096), b""):
			hashcode.update(part)
	return hashcode.hexdigest()

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
		EXECUTABLE_CODE_MBR = binascii.hexlify(content[0:446])
		FIRST_PARTITION_MBR = binascii.hexlify(content[446:462])
		SECOND_PARTITION_MBR = binascii.hexlify(content[462:478])
		THIRD_PARTITION_MBR = binascii.hexlify(content[478:494])
		FOURTH_PARTITION_MBR = binascii.hexlify(content[494:510])
		BOOT_SIG_MBR = binascii.hexlify(content[510:512])

	partition1_MBR = PartitionEntry(FIRST_PARTITION)
	partition2_MBR = PartitionEntry(SECOND_PARTITION)
	partition3_MBR = PartitionEntry(THIRD_PARTITION)
	partition4_MBR = PartitionEntry(FOURTH_PARTITION)

	partitions=[partition1_MBR, partition2_MBR, partition3_MBR, partition4_MBR]

	for partition in partitions:
		to_hex='0x{0}'
		type_partition = PartitionTypes[to_hex.format(partition.type_par)]
		start_sector = int(to_hex.format(partition.beg_sec), 16)
		end_sector = int(to_hex.format(partition.end_sec), 16)
		size_partition = end_sector - start_sector
		print '({0}) {1}, {2}, {3}'.format(partition.type_par, type_partition, start_sector, size_partition)

    for partition in partitions:
        # calculate apporpriate information
        # print 'Reserved area:   Start sector: {0} Ending sector: {1} Size: {2} sectors'.format(partition.beg_sec, partition.end_sec, partition.sz)
        # print 'Sectors per cluster: {0} sectors'.format(partition.)
        # print 'FAT area:    Start sector: {0} Ending sector{1}'.format()
        # print '# of FATs: {0}'.format(partition.)
        # print 'The size of each FAT: {0} sectors'.format(partition.)
        # print 'The first sector of cluster 2: {0} sectors'.format()













