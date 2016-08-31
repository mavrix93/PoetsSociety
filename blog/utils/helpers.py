import re

def get_first_verse(poem_txt):
    first_verse = re.split('\n\s*\n', poem_txt)
    if len(first_verse) > 1:
	return first_verse[0] +"\n..."
    return poem_txt
