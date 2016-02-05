# CSC401H1 Winter 2016
# Assignment 1 - twtt.py
# Prepares .CSV files containing tweets for later processing by tokenizing and tagging them.

# Group 69 / Samantha Halliday (c6hallid) and Christine (Yuqing) Du (c5duyuqi)

# parameters: <input.csv> <group ID> <output.twt>
# if <group ID> is missing, use whole file

from __future__ import print_function
import sys, re, csv
from itertools import chain
import NLPlib

in_file = ""
out_file = ""
group_id = -1

if 3 <= len(sys.argv) <= 4:
	in_file = sys.argv[1].strip()
	out_file = sys.argv[-1].strip()

	if len(sys.argv) == 4:
		group_id = int(sys.argv[2])
else:
	print("Incorrect parameter format.", file=sys.stderr)
	sys.exit(1)

print("Loading:", in_file)

# open file (normally from /u/cs401/A1/tweets/)

tweetset = []

tagger = NLPlib.NLPlib()

with open(in_file, 'r') as fi:
	num_lines = sum(1 for line in fi)
	fi.seek(0)

	with open(out_file, 'w') as fo:
		scanrange = range(0, num_lines)
		
		fireader = csv.reader(fi, delimiter=",", quotechar='"')

		i = -1
		for in_row in fireader:
			i += 1
			if group_id > 0 \
				and not (i >= 5500 * group_id and i < 5500 * (group_id + 1)) \
				and not (i >= 5500 * group_id + 800000 and i < 5500 * (group_id + 1) + 800000):
					continue

			out_line = in_row[5]
