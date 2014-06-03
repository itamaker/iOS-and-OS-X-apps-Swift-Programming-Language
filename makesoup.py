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
import re


baseUrl = 'https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/'

def cleanpage(url):
    soup = BeautifulSoup(urlopen(url))
    art = soup.find('article', class_="chapter")
    styleChange = [('<h2','<h1'),('</h2>','</h1>'),('<h3','<h2'),('</h3>','</h2>')]
    artHtml = re.sub(re.compile('<section\sid="next_previous"\sclass="">.+?</section>', re.DOTALL), '\n', str(art))
    for x,y in styleChange:
        artHtml = re.sub(re.compile(x),y,artHtml)
    return artHtml

def getpage(allLink):
    # web crawler
    allPage = []
    for idx, unit in enumerate(allLink):
        url, name  = unit
        url  = baseUrl + url
        page = cleanpage(url)
        allPage.append(page)
        print idx+1,name
    return allPage

def main():
    soup = BeautifulSoup(urlopen(baseUrl))
    tt = soup.find('nav', class_="book-parts hideInXcode")
    allLink = map(lambda x: (x.get('href'), x.text), tt.findAll('a')) #read all links
    allPage = getpage(allLink)
    with open('swift.md','wb') as f:
        for apage in allPage:
            f.write(apage)
    print 'All done'

if __name__ == '__main__':
    main()
