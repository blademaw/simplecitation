#!/usr/bin/env python3.11
import bibtexparser as bt
import sys, re, rispy

def formatRis(c_dict):
	# format authors
	filler = " and " if len(c_dict['authors']) == 2 else ", "
	c_dict['author'] = filler.join([f"{i[1]} {i[0]}" for i in list(map(lambda s: s.split(', '), c_dict['authors']))])

	# semantic corrections
	c_dict['title'], c_dict['journal'] = c_dict['primary_title'], c_dict['journal_name']

	return c_dict

def parseCitation(f_name, str_type=None):
	# read file
	with open(f_name) as file:
		match str_type:
			# if string passed (as .txt), read file accordingly
			case 'bibtex':
				c_dict = bt.loads(file.read()).entries[0]
			case 'ris':
				c_dict = formatRis(rispy.loads(file.read())[0])
			
			case None:
				# load file as bibtex/ris
				ext = f_name.split('.')[-1]
				match ext:
					case 'bib':
						c_dict = bt.load(file).entries[0]
					case 'ris':
						c_dict = formatRis(rispy.load(file)[0])
					case _:
						raise ValueError(f"Extension {ext} not recognized.")
			case _:
				raise ValueError(f"String type {str_type} not recognized.")
	
	# print(c_dict) # debugging

	# output string
	retrieve = lambda k: c_dict.get(k,f'No {k}')
	out_s = f"{retrieve('author')} ({retrieve('year')}). {retrieve('title')}. {retrieve('journal')}, {retrieve('doi')}"

	# clean spacing, punctuation, random characters
	return out_s

if __name__ == '__main__':
	if len(sys.argv) > 2:
		print(parseCitation(sys.argv[1], sys.argv[2]))
	else:
		print(parseCitation(sys.argv[1]))