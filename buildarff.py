import sys
import re
import numpy as np

def feature_extraction():
	if(len(sys.argv)<4):
		twt_sum = 11000
	else: 
		twt_sum = min(int(sys.argv[3])*2,11000)
	# define features
	features = ["First-person-pronouns","Second-person-pronouns","Third-person-pronouns",\
				"Coordinating-conjunctions","Past-tense-verbs","Future-tense-verbs",\
				"Commas","colons-and-semi-colons","Dashes","Parentheses","Ellipses","Common-nouns",\
				"Proper-nouns","Adverbs","wh-words","Modern-slang-acroynms","Words-all-in-upper-case",\
				"Average-length-of-sentences","Average-length-of-tokens","Number-of-sentences","Class"]
	fe = np.array(20*[0])
	# load and open files
	f = open(sys.argv[1],'r')
	print sys.argv[1]
	output = open(sys.argv[2],'a')
	print sys.argv[2]
	# write attributes part to output file
	output.write("@relation tweet_features\n\n")
	for i in range(0,20):
		output.write("@attribute " + features[i] + " numeric\n")
	output.write("@attribute " +features[20]+" {0,4}")
	output.write("\n")
	output.write("@data\n")
	# extract features
	txt_counts = 0
	txt_class = 0
	wordlist = readfiles()
	char_count = 0
	output_line = ""
	flag=1

	while(txt_counts <= twt_sum):
		line = f.readline().rstrip()
		if(re.match(r"<A=[0-4]>",line) or line == ""):
			if(txt_counts!=0 and line!="" or txt_counts==twt_sum):
				# previous tweet ends, process average features and write to files
				fe[17] = fe[17] * 1.0 / fe[19]
				fe[18] = char_count * 1.0 / fe[18]
				for i in range(0,20):
					output_line = output_line + str(fe[i]) + ","
					fe[i] = 0
				output_line = output_line + txt_class
				output.write(output_line + "\n")
				
				output_line=""
				char_count=0
			if(line != ""):
				txt_counts += 1
				txt_class = re.search("[0-4]",line).group()
			elif(txt_counts == twt_sum and line == ""): break
			else: continue
		else:
			fp = wordlist["first_person"]
			expression = "^("+fp+")/|\\s("+fp+")/"
			fe[0] = fe[0] + len(re.findall(expression, line, re.IGNORECASE))
			sp = wordlist["second_person"]
			expression = "^("+sp+")/|\\s("+sp+")/"
			fe[1] = fe[1] + len(re.findall(expression, line, re.IGNORECASE))
			tp = wordlist["third_person"]
			expression = "^("+tp+")/|\\s("+tp+")/"
			fe[2] = fe[2] + len(re.findall(expression, line, re.IGNORECASE))
			fe[3] = fe[3] + len(re.findall(r"/CC\s+", line, re.IGNORECASE))
			fe[4] = fe[4] + len(re.findall(r"/VBD", line, re.IGNORECASE))
			fe[5] = fe[5] + len(re.findall(r"('ll|will|gonna|(going/\w+\s+to))/\w+\s+\w+/VB", line, re.IGNORECASE))
			fe[6] = fe[6] + len(re.findall(r"\s,/,\s+", line))
			fe[7] = fe[7] + len(re.findall(r"[:;]/:", line))
			# 9th feature?? dash??
			fe[8] = fe[8] + len(re.findall(r"~", line))
			# 10th feature?? consider a pair of parenthesis as one? 
			fe[9] = fe[9] + len(re.findall(r"\(/\(", line))
			fe[10] = fe[10] + len(re.findall(r"[.][.][.]+/.", line))
			fe[11] = fe[11] + len(re.findall(r"/NN\s+|/NNS\s+", line, re.IGNORECASE))
			fe[12] = fe[12] + len(re.findall(r"/NNP\s+|/NNPS\s+", line, re.IGNORECASE))
			fe[13] = fe[13] + len(re.findall(r"/RB\s+|/RBR\s+|/RBS\s+", line))
			fe[14] = fe[14] + len(re.findall(r"/WDT\s+|/WP\s+|/WRB\s+|/WP\$\s+", line, re.IGNORECASE))
			slang = wordlist["slang"]
			expression = "^("+slang+")/|\\s("+slang+")/"
			fe[15] = fe[15] + len(re.findall(expression, line, re.IGNORECASE))
			fe[16] = fe[16] + len(re.findall(r"^[A-Z]+[A-Z]+/\w+\s|\s[A-Z]+[A-Z]+/\w+\s",line))
			fe[17] = fe[17] + len(re.findall(r"/[A-Z]+\s",line))
			
			tmp = re.findall(r"^[a-zA-Z0-9_@]+/|\s[a-zA-Z0-9_]+/", line)
			fe[18] = fe[18] + len(tmp)
			#if(fe[18]==0): print line
			fe[19] +=1
			
			line = re.sub(r"/\w+\s",'', line)
			line = re.sub(r"\W",'',line)
			char_count = char_count + len(line)
			
			
		#extract partial training data from both classes
		if (twt_sum!=11000 and txt_counts==(int(twt_sum)/2+1) and flag):
			flag=0
			while txt_class!="4":
				line = f.readline().rstrip()
				if re.match(r"<A=[0-4]>",line):
					txt_class = re.search("[0-4]",line).group()




	f.close()
	output.close()
	print txt_counts
	print twt_sum



def readfiles():
	f1 = open("wordlists/First-person",'r')
	first_person = f1.read().rstrip()
	f1.close()
	f2 = open("wordlists/Second-person",'r')
	second_person = f2.read().rstrip()
	f2.close()
	f3 = open("wordlists/Third-person",'r')
	third_person = f3.read().rstrip()
	f3.close()
	f4 = open("wordlists/Slang",'r')
	slang = f4.read().rstrip()
	f4.close()
	wordlist = {
		"first_person" : re.sub(r"\n","|",first_person), 
		"second_person" : re.sub(r"\n","|",second_person), 
		"third_person" : re.sub(r"\n","|",third_person),
		"slang" : re.sub(r"\n","|",slang)
		}

	return wordlist



if __name__ == '__main__':
    feature_extraction()
