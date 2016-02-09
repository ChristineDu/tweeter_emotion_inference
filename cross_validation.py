def divide_files():
	file_names = ["part1.txt", "part2.txt", "part3.txt", "part4.txt", "part5.txt", \
				"part6.txt", "part7.txt", "part8.txt", "part9.txt", "part10.txt",]
	fin = open("all.arff",'r')
	# cope with non-data lines in the begining
	beginlines = []
	k = 0
	while k < 24:
		beginlines.append(fin.readline())
		k += 1
	# copy 550 data from class 0 to each file
	i = 0
	while i<10:
		fout = open(file_names[i],'a')
		k = 0
		while k < 24:
			fout.write(beginlines[k])
			k += 1
		j = 0
		while j < 550:
			line = fin.readline()
			fout.write(line)
			j += 1
		i += 1
		fout.close()
	# copy 550 data from class 4 to each file
	i = 0
	while i<10:
		fout = open(file_names[i],'a')
		j = 0
		while j < 550:
			line = fin.readline()
			fout.write(line)
			j += 1
		i += 1
		fout.close()
	fin.close()

def combine_files():
	file_names = ["part1.txt", "part2.txt", "part3.txt", "part4.txt", "part5.txt", \
				"part6.txt", "part7.txt", "part8.txt", "part9.txt", "part10.txt",]
	file_names1 = ["train1.txt", "train2.txt", "train3.txt", "train4.txt", "train5.txt", \
				"train6.txt", "train7.txt", "train8.txt", "train9.txt", "train10.txt",]
	# cope with non-data lines in the begining
	beginlines = []
	fin = open(file_names[0],'r')
	k = 0
	while k < 24:
		beginlines.append(fin.readline())
		k += 1
	fin.close()

	# for each output file
	i = 0
	while i < 10:
		fout = open(file_names1[i],'a')
		# write begining lines
		k = 0
		while k < 24:
			fout.write(beginlines[k])
			k += 1
		# open readfiles one by one
		j = 0
		while j < 10:
			if j == i: 
				j += 1
				continue
			fin = open(file_names[j])
			k = 0
			while k < 24:
				fin.readline()
				k += 1
			line = fin.readline()
			while line != "":
				fout.write(line)
				line = fin.readline()
				#print line
			print file_names[j]
			j+=1
			fin.close()
		fout.close()
		print file_names1[i]
		i += 1



if __name__ == '__main__':
    #divide_files()
    combine_files()