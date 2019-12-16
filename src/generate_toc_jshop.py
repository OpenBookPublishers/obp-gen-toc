import argparse
from outline import Outline
from os import path
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz


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
    return ', '.join(names[:-2]
                     + [' and '.join(names[-2:])])


def get_authors(chapter):
    '''
    Takes a (beautiful suop object) chapter and
    return a string with author name(s).
    '''
    contributors = chapter.find_all('person_name')

    names = []

    for person in contributors:
        names.append(person.find('given_name').text
                     + ' '
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

            data.update({title: {'authors': authors,
                                 'pdf_url': pdf_url,
                                 'title': title}})

        return data


def check_match(chapter, doi_chapter):
    '''
    Fuzzy string matching between two chapter names; returns a
    (int) ratio of the match.
    '''
    ratio = fuzz.ratio(chapter.lower(), doi_chapter.lower())

    return ratio


def generate_toc(data):
    soup = BeautifulSoup('<div></div>', 'html.parser')

    source_tag = soup.div

    for entry in data:

        # if entry is not a dictionary
        if type(entry) is not dict:
            attrs = {'class': 'title'}
            title_tag = soup.new_tag('p', **attrs)
            title_tag.string = entry

        else:
            for element in entry:
                # Title
                attrs = {'class': 'title'}
                title_tag = soup.new_tag('p', **attrs)
                title_tag.string = entry[element]['title']

                # Download block
                attrs = {'style': 'float: right;'}
                span_tag = soup.new_tag('span', **attrs)

                attrs = {'href': entry[element]['pdf_url'].lower()}
                a_tag = soup.new_tag('a', **attrs)
                a_tag.string = 'Download'

                span_tag.append(a_tag)
                title_tag.append(span_tag)

                # append <br>
                title_tag.append(soup.new_tag('br'))

                # Author
                attrs = {'class': 'authors'}
                authors_tag = soup.new_tag('i', **attrs)
                authors_tag.string = entry[element]['authors']

                title_tag.append(authors_tag)

        source_tag.append(title_tag)

    print(source_tag.prettify())


def run():
    parser = argparse.ArgumentParser(description='Generate TOC for JShop')
    parser.add_argument('doi_file', help='Input DOI deposit file')
    parser.add_argument('pdf_file', help='Input PDF deposit file')

    args = parser.parse_args()

    # Get a (simple) list of the chapters
    outline = Outline(path.abspath(args.pdf_file))
    chapters = outline.get_chapter_list()

    # Make a dictionary with chapters with DOI and related info
    # (author name(s), chapter title and PDF url)
    doi_chapters = get_doi_chapters(path.abspath(args.doi_file))

    # Merge in data the information of the first list
    # and the dictionary
    data = []

    for chapter in chapters:
        for doi_chapter in doi_chapters:

            # Find (fuzzy) string matches
            if check_match(chapter, doi_chapter) > 90:
                data.append({doi_chapter: doi_chapters[doi_chapter]})
                break

        else:
            data.append(chapter)

    generate_toc(data)


if __name__ == "__main__":
    run()
