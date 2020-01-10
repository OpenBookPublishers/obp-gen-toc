#!/usr/bin/env python3
import subprocess
import re

class Outline():
    '''
    Get a PDF file as input and extract information such as
    chapter names and page numbers up to the specified TOC level
    '''
    def __init__(self, pdf_file, level):
        # Get the complete outline
        outline = self.get_outline(pdf_file)

        # Reduce the outline to the specified TOC level
        reduced_outline = self.reduce_outline(outline, level)

        self.chapters = []
        self.extract_data(reduced_outline)

    def get_outline(self, pdf_file):
        '''
        Extract outline from the PDF file. Take the file path (str) of
        the PDF and return the the complete outline (str).

        Levels are indented with (leading) tabs.
        '''
        cmd = ['mutool', 'show', pdf_file, 'outline']

        run = subprocess.run(cmd, stdout=subprocess.PIPE)
        outline = run.stdout.decode('utf-8')

        return outline

    def reduce_outline(self, outline, level):
        '''
        Reduce the outline to the specified (int) TOC level.
        Return a clean string of the resulting outline.
        
        A tab character separates title from page number
        i.e. 'This is a chapter title\t10'
        '''
        # Match lines starting with as many tab as in the
        # range {level,} and remove them
        pattern = r'^\t{%s,}.*\n?' % level
        reduced_outline = re.sub(pattern, '', outline,
                                 flags=re.MULTILINE)

        # Remove leading tabs
        clean_outline = re.sub(r'^\t', '', reduced_outline,
                               flags=re.MULTILINE)
        
        return clean_outline

    def extract_data(self, reduced_outline):
        '''
        Extract chapter titles and page numbers and place them
        into a (python) list of dictionaries.
        i.e. [{'title': 'ch1', 'page_number': 1},
              {'title': 'ch2', 'page_number': 2}]
        '''
        for line in reduced_outline.splitlines():
            self.chapters.append({'title': line.split('\t')[0],
                                  'page_number': line.split('\t')[1]})

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
