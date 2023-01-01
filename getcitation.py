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
	"""Formats a list of author names into a single string.
	
	Args:
	    c_dict (Dict): Citation dictionary with 'author' field
	    field (str, optional): Field to draw from ('author' initially)
	"""
	if len(c_dict[field]) == 1:
		temp = c_dict[field][0].split(', ')
		c_dict['author'] = f"{temp[1]} {temp[0]}"
	else:
		filler = " and " if len(c_dict[field]) == 2 else ", "
		c_dict['author'] = filler.join([f"{i[1]} {i[0]}" for i in list(map(lambda s: s.split(', '), c_dict[field]))])


def formatRis(c_dict):
	"""Formats a .ris text read-in.
	
	Args:
	    c_dict (Dict): Citation dictionary
	
	Returns:
	    Dict: Updated citation dictionary
	"""
	# retrieval function
	retrieve = lambda k: c_dict.get(k,f"No {k.split('_')[0]}")

	# format authors
	formatAuthors(c_dict, 'authors')

	# semantic corrections
	c_dict['title'] = c_dict.get('primary_title') if c_dict.get('primary_title') is not None else retrieve('title')
	c_dict['journal'] = retrieve('journal_name')

	return c_dict


def getStringType(f_name, ext, s):
	"""Detects whether a string is in .bib or .ris format.
	
	Args:
	    f_name (str): File name citation is read from
	    ext (str): Extension of file
	    s (str): String of file/citation
	
	Returns:
	    Enum: bibtex or ris, depending on type detected
	
	Raises:
	    ValueError: if citation cannot be detected with naive pattern matching
	"""
	if any([symbol in s.lstrip(' \n').split('\n')[0] for symbol in ['@', '{']]):
		return FILETYPE.bibtex
	elif s.lstrip(' \n')[:2] == 'TY':
		return FILETYPE.ris

	if f_name is None:
		raise ValueError(f"Cannot detect format of citation in clipboard.")
	raise ValueError(f"Cannot read contents of file with extension '{ext}' — if .bib or .ris ensure file contents are correct.")


def loadStringData(f_name, f_type, s):
	"""Load data into citation dictionary from file.
	
	Args:
	    f_name (str): File name of citation
	    f_type (Enum): Type of citation format
	    s (str): String of contents of file/citation
	
	Returns:
	    Dict: Citation dictionary
	
	Raises:
	    ValueError: if Enum is not recognized (should never happen)
	"""
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


def getFileData(f_name, f_type, s):
	"""Obtain citation dictionary from supplied file
	
	Args:
	    f_name (str): File name
	    f_type (Enum, optional): File type; default is None signifying clipboard
	    s (str, optional): String of citation, default is None signifying file to be read
	
	Returns:
	    dict: Citation dictionary
	
	Raises:
	    ValueError: if cannot access/read file
	"""
	c_dict = None

	if f_name is None:
		# assume user has data in clipboard
		f_type = getStringType(None, None, s) if f_type is None else f_type
		c_dict = loadStringData(None, f_type, s)
	else:
		ext = f_name.split('.')[-1]

		with open(f_name) as file:
			# try to detect with supplied filetype (takes precedence)
			match f_type:
				case FILETYPE.ris:
					c_dict = formatRis(rispy.load(file)[0])
				case FILETYPE.bibtex:
					c_dict = bt.load(file, parser=BIB_PARSER).entries[0]
					formatAuthors(c_dict)
				case _:
					# otherwise, detect file extension
					match ext:
						case 'bib':
							c_dict = bt.load(file, parser=BIB_PARSER).entries[0]
							formatAuthors(c_dict)
							f_type = FILETYPE.bibtex
						case 'ris':
							c_dict = formatRis(rispy.load(file)[0])
							f_type = FILETYPE.ris
						case _:
							# assume text file, read contents
							try:
								s = file.read() if s is None else s
							except OSError:
								raise ValueError(f"Cannot read file {f_name}.")
							f_type = getStringType(f_name, ext, s)
							c_dict = loadStringData(f_name, f_type, s)

	return c_dict


def parseCitation(f_name, str_type=None, s=None):
	"""Parse a citation.
	
	Args:
	    f_name (str): File name
	    str_type (str, optional): Type of citation format to be parsed, default None signifies autodetect
	    s (str, optional): String to parse; default is None, supplied implies clipboard
	
	Returns:
	    str: Parsed citation
	
	Raises:
	    ValueError: if filetype supplied is erroneous
	"""
	if f_name is not None: assert os.path.exists(f_name), f"Path {f_name} to file does not exist."

	match str_type:
		case None:
			f_type = None
		case "ris":
			f_type = FILETYPE.ris
		case "bibtex":
			f_type = FILETYPE.bibtex
		case _:
			raise ValueError(f"Cannot parse filetype '{str_type}'.")

	# obtain file data
	c_dict = getFileData(f_name, f_type, s)
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