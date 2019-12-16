#!/usr/bin/env python3
from PyPDF2 import PdfFileReader


class Outline():
    def __init__(self, pdf_file):
        reader = PdfFileReader(pdf_file)
        self.outlines = reader.outlines

    def get_chapter_list(self):
        chapters = []
    
        for entry in self.outlines:

            try:
                title = entry['/Title']

            except:
                continue

            chapters.append(title)

        return chapters