#			print(i)

			# strip HTML tags
			out_line = re.sub(r"\<.+?\>", "", out_line)

			# demunge HTML entities
			out_line = re.sub(r"&gt;", ">", out_line)
			out_line = re.sub(r"&lt;", "<", out_line)
			out_line = re.sub(r"&amp;", "&", out_line)
			out_line = re.sub(r"&quot;", "\"", out_line)

			# particular nuisance: smart quotes
			out_line = re.sub(r"\xef\xbf\xbd", "", out_line)
			out_line = re.sub(r"\u2019", "", out_line)

			# currency symbols
			out_line = re.sub(r"(\$|\c2\a3|\u00a3)", " \\1 ", out_line)

			# pull out parentheses as separate tokens 
			# more likely to be stuck to URLs than other punctuation
			out_line = re.sub(r"(\(|\))", " \\1 ", out_line)

			# remove URLs
			out_line = re.sub(r"http:\/\/.+?( |$)", "", out_line)
			out_line = re.sub(r"https:\/\/.+?( |$)", "", out_line)
			out_line = re.sub(r"ftp:\/\/.+?( |$)", "", out_line)
			out_line = re.sub(r"www\.\/\/.+?( |$)", "", out_line)
			out_line = re.sub(r"[0-9A-z.\-]\.(com|net|org)[0-9A-z.\?\=\&\/]*( |$)", "", out_line)

			# demote hashtags and usernames
			out_line = re.sub(r"@([A-Za-z0-9_]+?)(:|,| |$)", " \\1 \\2", out_line)
			out_line = re.sub(r"#([A-Za-z0-9_]+?)( |\s|:|;,)", " \\1 \\2", out_line)
			out_line = re.sub(r"#([A-Za-z0-9_]+?)#", " \\1 ", out_line)

			# protect against initialisms with periods in them getting messed up
			out_line = re.sub(r"<([A-Za-z]\. ?)+ ", "\\1", out_line)

			# single-word honourifics and abbreviations
			out_line = re.sub(r"(?i)prof\.", " Prof ", out_line)
			out_line = re.sub(r"(?i)mr\.", " Mr ", out_line)
			out_line = re.sub(r"(?i)ms\.", " Ms ", out_line)
			out_line = re.sub(r"(?i)dr\.", " Dr ", out_line)
			out_line = re.sub(r"(?i)capt\.", " Capt ", out_line)
			out_line = re.sub(r"(?i)sr\.", " Sr ", out_line)
			out_line = re.sub(r"(?i)jr\.", " Jr ", out_line)
			out_line = re.sub(r"(?i)([0-9])([ap]m)", "\\1 \\2", out_line) #fix scrunched times

			# line-ending punctuation into tokens
			# and split sentences into separate lines but keep repeated punctuation intact
			out_line = re.sub(r"(\.|\?|\!) +(\.|\?|\!)", "\\1\\2", out_line)
			out_line = re.sub(r"(\.|\?|\!)([^\.\?\!])", "\\1 \n \\2", out_line)
			out_line = re.sub(r"([^\.\?\!])([\.\?\!])", "\\1 \\2", out_line)

			out_line = re.sub(r"\.\.+", "...", out_line) # standardize on 3-period ellipsis

			# whoops - found some emoticons remaining in our sample data

			out_line = re.sub(r" ; +\)", "", out_line)


			# put remaining punctuation and clitics into separate tokens
			out_line = re.sub(r" (\-+)([A-Za-z]+)(\-+) ", " \\2 ", out_line) # cope with -emphasis-
			out_line = re.sub(r" (\*+)([A-Za-z]+)(\*+) ", " \n\\2\n ", out_line) # cope with *emphasis*, assuming emotes

			out_line = re.sub(r"([^\:\;\,\-])([\:\;\,\-]+)", "\\1 \\2 ", out_line)
			
			# clitics

			out_line = re.sub(r"(?i)'s(\s|$)", " 's\\1", out_line)
			out_line = re.sub(r"(?i)s'(\s|$)", "s '\\1", out_line)
			out_line = re.sub(r"(?i)can'?t(\s|$)", "can n't\\1", out_line)
			out_line = re.sub(r"(?i)won'?t(\s|$)", " will n't\\1", out_line)
			out_line = re.sub(r"(?i)shan'?t(\s|$)", " shall n't\\1", out_line)
			out_line = re.sub(r"(?i)dn'?t(\s|$)", "d n't\\1", out_line)
			out_line = re.sub(r"(?i)lln'?t(\s|$)", "ll n't\\1", out_line)
			out_line = re.sub(r"(?i)'ll(\s|$)", " 'll\\1", out_line)
			out_line = re.sub(r"(?i)'d(\s|$)", " 'd\\1", out_line)
			out_line = re.sub(r"(?i)(\s|^)hed(\s|$)", "\\1he 'd\\2", out_line) #gambling that sheds are a popular conversation topic?
			out_line = re.sub(r"(?i)(\s|^)theyd(\s|$)", "\\1they 'd\\2", out_line)
			out_line = re.sub(r"(?i)dn'?t(\s|$)", "d n't\\1", out_line)
			out_line = re.sub(r"(?i)in'(\s|$)", "ing\\1", out_line)
			out_line = re.sub(r"(?i)(\s|^)ain'?t(\s|$)", "\\1be not\\2", out_line) # ungrammatical but could be worse
			out_line = re.sub(r"(?i)(\s|^)'?tis(\s|$)", "\\1it is\\2", out_line)
			out_line = re.sub(r"(?i)(\s|^)'?twas(\s|$)", "\\1it was\\2", out_line)
			out_line = re.sub(r"(?i)(\s|^)i'?m(\s|$)", "\\1I 'm\\2", out_line)

			# stupid human tricks

			out_line = re.sub(r"([A-Za-z])\1\1+", "\\1", out_line) # trim 3+ repeats down to 1 letter (more likely than 2)

			# tag POS

			out_lines = out_line.split('\n')
			for j in range(len(out_lines)):
				lin = out_lines[j].split()
				tags = tagger.tag(lin)
				for k in range(len(lin)):
					lk = lin[k]
					tk = tags[k]

					if re.match(r"[\!\.\?]+", lk):
						tk = "."
					
					lin[k] = lk + "/" + tk
				out_lines[j] = " ".join(lin)

			# prefix <A=#> mood indicator
			out_line = "<A=" + in_row[0] + ">\n" + "\n".join(out_lines)
			
			print(out_line, file=fo)

print("Translation complete.")
