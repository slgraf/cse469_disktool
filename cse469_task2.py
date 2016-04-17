import distorm3
import getopt, sys
import hashlib
import struct

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

