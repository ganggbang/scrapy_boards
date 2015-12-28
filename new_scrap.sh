#!/bin/bash

SCRAPY_DIR=/home/admin/web/katerusa/public_html/scrapy_boards
rm -rf $SCRAPY_DIR/last.csv
rm -rf $SCRAPY_DIR/tmp
rm -rf $SCRAPY_DIR/full

cd $SCRAPY_DIR
scrapy crawl scraby -a mode=from_list -a file_path=$SCRAPY_DIR/list_urls.txt -o $SCRAPY_DIR/last.csv -t csv


rm -rf $SCRAPY_DIR/list_urls.txt

chown -R admin.admin $SCRAPY_DIR

su - admin -c 'php ~/web/katerusa/public_html/core/components/minishop2/import/csv.php "scrapy_boards/last.csv" "content,price,old_price,pagetitle,boatyear,boatbrand,boatmodel,boatlength,boatwidth,boatmotor,boattype,parent,template,bfromurl,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,gallery,bfromsite" 1 "pagetitle" 0 "|"' -s '/bin/bash'


rm -rf $SCRAPY_DIR/last.csv