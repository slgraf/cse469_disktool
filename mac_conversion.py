#uses Python 3.5 with Anaconda
#Anaconda not required for this code, but Python 3.5 is

import os
import sys

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

#converts hex to date, need to find the format for taking in inputs
#this input comes in from the command line
def hex_to_date(hex1):
	hex1_1 = hex1[2:4]
	hex1_2 = hex1[4:6]
	my_hex = hex1_2+hex1_1

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
def hex_to_time(hex2):
	hex2_1 = hex2[2:4]
	hex2_2 = hex2[4:6]
	my_hex2 = hex2_2+hex2_1
	
	scale = 16
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

#hex_to_time("0x53f6")
#hex_to_date("0x3a81")

#main code
list_of_arg = (sys.argv)

if list_of_arg[1] == "-T":
	if list_of_arg[2] == "-h":
		hex_to_time(list_of_arg[3])
	elif list_of_arg[2] == "-f":
		f = open(list_of_arg[3], 'r')
		my_hex3 = f.read()
		hex_to_time(my_hex3)
elif list_of_arg[1] == "-D":
	if list_of_arg[2] == "-h":
		hex_to_date(list_of_arg[3])
	elif list_of_arg[2] == "-f":
		f = open(list_of_arg[3], 'r')
		my_hex3 = f.read()
		hex_to_time(my_hex3)
