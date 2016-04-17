import sys
import os
import binascii

path='/Users/spencergraf/Desktop/asu_juniour/cse469/prj/cse469_disktool/test_imgs/TestImage1.img'

if os.path.exists(path):
	with open(path, 'rb') as f:
		content=f.read()
		print len(content[0:446])
		print binascii.hexlify(content[0:446])
		print ''
		print binascii.hexlify(content[447:512])
else:
	print 'FileNotFound'