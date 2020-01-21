import argparse
from outline import Outline
from os import path


def generate_toc(input_file, level):
    '''
    Print to standard output the table of contents for
    obp-gen-pdfreader integration, such as:

    Introduction {1}
    Chapter 1 {3}
    [...]
    '''

    outlines = Outline(input_file, level)

    chapters = outlines.get_data()

    for entry in chapters:
        print('%s {%s}' % (entry['title'], entry['page_number']))


def run():
    parser = argparse.ArgumentParser(description='Generate TOC for PDF reader')
    parser.add_argument('input_file', help='Input PDF file')
    parser.add_argument('-l', '--level', default=1,
                        help='TOC level to which to parse to')

    args = parser.parse_args()

    generate_toc(path.abspath(args.input_file), args.level)


if __name__ == "__main__":
    run()
