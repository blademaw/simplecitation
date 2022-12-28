#!/usr/bin/env python3.11
import bibtexparser as bt
from enum import Enum
import sys, re, os, rispy

# defining enums
FILETYPE = Enum('FileType', 'bibtex ris')

def formatRis(c_dict):
	# format authors
	if len(c_dict['authors']) == 1:
		temp = c_dict['authors'][0].split(', ')
		c_dict['author'] = f"{temp[1]} {temp[0]}"
	else:
		filler = " and " if len(c_dict['authors']) == 2 else ", "
		c_dict['author'] = filler.join([f"{i[1]} {i[0]}" for i in list(map(lambda s: s.split(', '), c_dict['authors']))])

	# semantic corrections
	c_dict['title'] = c_dict.get('primary_title') if c_dict.get('primary_title') is not None else c_dict.get('title')
	c_dict['journal'] = c_dict['journal_name']

	return c_dict

def getStringType(f_name, ext, s):
	# print(s)
	if any([symbol in s.lstrip(' \n').split('\n')[0] for symbol in ['@', '{']]):
		# print(bt.loads(s).entries[0])
		return FILETYPE.bibtex
	elif s.lstrip(' \n')[:2] == 'TY':
		return FILETYPE.ris
	raise ValueError(f"Cannot read contents of file with extension '{ext}' — if .bib or .ris ensure file contents are correct.")


def getFileData(f_name, str_type=None, f_type=None):
	ext = f_name.split('.')[-1]
	c_dict = None

	with open(f_name) as file:
		match ext:
			case 'bib':
				c_dict = bt.load(file).entries[0]
				f_type = FILETYPE.bibtex
			case 'ris':
				c_dict = formatRis(rispy.load(file)[0])
				f_type = FILETYPE.ris
			case _:
				# assume string; switch on filetype
				try:
					s = file.read()
				except OSError:
					raise ValueError(f"Cannot read file {f_name}.")
				f_type = getStringType(f_name, ext, s)

				match f_type:
					# if string passed correctly, read file accordingly
					case FILETYPE.bibtex:
						c_dict = bt.loads(s).entries[0]
					case FILETYPE.ris:
						c_dict = formatRis(rispy.loads(s)[0])
					case _:
						raise ValueError(f"Type of contents in {f_name} not recognized.")
				
				# raise ValueError(f"Extension {ext} not recognized.")

	return c_dict

def parseCitation(f_name, str_type=None):
	assert os.path.exists(f_name), f"Path {f_name} to file does not exist."

	# obtain file data
	c_dict = getFileData(f_name, str_type)
	assert c_dict is not None, "Could not obtain data from file."

	# format output string
	retrieve = lambda k: c_dict.get(k,f'No {k}')
	out_s = f"{retrieve('author')} ({retrieve('year')}). {retrieve('title')}. {retrieve('journal')}, {retrieve('doi')}"

	# TODO: clean spacing, punctuation, random characters
	return out_s

if __name__ == '__main__':
	if len(sys.argv) > 2:
		print(parseCitation(sys.argv[1], sys.argv[2]))
	else:
		print(parseCitation(sys.argv[1]))