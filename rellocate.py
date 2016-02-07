import re
import numpy as np
line_num=0
fo = open("test.twt",'r')
f0 = open("test0.twt",'a')
f4 = open("test4.twt",'a')
f = f0
while line_num<1476:
	line_num+=1
	line = fo.readline()
	if re.match(r"<A=[0-4]>",line):
		txt_class = re.search("[0-4]",line).group()
		if txt_class=="0": f=f0
		elif txt_class=="4": f=f4
		else: f=None
	if f!=None:
		f.write(line)
		print "w"

print "done"





fo.close()
f0.close()
f4.close()