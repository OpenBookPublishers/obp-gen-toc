import argparse
from os import path
from bs4 import BeautifulSoup


def get_chapters(soup):
    '''
    Extract chapters from the (beautiful suop object)
    doi deposit.
    '''
    return soup.find_all('content_item',
                         {'component_type': 'chapter'})


def join_author_names(names):
    '''
    Take a list of author names and return a string of names 
    in a pretty format.
    
    i.e. ['author1', 'author2', 'author3'] 
         -> 'author1, author2 and author3'
    '''
    return ", ".join(names[:-2] \
                     + [" and ".join(names[-2:])])


def get_authors(chapter):
    '''
    Takes a (beautiful suop object) chapter and
    return a string with author name(s).
    '''
    contributors = chapter.find_all('person_name')

    names = []
     
    for person in contributors:
        names.append(person.find('given_name').text \
                     + ' ' \
                     + person.find('surname').text)

    return join_author_names(names)


def get_title(chapter):
    '''
    Get chapter title from the (beautiful suop object)
    given chapter.
    '''
    return chapter.find('title').text


def get_pdf_url(chapter):
    '''
    Get the PDF url from the (beautiful suop object)
    given chapter.
    '''
    return chapter.find('resource', {'mime_type': 'application/pdf'}).text


def get_doi_chapters(file_path):
    with open(file_path, 'r')as in_file:
        soup = BeautifulSoup(in_file, 'html.parser')

        chapters = get_chapters(soup)

        data = {}

        for chapter in chapters:

            authors = get_authors(chapter)
            title = get_title(chapter)
            pdf_url = get_pdf_url(chapter)

            data.update({title: {'authors':authors,
                                 'pdf_url': pdf_url}})

        return data


def run():
    parser = argparse.ArgumentParser(description='Generate TOC for JShop')
    parser.add_argument('doi_file', help='Input DOI deposit file')

    args = parser.parse_args()

    doi_chapter_data = get_doi_chapters(path.abspath(args.doi_file))
    print(doi_chapter_data)


if __name__ == "__main__":
    run()
