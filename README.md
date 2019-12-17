# obp-gen-toc
Collection of scripts to produce TOCs for the website.

Work in progress

## How to run this tool
### Run with docker

```
docker run --rm \
  -v /path/to/local/file.xml:/ebook_automation/file.xml \
  -v /path/to/local/file.pdf:/ebook_automation/file.pdf \
  -v /path/to/output:/ebook_automation/output \
  openbookpublishers/obp-gen-toc
```

Alternatively you may clone the repo, build the image using `docker build . -t some/tag` and run the command above replacing `openbookpublishers/obp-gen-toc` with `some/tag`.

## DEV
 -  Multi-level TOC for `generate_toc_jshop.py`?