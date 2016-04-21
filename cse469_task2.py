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
        print data
        self.state_of_partition = self.to_int(data[:2])
        self.beg_head = self.to_int(data[2:4])
        self.beg_sec = self.to_int(data[4:8])
        self.type_par = self.to_int(data[8:10])
        self.end_head = self.to_int(data[10:12])
        self.end_sec = self.to_int(data[12:16])
        self.num_sec_MBR = self.to_int(data[16:24])
        self.num_sec_par = self.to_int(data[24:32])

        print self.num_sec_MBR
        print '-----'

    
    def to_int(self, num):
        if len(num) == 2:
            print 'here @2'
            return int('0x{0}'.format(num), 16)
        elif len(num) == 4:
            print 'here @4'
            a = num[0:2]
            b = num[2:4]
            return int('0x{0}{1}'.format(b, a), 16)
        elif len(num) == 8:
            print 'here @8'
            a = num[0:2]
            b = num[2:4]
            c = num[4:6]
            d = num[6:8]
            return int('0x{0}{1}{2}{3}'.format(c,d,b,a), 16)

class PartitionEntryVBR:
    def __init__(self, data):
        self.ra_beg_sec = -1
        self.bootCode = self.to_int(data[:4])
        self.FAT_name = self.to_int(data[4:20])
        self.byte_per_sec = self.to_int(data[20:24])
        self.sec_per_clus = self.to_int(data[24:26])
        self.ra_size_in_sec = self.to_int(data[26:30])
        self.num_FAT = self.to_int(data[30:32])
        self.num_files_root = self.to_int(data[32:36])
        self.bit16_num_sec = self.to_int(data[36:40])
        self.med_type = self.to_int(data[40:42])
        self.fat_bit16_size_sec = self.to_int(data[42:46])
        self.sec_per_track = self.to_int(data[46:50])
        self.num_heads = self.to_int(data[50:54])
        self.num_sec_b4_start = self.to_int(data[54:62])
        self.bit32_num_sec = self.to_int(data[62:72])
        try:
            self.fat_bit16_size_sec = self.to_int(data[73:78])
        except: pass

    def to_int(self, num):
        if len(num) == 2:
            print 'here @2'
            return int('0x{0}'.format(num), 16)
        elif len(num) == 4:
            print 'here @4'
            a = num[0:2]
            b = num[2:4]
            return int('0x{0}{1}'.format(b, a), 16)
        elif len(num) == 8:
            print 'here @8'
            a = num[0:2]
            b = num[2:4]
            c = num[4:6]
            d = num[6:8]
            return int('0x{0}{1}{2}{3}'.format(c,d,b,a), 16)
    # create function to_hex
    # need to parse incoming data to int
    # instead of casting it throught program
    # become more efficient
    # cleanup code


def BARS():
	print "="*(65)

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
    if type_par == '0x04' or type_par == '0x06':
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
        exit()

        partitions_MBR=[partition1_MBR, partition2_MBR, partition3_MBR, partition4_MBR]

        #///////////////////////////////////////
        #COMMENT THESE OUT TO RUN FASTER
        #///////////////////////////////////////
        #MD5 SHA1 Requirements
        MD5hash = MD5(arguments['FILE'])
        SHA1hash = SHA1(arguments['FILE'])
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
                sz = getVBRsz(to_hex)*2
                beg = 512*partition.beg_sec*2
                end = beg+sz

                tmp = PartitionEntryVBR(binascii.hexlify(content[beg:end]))
                tmp.ra_beg_sec = partition.beg_sec

                partitions_VBR.append(tmp)

    BARS()
    for partition in partitions_MBR:
        type_partition = PartitionTypes[partition.type_par]
        start_sector = partition.beg_sec
        end_sector = partition.end_sec
        size_partition = end_sector - start_sector
        print '({0}) {1}, {2}, {3}'.format(partition.type_par, type_partition, start_sector, size_partition)
    BARS()

    for partition in partitions_VBR:
        # calculate appropriate information
        print '-------'
        print partition.ra_size_in_sec
        ra_end_sec = partition.ra_beg_sec+partition.ra_size_in_sec
        fat_beg_sec = int('0x{0}'.format(ra_end_sec), 16)+1
        fat_end_sec = fat_beg_sec+(int('0x{0}'.format(partition.num_FAT), 16)*int('0x{0}'.format(partition.fat_bit16_size_sec), 16))

        print 'Reserved area:   Start sector: {0} Ending sector: {1} Size: {2} sectors'.format(partition.ra_beg_sec, ra_end_sec, partition.ra_size_in_sec)
        print 'Sectors per cluster: {0} sectors'.format(partition.sec_per_clus)
        print 'FAT area:    Start sector: {0} Ending sector {1}'.format(fat_beg_sec, fat_end_sec)
        print '# of FATs: {0}'.format(partition.num_FAT)
        print 'The size of each FAT: {0} sectors'.format(partition.fat_bit16_size_sec)
        print 'The first sector of cluster 2: {0} sectors'.format(partition.num_sec_b4_start)

if __name__ == '__main__':
	main()

