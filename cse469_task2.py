import distorm3
import getopt, sys
import hashlib
import struct

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

class PartitionEntry:
    def __init__(self, data):
        self.BootableFlag = struct.unpack("<c", data[:1])[0]
        self.StartCHS0 = struct.unpack("<B", data[1:2])[0]
        self.StartCHS1 = struct.unpack("<B", data[2:3])[0]
        self.StartCHS2 = struct.unpack("<B", data[3:4])[0]
        self.PartitionType = struct.unpack("<c", data[4:5])[0]
        self.EndCHS0 = struct.unpack("<B", data[5:6])[0]
        self.EndCHS1 = struct.unpack("<B", data[6:7])[0]
        self.EndCHS2 = struct.unpack("<B", data[7:8])[0]
        self.StartLBA = struct.unpack("<I", data[8:12])[0]
        self.SizeInSectors = struct.unpack("<i", data[12:16])[0]

class PartitionTable:
    def __init__(self, data):
        self.DiskSignature0 = struct.unpack("<B", data[:1])[0]
        self.DiskSignature1 = struct.unpack("<B", data[1:2])[0]
        self.DiskSignature2 = struct.unpack("<B", data[2:3])[0]
        self.DiskSignature3 = struct.unpack("<B", data[3:4])[0]
        self.Unused = struct.unpack("<H", data[4:6])[0]
        self.Entry0 = PartitionEntry(data[6:22])
        self.Entry1 = PartitionEntry(data[22:38])
        self.Entry2 = PartitionEntry(data[38:54])
        self.Entry3 = PartitionEntry(data[54:70])
        self.Signature = struct.unpack("<H", data[70:72])[0]

