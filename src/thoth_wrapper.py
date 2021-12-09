#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
from os import path

import subprocess

TOC_PATH=path.abspath('./output/Jshop-TOC.txt')
RUN_PATH='/ebook_automation/run'

def html2text(toc_path):
    toc = ''

    with open(toc_path) as toc_file:
        soup = BeautifulSoup(toc_file, 'html.parser')

        # remove the 'download links'
        for span in soup.find_all('span'):
            span.decompose()

        for p in soup.find_all('p'):
            toc += p.get_text('\n', strip=True) + '\n\n'

    return toc


def main():
    parser = argparse.ArgumentParser(description='Thoth wrapper')
    parser.add_argument('-d', '--doi', help='Work DOI (registered in Thoth)')
    args = parser.parse_args()

    # Execute run.sh
    cmd = f'bash {RUN_PATH} file'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    toc = html2text(TOC_PATH)

    print(toc)



if __name__ == "__main__":
    main()
