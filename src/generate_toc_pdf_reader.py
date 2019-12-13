import argparse
from os import path
from PyPDF2 import PdfFileReader


def generate_toc(input_file):
    reader = PdfFileReader(input_file)

    outlines = reader.outlines

    for entry in outlines:
        string = entry['/Title'] \
                 + ' {' \
                 +  str(reader.getDestinationPageNumber(entry) + 1) \
                 + '}'
        print(string)
    

def run():
    parser = argparse.ArgumentParser(description='Generate TOC for PDF reader')
    parser.add_argument('input_file', help='Input PDF file')

    args = parser.parse_args()

    generate_toc(path.abspath(args.input_file))


if __name__ == "__main__":
    run()
