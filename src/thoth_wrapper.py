#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
from os import path

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
    parser.add_argument('-t', '--toc', help='Input toc file')
    args = parser.parse_args()

    toc = html2text(path.abspath(args.toc))

    print(toc)

    

if __name__ == "__main__":
    main()
