#!/usr/local/bin/python
# uses python 2.7.11
"""
Usage: cse469_task2.py FILE
"""

import sys
import hashlib
import struct
import binascii
import docopt
import os

# global variables
global EXECUTABLE_CODE_MBR, FIRST_PARTITION_MBR, SECOND_PARTITION_MBR, THIRD_PARTITION_MBR, FOURTH_PARTITION_MBR, BOOT_SIG_MBR

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
    0xc7:"Corrupted NTFS volume/stripe set",
    0xeb:"BeOS"
}

class PartitionEntryMBR:
    def __init__(self, data):
        self.name = ''
        self.state_of_partition = self.to_int(data[:2])
        self.beg_head = self.to_int(data[2:4])
        self.beg_sec = self.to_int(data[4:8])
        self.type_par = self.to_int(data[8:10])
        self.end_head = self.to_int(data[10:12])
        self.end_sec = self.to_int(data[12:16])
        self.num_sec_MBR = self.to_int(data[16:24])
        self.num_sec_par = self.to_int(data[24:32])

    def to_int(self, num):
        if len(num) == 2:
            return int('0x{0}'.format(num), 16)
        elif len(num) == 4:
            a = num[0:2]
            b = num[2:4]
            return int('0x{0}{1}'.format(b,a), 16)
        elif len(num) == 8:
            a = num[0:2]
            b = num[2:4]
            c = num[4:6]
            d = num[6:8]
            return int('0x{0}{1}{2}{3}'.format(d,c,b,a), 16)

class PartitionEntryVBR:
    def __init__(self, data):
        mbr = None
        self.ra_beg_sec = -1
        self.bootCode = self.to_int(data[:6])
        self.FAT_name = self.to_int(data[6:22])
        self.byte_per_sec = self.to_int(data[22:26])
        self.sec_per_clus = self.to_int(data[26:28])
        self.ra_size_in_sec = self.to_int(data[28:32])
        self.num_FAT = self.to_int(data[32:34])
        self.num_files_root = self.to_int(data[34:38])
        self.bit16_num_sec = self.to_int(data[38:42])
        self.med_type = self.to_int(data[42:44])
        self.fat_bit16_size_sec = self.to_int(data[44:48])
        self.sec_per_track = self.to_int(data[48:52])
        self.num_heads = self.to_int(data[52:56])
        self.num_sec_b4_start = self.to_int(data[56:64])
        self.bit32_num_sec = self.to_int(data[64:72])
        if self.fat_bit16_size_sec == 0:
            self.fat_bit16_size_sec = self.to_int(data[72:80])

    def to_int(self, num):
        if len(num) == 2:
            return int('0x{0}'.format(num), 16)
        elif len(num) == 4:
            a = num[0:2]
            b = num[2:4]
            return int('0x{0}{1}'.format(b, a), 16)
        elif len(num) == 8:
            a = num[0:2]
            b = num[2:4]
            c = num[4:6]
            d = num[6:8]
            return int('0x{0}{1}{2}{3}'.format(d,c,b,a), 16)

def BARS():
	print "="*(50)

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
    return starting_sector

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
    return size_par

def getVBRsz(type_par):
    if type_par == 0x04 or type_par == 0x06:
        return 36
    else: 
        return 512

