#!/usr/bin/env python3.11
import bibtexparser as bt
from bibtexparser.bparser import BibTexParser
import bibtexparser.customization as bc
from enum import Enum
import sys, os, rispy

# defining parser for bibtex
BIB_PARSER = BibTexParser()
BIB_PARSER.customization = lambda r: bc.author(r)

# defining enums
FILETYPE = Enum('FileType', 'bibtex ris')

def formatAuthors(c_dict, field='author'):
	if len(c_dict[field]) == 1:
		temp = c_dict[field][0].split(', ')
		c_dict['author'] = f"{temp[1]} {temp[0]}"
	else:
		filler = " and " if len(c_dict[field]) == 2 else ", "
		c_dict['author'] = filler.join([f"{i[1]} {i[0]}" for i in list(map(lambda s: s.split(', '), c_dict[field]))])


def formatRis(c_dict):
	# retrieval function
	retrieve = lambda k: c_dict.get(k,f"No {k.split('_')[0]}")

	# format authors
	formatAuthors(c_dict, 'authors')

	# semantic corrections
	c_dict['title'] = c_dict.get('primary_title') if c_dict.get('primary_title') is not None else retrieve('title')
	c_dict['journal'] = retrieve('journal_name')

	return c_dict


def getStringType(f_name, ext, s):
	if any([symbol in s.lstrip(' \n').split('\n')[0] for symbol in ['@', '{']]):
		return FILETYPE.bibtex
	elif s.lstrip(' \n')[:2] == 'TY':
		return FILETYPE.ris

	if f_name is None:
		raise ValueError(f"Cannot detect format of citation in clipboard.")
	raise ValueError(f"Cannot read contents of file with extension '{ext}' — if .bib or .ris ensure file contents are correct.")


def loadStringData(f_name, f_type, s):
	c_dict = None 

	match f_type:
		# if string passed correctly, read file accordingly
		case FILETYPE.bibtex:
			c_dict = bt.loads(s, parser=BIB_PARSER).entries[0]
			formatAuthors(c_dict)
		case FILETYPE.ris:
			c_dict = formatRis(rispy.loads(s)[0])
		case _:
			raise ValueError(f"Type of contents in {f_name} not recognized.")

	return c_dict


def getFileData(f_name, str_type=None, f_type=None, s=None):
	c_dict = None

	if f_name is None:
		f_type = getStringType(None, None, s)
		c_dict = loadStringData(None, f_type, s)
	else:
		ext = f_name.split('.')[-1]

		with open(f_name) as file:
			match ext:
				case 'bib':
					c_dict = bt.load(file, parser=BIB_PARSER).entries[0]
					formatAuthors(c_dict)
					f_type = FILETYPE.bibtex
				case 'ris':
					c_dict = formatRis(rispy.load(file)[0])
					f_type = FILETYPE.ris
				case _:
					# assume string; switch on filetype
					try:
						s = file.read() if s is None else s
					except OSError:
						raise ValueError(f"Cannot read file {f_name}.")
					f_type = getStringType(f_name, ext, s)
					c_dict = loadStringData(f_name, f_type, s)

	return c_dict


def parseCitation(f_name, str_type=None, s=None):
	if f_name is not None: assert os.path.exists(f_name), f"Path {f_name} to file does not exist."

	# obtain file data
	c_dict = getFileData(f_name, str_type=str_type, s=s)
	assert c_dict is not None, "Could not obtain data from file."

	# format output string
	retrieve = lambda k: c_dict.get(k,f'No {k}')
	out_s = f"{retrieve('author')} ({retrieve('year')}). {retrieve('title')}. {retrieve('journal')}, {retrieve('doi')}"

	# TODO: add cleaning for spacing, punctuation, random characters (encodings gone wrong)
	return out_s


if __name__ == '__main__':
	if len(sys.argv) > 2:
		# text format has been specified
		print(parseCitation(sys.argv[1], sys.argv[2]))
	elif len(sys.argv) == 1:
		# assume citation is in clipboard
		import pyperclip
		print(parseCitation(None, s=pyperclip.paste()))
	else:
		# assume first argument is file path
		print(parseCitation(sys.argv[1]))