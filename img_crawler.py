#!/usr/bin/python

import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import optparse

from bs4 import BeautifulSoup as BS

URL = 'http://tw-hiesrv.tw.trendnet.org/uiwww/segment/03_consumer/MUP/R1.5/Mobile/Visual/slice/Android/drawable-hdpi/'
img_file_exts = ['png', 'jpg']

opt_parser = optparse.OptionParser('Usage: %prog [options] download_folder')
opt_parser.add_option('-d', '--debug', action='store_true', dest='debug', default=False,
                      help='switch on debug mode for more detailed output')
opt, args = opt_parser.parse_args()

if opt.debug:
    print 'opt: ', opt
    print 'args: ', args

if len(args) == 0:
    download_folder = '.'

soup = BS(urlopen(URL))
links = soup.findAll('a') + soup.findAll('A')
total_num = 0
for link in links:
    href = link['href']
    for ext in img_file_exts:
        if href.endswith(ext):
            img_url = urlparse.urljoin(URL, href)
            out_path = os.path.join(download_folder, link.string)
            print 'start downloading ' + link.string
            urlretrieve(img_url, out_path)
            total_num += 1
            break

if opt.debug:
    print 'summary >>>>>>>>>>>>>>>>>>>>>>'
    print 'download ' + str(total_num) + ' images in total'
    print 'end <<<<<<<<<<<<<<<<<<<<<<<<<<'

