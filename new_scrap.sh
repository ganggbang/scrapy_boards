#!/bin/bash

rm -rf last.csv
rm -rf ./tmp
rm -rf ./full
scrapy crawl scraby -o last.csv -t csv
