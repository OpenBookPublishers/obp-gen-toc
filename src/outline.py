#!/usr/bin/env python3
import fitz

class Outline():
    '''
    Get a PDF file as input and extract information such as
    chapter names and page numbers up to the specified TOC level
    '''
    def __init__(self, pdf_file, depth):
        self.depth = int(depth)

        self.doc = fitz.open(pdf_file)

    def get_chapter_list(self):
        '''
        Return a simple chapter (python) list of book chapters.
        '''
        # this method returns a python list of lists which looks like:
        # [[level1, title1, p_number1], [level2, title2, p_number2]]
        toc = self.doc.get_toc()

        chapters = []

        for level, title, page in toc:
            if level in range(self.depth + 1):
                chapters.append(title)

        return chapters
