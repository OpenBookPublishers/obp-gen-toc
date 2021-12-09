# obp-gen-toc
Generate better TOCs for the website.

Once a book is published, the website requires a TOC:
 1.  TOC to display in the _Contents_ tab of the (website) product page ([example](https://doi.org/10.11647/OBP.0195#contents)).

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

## How to run this tool
### Run with docker

The environment variable TOC_LEVEL refers to the TOC level to which parse the TOC to. 

```
docker run --rm \
  -v /path/to/local/file.xml:/ebook_automation/file.xml \
  -v /path/to/local/file.pdf:/ebook_automation/file.pdf \
  -v /path/to/output:/ebook_automation/output \
  -e TOC_LEVEL=1 \
  openbookpublishers/obp-gen-toc \
  bash run file
```

Alternatively you may clone the repo, build the image using `docker build . -t some/tag` and run the command above replacing `openbookpublishers/obp-gen-toc` with `some/tag`.

## Thoth wrapper

In the repository is available a wrapper to upload the toc to Thoth (as plain text). The new command would be:

```
docker run --rm \
           --user `id -u`:`id -g` \
           -v `pwd`/input/file.xml:/ebook_automation/file.xml \
           -v `pwd`/input/file.pdf:/ebook_automation/file.pdf \
           -v `pwd`/output/obp-gen-toc:/ebook_automation/output \
           -e TOC_LEVEL=1 \
           -e THOTH_EMAIL=${THOTH_EMAIL} \
           -e THOTH_PWD=${THOTH_PWD} \
           openbookpublishers/obp-gen-toc \
           ./src/thoth_wrapper.py --doi $(doi)
```
