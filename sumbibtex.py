#!/usr/bin/env python3.11
import bibtexparser as bt
import sys, re

def parseBibtex(b_name, b_type=None):
	# read file
	with open(b_name) as b:
		match b_type:
			case 'str':
				b_data = bt.loads(b.read())
			case _:
				b_data = bt.load(b)
	b_dict = b_data.entries[0]

	# for j in b_dict: print(j) # debugging

	# create output string
	retrieve = lambda k: b_dict.get(k,f'No {k}')
	out_s = f"{retrieve('author')} ({retrieve('year')}). {retrieve('title')}. {retrieve('journal')}, {retrieve('doi')}"

	# clean spacing, punctuation, random characters
	return out_s

if __name__ == '__main__':
	if len(sys.argv) > 2:
		print(parseBibtex(sys.argv[1], sys.argv[2]))
	else:
		print(parseBibtex(sys.argv[1]))