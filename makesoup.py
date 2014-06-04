# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Name:        The-Swift-Programming-Language
# Purpose:     Web crawler of Swift, Python is slow-------
#
# Author:      muxuezi@gmail.com
#
# Created:     03/06/2014
# Copyright:   (c) muxuezi 2014
# Licence:     <All licence>
#-------------------------------------------------------------------------
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import time
import thread


allPageCnt = {}
mutex = thread.allocate_lock()
exitmutexes = [thread.allocate_lock() for i in range(35)]
baseUrl = 'https://developer.apple.com/library/prerelease/ios/documentation/Swift/Conceptual/Swift_Programming_Language/'

def cleanpage(url):
    soup = BeautifulSoup(urlopen(url))
    art = soup.find('article', class_="chapter")
    styleChange = [('<h2', '<h1'), ('</h2>', '</h1>'), ('<h3', '<h2'), ('</h3>', '</h2>')]
    artHtml = re.sub(re.compile('<section\sclass=""\sid="next_previous">.+?</section>',re.DOTALL), '', str(art))
    for x, y in styleChange:
        artHtml = re.sub(re.compile(x), y, artHtml)
    return artHtml


def getpage(idx, unit, mutex):
    # web crawler
    with mutex:
        url, name = unit
        url = baseUrl + url
        page = cleanpage(url)
        allPageCnt[idx + 1] = page
        print idx + 1, name
    exitmutexes[idx].acquire()


def main():
    # read all links
    soup = BeautifulSoup(urlopen(baseUrl))
    tt = soup.find('nav', class_="book-parts hideInXcode")
    allLink = map(lambda x: (x.get('href'), x.text), tt.findAll('a'))
    for idx, unit in enumerate(allLink):
        thread.start_new_thread(getpage, (idx, unit, mutex))
    while True:
        if all(mutex.locked() for mutex in exitmutexes):
            with open('swift.html', 'wb') as f:
                for k,apage in sorted(allPageCnt.items()):
                    f.write(apage)
            print 'All done'
            break
        else:
            time.sleep(0.01)

if __name__ == '__main__':
    main()
