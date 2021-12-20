# obp-gen-toc
A tool to generate rich HTML TOCs.

This tool combines the information of a book PDF bookmark data and its DOI deposit to output an HTML representation of its TOC. The output would look like this:

```
Preface
Acknowledgements

1. Introduction                                        Download
Author1 Name, Author2 Name and Author3 Name

2. Chapter One Title                                   Download
Author1 Name and Author2 Name
```

## Installation

Clone the repo and build the docker image: $ `docker build . -t openbookpublishers/obp-gen-toc`.

## Usage

```bash
docker run --rm \
           -v /path/to/local/file.xml:/ebook_automation/file.xml \
           -v /path/to/local/file.pdf:/ebook_automation/file.pdf \
           -v /path/to/output:/ebook_automation/output \
           -e TOC_LEVEL=1 \
           openbookpublishers/obp-gen-toc \
           bash run file
```

The environment variable TOC_LEVEL refers to the TOC level to which parse the TOC to.

## Thoth Wrapper (Optional)

The [Thoth](https://thoth.pub/) wrapper stored at ./src/thoth_wrapper.py` would:

 - Convert the HTML TOC to plain text;
 - Upload the TOC to Thoth.

The new command would be:

```bash
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

Make sure you store your Thoth credentials in the env variables $THOTH_EMAIL and $THOTH_PWD.

## Contributing

Pull requests are welcome.

## License

[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)
