#!/usr/bin/env python3
from PyPDF2 import PdfFileReader


class Outline():
    '''
    Get a PDF file as input and extract information such as
    chapter names and page numbers
    '''
    def __init__(self, pdf_file):
        reader = PdfFileReader(pdf_file)
        outlines = reader.outlines

        self.chapters = []
        self.extract_data(reader, outlines)

    def extract_data(self, reader, outlines):
        '''
        Extract chapter titles and page numbers and place them
        into a (python) list of dictionaries.
        i.e. [{'title': 'ch1', 'page_number': 1},
              {'title': 'ch2', 'page_number': 2}]
        '''
        for entry in outlines:

            try:
                title = entry['/Title']
                page_number = reader.getDestinationPageNumber(entry) + 1

            except TypeError:
                continue

            self.chapters.append({'title': title,
                                  'page_number': page_number})

    def get_chapter_list(self):
        '''
        Return a simple chapter (python) list by taking self.chapters
        and stripping out information about the page number.
        '''
        return [entry['title'] for entry in self.chapters]

    def get_data(self):
        '''
        Method to retrieve self.chapters.
        '''
        return self.chapters
