#!/bin/bash

rm -rf last.csv
rm -rf ./tmp
rm -rf ./full
scrapy crawl scraby -a mode=from_list -a file_path=list_urls.txt -o last.csv -t csv
