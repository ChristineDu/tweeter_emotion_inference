# Cross validation for task 3

from scipy import stats

def divide_files():
	file_names = ["part1.arff", "part2.arff", "part3.arff", "part4.arff", "part5.arff", \
				"part6.arff", "part7.arff", "part8.arff", "part9.arff", "part10.arff",]
	fin = open("all.arff",'r')
	# cope with non-data lines in the begining
	beginlines = []
	for k in range(0,25):
		beginlines.append(fin.readline())
	# copy 550 data from class 0 to each file
	for i in (0,10):
		fout = open(file_names[i],'a')
		for k in range(0,25):
			fout.write(beginlines[k])
		for j in range(0,550):
			line = fin.readline()
			fout.write(line)
		fout.close()
	# copy 550 data from class 4 to each file
	for i in (0,10):
		fout = open(file_names[i],'a')
		for j in range(0,550):
			line = fin.readline()
			fout.write(line)
		fout.close()
	fin.close()

def combine_files():
	file_names = ["part1.arff", "part2.arff", "part3.arff", "part4.arff", "part5.arff", \
				"part6.arff", "part7.arff", "part8.arff", "part9.arff", "part10.arff",]
	file_names1 = ["train1.arff", "train2.arff", "train3.arff", "train4.arff", "train5.arff", \
				"train6.arff", "train7.arff", "train8.arff", "train9.arff", "train10.arff",]
	# cope with non-data lines in the begining
	beginlines = []
	fin = open(file_names[0],'r')
	for k in range(0,25):
		beginlines.append(fin.readline())
	fin.close()

	# for each output file
	for i in range(0,10):
		fout = open(file_names1[i],'a')
		# write begining lines
		for k in range(0,25):
			fout.write(beginlines[k])
		# open readfiles one by one
		for j in range(0,10):
			if j == i: 
				j += 1
				continue
			fin = open(file_names[j])
			for k in range(0,25):
				fin.readline()
			line = fin.readline()
			while line != "":
				fout.write(line)
				line = fin.readline()
				#print line
			print file_names[j]
			fin.close()
		fout.close()
		print file_names1[i]

def calculate():
	fin = open("record1.txt",'r')
	fout = open("output3.4.txt",'a')
	for x in range(0,30):
		line = fin.readline()
		a = [int(n) for n in line.split(" ")]
		accuracy = (a[0] + a[3]) * 1.0 / (a[0] + a[1] + a[2] +a[3])
		precision1 = a[0] * 1.0 / (a[0] + a[2])
		precision2 = a[3] * 1.0 / (a[1] + a[3])
		recall1 = a[0] * 1.0 / (a[0] + a[1])
		recall2 = a[3] * 1.0 / (a[2] + a[3])
		b = str(accuracy)+"\t"+str(precision1)+"\t"+str(precision2)+"\t"+str(recall1)+"\t"+str(recall2) +"\n"
		fout.write(b)
	fin.close()
	fout.close()

def acurracy_comp():
	fin = open("output3.4.txt",'r')
	nb = []
	svm = []
	dt = []
	for x in range(0,10):
		line = fin.readline()
		a = [float(n) for n in line.split("\t")]
		svm.append(a[0])
	for y in range(0,10):
		line = fin.readline()
		a = [float(n) for n in line.split("\t")]
		nb.append(a[0])
	for z in range(0,10):
		line = fin.readline()
		a = [float(n) for n in line.split("\t")]
		dt.append(a[0])
	svm_nb = stats.ttest_rel(svm, nb)
	nb_dt = stats.ttest_rel(nb, dt)
	svm_dt = stats.ttest_rel(svm, dt)
	print svm_nb
	print nb_dt
	print svm_dt











if __name__ == '__main__':
    #divide_files()
    #combine_files()
    calculate()
    acurracy_comp()
