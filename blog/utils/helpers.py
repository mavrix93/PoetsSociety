import re



def get_first_verses(poems):
    poems_preview = []
    for poem in poems:
        poem.text = _get_first_verse(poem.text)
        poems_preview.append(poem)
    return  poems_preview


def _get_first_verse(poem_txt):
    first_verse = re.split('\n\s*\n', poem_txt)
    if len(first_verse) > 1:
	    return first_verse[0] +"\n..."
    return poem_txt