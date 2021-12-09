#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup
from os import path
import subprocess
from thothlibrary import ThothClient
from os import getenv

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
    parser.add_argument('--dry-run', action='store_true',
                        help='Do not upload data to Thoth')
    args = parser.parse_args()

    # Execute run.sh
    cmd = f'bash {RUN_PATH} file'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    toc = html2text(TOC_PATH)

    # query Thoth
    client = ThothClient(version="0.6.0")
    data = client.query('workByDoi',
                        {'doi': f'"https://doi.org/10.11647/{args.doi}"'})
    # update toc
    data['toc'] = toc

    # login
    thoth_email = getenv('THOTH_EMAIL')
    thoth_pwd = getenv('THOTH_PWD')

    if not thoth_email or not thoth_pwd:
        raise 'Thoth credentials not set: $THOTH_EMAIL and $THOTH_PWD'

    client.login(thoth_email, thoth_pwd)

    if not args.dry_run:
        mutation = client.mutation('updateWork', data, units='MM')


if __name__ == "__main__":
    main()
