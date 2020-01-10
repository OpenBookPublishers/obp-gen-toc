# obp-gen-toc
Generate better TOCs for the website.

Once a book is published, the website requires two types of TOCs:
 1.  TOC to display in the _Contents_ tab of the (website) product page ([example](https://doi.org/10.11647/OBP.0195#contents)).
 2.  TOC for [PDF reader](https://github.com/OpenBookPublishers/obp-gen-pdfreader) integration;

This can be performed programmatically via scripts stored in `./src/` taking as arguments files which are already part of the publication workflow (DOI deposit and PDF file)

## Content of `./src/`
### `./src/generate_toc_jshop.py`
TOC to display in the _Contents_ tab of the (website) product page ([example](https://doi.org/10.11647/OBP.0195#contents))

This script extracts the TOC from the PDF file and integrates this information with what is reported in the DOI deposit (via fuzzy matching of chapter titles).

The result is a neat TOC which reports chapter titles, author names and download link of individual chapter PDFs, such as:

```
Preface
Acknowledgements

1. Introduction                                        Download
Author1 Name, Author2 Name and Author3 Name

2. Chapter One Title                                   Download
Author1 Name and Author2 Name
```

### `./src/generate_toc_pdf_reader.py`
Script to produce the TOC for [PDF reader](https://github.com/OpenBookPublishers/obp-gen-pdfreader) integration.

This script extracts the TOC from the PDF file consisting of title name and (real) PDF page number.

The result looks like this:

```
Preface {5}
Acknowledgements {10}

1. Introduction {15}
2. Chapter One Title {20}
```

## How to run this tool
### Run with docker

The environment variable TOC_LEVEL refers to the TOC level to which parse the TOC to. 

```
docker run --rm \
  -v /path/to/local/file.xml:/ebook_automation/file.xml \
  -v /path/to/local/file.pdf:/ebook_automation/file.pdf \
  -v /path/to/output:/ebook_automation/output \
  -e TOC_LEVEL=1 \
  openbookpublishers/obp-gen-toc
```

Alternatively you may clone the repo, build the image using `docker build . -t some/tag` and run the command above replacing `openbookpublishers/obp-gen-toc` with `some/tag`.