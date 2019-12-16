import argparse
from os import path
from PyPDF2 import PdfFileReader


def generate_toc(input_file):
    reader = PdfFileReader(input_file)

    outlines = reader.outlines

    for entry in outlines:

        try:
            title = entry['/Title']
            page_number = reader.getDestinationPageNumber(entry) + 1
            
        except:
            continue

        print(title + ' {' + str(page_number) + '}')
    

def run():
    parser = argparse.ArgumentParser(description='Generate TOC for PDF reader')
    parser.add_argument('input_file', help='Input PDF file')

    args = parser.parse_args()

    generate_toc(path.abspath(args.input_file))


if __name__ == "__main__":
    run()
