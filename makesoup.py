# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        The-Swift-Programming-Language
# Purpose:     Web crawler of Swift, Python is slow-------
#
# Author:      muxuezi@gmail.com
#
# Created:     03/06/2014
# Copyright:   (c) muxuezi 2014
# Licence:     <All licence>
#-------------------------------------------------------------------------------
from bs4 import  BeautifulSoup
from urllib2 import urlopen


temp = open('swif.txt').readlines() #read all links
with open('swift.md','wb') as f:
    # web crawler
    for id,url in enumerate(temp):
        soup = BeautifulSoup(urlopen(url.strip()))
        art = soup.find('article', class_="chapter")
        f.write(str(art) + '\n')
print 'Well done!'
