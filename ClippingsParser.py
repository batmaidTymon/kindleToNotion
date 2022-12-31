import re
from dataclasses import dataclass
from typing import List

@dataclass
class Clipping:
    author: str
    title: str
    highlightText: str
    dateAndLocation: str

# sample clipping:
# Never Split the Difference: Negotiating as if Your Life Depended on It (Chris Voss)
# - Your Highlight at location 3749-3751 | Added on Monday, 26 December 2022 10:14:35
#
# How does this affect the rest of your team? How on board are the people not on this call? What do your colleagues see as their main challenges in this area?

class ClippingsParser:

    def parseClippings(self, filePath: str) -> List[Clipping]:
        clippings = ''
        # read all content from the clippingsfile
        with open(filePath, 'r') as file:
            clippings = file.read().split('==========')

            clippings = [clipping.strip() for clipping in clippings]
            clippings = list(filter(None, clippings))

        # loop through all clippings
        for clipping in clippings:

            # get title via regex
            match = re.search(r'(.*)\((.*)\)', clipping)
            title = match.group(1)
            author = match.group(2)
            highlightText = '\n'.join( clipping.splitlines()[2:] ).strip()
            dateAndLocation = clipping.splitlines()[1]


            yield Clipping(author, title, highlightText, dateAndLocation)