def main():
    arguments = docopt.docopt(__doc__)

    partition1_MBR = None
    partition2_MBR = None
    partition3_MBR = None
    partition4_MBR = None

    partitions_MBR = []
    partitions_VBR = []

    with open(arguments['FILE'], 'rb') as f:
        content=f.read()

        EXECUTABLE_CODE_MBR = binascii.hexlify(content[0:446])
        FIRST_PARTITION_MBR = binascii.hexlify(content[446:462])
        SECOND_PARTITION_MBR = binascii.hexlify(content[462:478])
        THIRD_PARTITION_MBR = binascii.hexlify(content[478:494])
        FOURTH_PARTITION_MBR = binascii.hexlify(content[494:510])
        BOOT_SIG_MBR = binascii.hexlify(content[510:512])

        partition1_MBR = PartitionEntryMBR(FIRST_PARTITION_MBR)
        partition2_MBR = PartitionEntryMBR(SECOND_PARTITION_MBR)
        partition3_MBR = PartitionEntryMBR(THIRD_PARTITION_MBR)
        partition4_MBR = PartitionEntryMBR(FOURTH_PARTITION_MBR)

        partition1_MBR.name = 'Partition 0'
        partition2_MBR.name = 'Partition 1'
        partition3_MBR.name = 'Partition 2'
        partition4_MBR.name = 'Partition 3'

        partitions_MBR=[partition1_MBR, partition2_MBR, partition3_MBR, partition4_MBR]

        #///////////////////////////////////////
        #COMMENT THESE OUT TO RUN FASTER
        #///////////////////////////////////////
        #MD5 SHA1 Requirements
        MD5hash = MD5(arguments['FILE'])
        SHA1hash = SHA1(arguments['FILE'])
        print ""
        print "Checksums:"
        BARS()
        print "MD5: {0}".format(MD5hash)
        print ""
        print "SHA1: {0}".format(SHA1hash)

        file_title = arguments['FILE']
        file_title_list = file_title.split('.')
        file_title = file_title_list[0]
        file1 = "MD5-{0}.txt".format(file_title)
        file2 = "SHA1-{0}.txt".format(file_title)
        with open(file1, 'w') as f:
            f.write(MD5hash)
        with open(file2, 'w') as f:
            f.write(SHA1hash)


        for partition in partitions_MBR:
            to_hex = partition.type_par
            if  to_hex == 0x04 or to_hex == 0x06 or to_hex == 0x0b or to_hex == 0x0c:
                # sz = getVBRsz(to_hex)
                beg = 512*(partition.num_sec_MBR)
                end = beg+512

                tmp = PartitionEntryVBR(binascii.hexlify(content[beg:end]))
                tmp.ra_beg_sec = (partition.num_sec_MBR)*512
                tmp.mbr = partition

                partitions_VBR.append(tmp)

    BARS()
    for partition in partitions_MBR:
        type_partition = PartitionTypes[partition.type_par]
        start_sector = partition.num_sec_MBR
        end_sector = partition.num_sec_par
        strHex = "%0.2x" % partition.type_par
        # size_partition = end_sector - start_sector
        print '({0}) {1}, {2}, {3}'.format(strHex, type_partition, str(start_sector).zfill(10), str(end_sector).zfill(10))
    BARS()

    for partition in partitions_VBR:
        # calculate appropriate information
        ra_beg_sec = 0
        ra_end_sec = partition.ra_size_in_sec-1
        fat_beg_sec = ra_end_sec+1
        fat_end_sec = fat_beg_sec+partition.num_FAT*partition.fat_bit16_size_sec-1

        sec_clus2 = 0
        # FAT32
        if partition.mbr.type_par == 0x0b or partition.mbr.type_par == 0x0c:
            sec_clus2 = partition.ra_size_in_sec+(partition.num_FAT*partition.fat_bit16_size_sec)+partition.mbr.num_sec_MBR
        # FAT16
        else:
            sec_clus2 = partition.ra_size_in_sec+(partition.num_FAT*partition.fat_bit16_size_sec)+partition.mbr.num_sec_MBR+partition.num_files_root*32/partition.byte_per_sec

        print '{0}({1}):'.format(partition.mbr.name, PartitionTypes[partition.mbr.type_par])
        print 'Reserved area: Start sector: {0} Ending sector: {1} Size: {2} sectors'.format(ra_beg_sec, ra_end_sec, partition.ra_size_in_sec)
        print 'Sectors per cluster: {0} sectors'.format(partition.sec_per_clus)
        print 'FAT area: Start sector: {0} Ending sector {1}'.format(fat_beg_sec, fat_end_sec)
        print '# of FATs: {0}'.format(partition.num_FAT)
        print 'The size of each FAT: {0} sectors'.format(partition.fat_bit16_size_sec)
        print 'The first sector of cluster 2: {0} sectors'.format(sec_clus2)
        BARS()

if __name__ == '__main__':
	main()

