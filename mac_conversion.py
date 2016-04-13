import os
import argparse
import datetime as dt

months = { 
1: "Jan",
2: "Feb",
3: "Mar",
4: "Apr",
5: "May",
6: "Jun",
7: "Jul",
8: "Aug",
9: "Sep",
10: "Oct",
11: "Nov",
12: "Dec"
}

#import binascci
#cmd = []

#if __name__ = "__main__":
#	parser = argparse.ArgumentParser()
#	parser.add_argument('-T')
#	parser.add_argument('-D')
#	parser.add_argument('-f')
#	parser.add_argument('-h')
#
#	args = parse.parse_args()
#	args.
#
#converting hex to date?

#converts hex to date, need to find the format for taking in inputs
#this input comes in from the command line
#def hex_to_bin(filename):
my_hex = "3a81"
scale = 16
num_of_bits = len(my_hex)*4
binary_rep = ( bin(int(my_hex, scale))[2:] ).zfill(num_of_bits)

year = binary_rep[0:7]
month = binary_rep[7:11]
day = binary_rep[11:16]

int_year = 1980 + int(year, 2)
int_month = int(month, 2)
int_day = int(day, 2)

print ("Date: ",months[int_month]," ",int_day,", ",int_year)

#moving on to the conversion to time from hex
#this input comes in from a .txt file
my_hex2 = "53f6"
num_of_bits2 = len(my_hex2)*4
binary_rep2 = ( bin(int(my_hex2, scale))[2:]).zfill(num_of_bits2)

hour = binary_rep2[0:5]
minute = binary_rep2[5:11]
second = binary_rep2[11:16]

int_hour = int(hour, 2)
int_minute = int(minute, 2)
int_second = 2*int(second, 2)

if int_hour>12:
	int_hour = int_hour - 12
	print("Time: ", int_hour, ":", int_minute, ":", int_second, "PM")
else:
	print("Time: ", int_hour, ":", int_minute, ":", int_second, "AM")
