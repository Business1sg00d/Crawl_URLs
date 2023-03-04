#!/usr/bin/env python3




import re
import sys
import requests
from bs4 import BeautifulSoup
from os.path import exists




def get_html_of(url):
    webpage = requests.get(url)#, verify=False)
    reqStatus = webpage.status_code
    DecodeURL = (webpage.content.decode())

    if reqStatus != 200:
        print(f'HTTP status code: {reqStatus}. Code 200 was expected. Exiting script.')
        exit(1)
    return DecodeURL




def check_urls(DecodeURL, urls_found_set):
    urls_found = re.split('\'|"', DecodeURL)
    urls_in_brackets = re.findall(r'\(.*?\)', DecodeURL) 

    #Find URLs
    with open('urls.txt', 'a') as w:
        for line in urls_found:
            starts_with_http = re.findall(r'^http.*', line)
            if len(starts_with_http) != 0:
                if starts_with_http[0] not in urls_found_set:
                    urls_found_set.add(starts_with_http[0])
                    w.write(starts_with_http[0])
                    w.write('\n')
        
        #Find URLs stuck within brackets; write to file
        for line in urls_in_brackets:
            starts_with_http = re.findall(r'^http.*', line.strip('(|)'))
            if len(starts_with_http) != 0:
                if starts_with_http[0] not in urls_found_set:
                    urls_found_set.add(starts_with_http[0])
                    w.write(starts_with_http[0])
                    w.write('\n')
    return urls_found_set




def click_links(url, firsturl, urls_found_set):
    html = get_html_of(url)
    CodeU = BeautifulSoup(html, 'html.parser')
    all_links = CodeU.findAll('a')
    currenturl = url

    with open('crawl.txt', 'a') as wr:
        for link in all_links:
            wr.write(str(link.get('href')))
            wr.write('\n')
    with open('crawl.txt', 'r') as r:
        pattern = re.findall(r'\b'+firsturl+r'.*', r.read())
    with open('crawl.txt', 'w') as w:
        for line in pattern:
            checkline = line.rstrip()
            removechar = checkline.rstrip('/') #this line assumes the user did not write '/' after URL
            exe = ('.exe', '.rpm', '.dmg', '.bz2', '.tgz', '.zip', '.git', '.png')
            if removechar != currenturl and not any(exe in removechar for exe in exe):
                w.write(removechar)
                w.write('\n')
    with open('crawl.txt', 'r') as r:
        lines = r.readlines()
        newlines = []
        for line in lines:
            if line not in newlines:
                newlines.append(line)
    with open('crawl.txt', 'w') as w:
        for line in newlines:
            w.write(line)
    return check_urls(html, urls_found_set)




def main(url, crawldepth):
    urls_found_set = set()

    if int(crawldepth) == 0:
        get_html_of(url)
        exit(0)
    else:
        firsturl = url
        file_exists = exists('/home/ShiguruiMuerto/Documents/Scripts/HTB_Project_Python/crawl.txt')
        if file_exists == False:
            print('crawl.txt file does not exist. Check code or create the file manually.')
            exit(1)
        urls_found_set = click_links(url, firsturl, urls_found_set)
        with open('crawl.txt', 'r') as r:
            searchedurls = []
            n = 1
            crawllist = r.readlines()
            for line in crawllist:
                URL = line.rstrip()
                try:
                    iterations(URL, searchedurls)
                    searchedurls = append_urls(URL, searchedurls)
                    print(searchedurls)
                except SystemExit:
                    pass

                if a == 2: continue
                elif a == 0: urls_found_set = click_links(URL, firsturl, urls_found_set)

                n = n + 1

                if n > int(crawldepth):
                    exit(0)




def iterations(URL, searchedurls):
    url = URL
    global a
    if url not in searchedurls:
        a = 0
        return a
    else:
        a = 2
        return a




def append_urls(URL, searchedurls):
    url = URL
    if url not in searchedurls: searchedurls.append(url)
    return searchedurls




if __name__=='__main__':
    url = sys.argv[1]
    crawldepth = sys.argv[2]
    main(url, crawldepth)
