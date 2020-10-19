#!/bin/python3

# Name of program : scrapIndexOf
# GitHub : https://github.com/TheWolfSecu/scrapIndexOf.git
#
# Created by TheWolfSecu with ❤

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import os.path
import os
import argparse
from multiprocessing.dummy import Pool as ThreadPool


# Variables

domain = []
urls = []
document_download = []
usefulExtension = []
date = str(datetime.now())
nameDirectory = "data"
nameDirectorySearch = date
nameFileLinkExist = "%s/%s/Link_%s"%(nameDirectory,nameDirectorySearch,date)
nameFileElementExist = "%s/%s/File_%s"%(nameDirectory,nameDirectorySearch,date)
namedirectoryFile = "File"
linkHrefHeader = ["?C=N;O=D","?C=M;O=A","?C=S;O=A","?C=D;O=A"]

pool = ThreadPool(4)


# Create directory 

def checkDirectoryExist():
    if os.path.isdir(nameDirectory) == False:
        os.mkdir(nameDirectory)
    if os.path.isdir(nameDirectory+"/"+nameDirectorySearch) == False:
        os.mkdir(nameDirectory+"/"+nameDirectorySearch)
    if os.path.isdir(nameDirectory+"/"+nameDirectorySearch+"/"+namedirectoryFile) == False:
        os.mkdir(nameDirectory+"/"+nameDirectorySearch+"/"+namedirectoryFile)

# Header

def header():
    os.system('clear')
    print("""

 ____                      ___           _            ___   __ 
/ ___|  ___ _ __ __ _ _ __|_ _|_ __   __| | _____  __/ _ \ / _|
\___ \ / __| '__/ _` | '_ \| || '_ \ / _` |/ _ \ \/ / | | | |_ 
 ___) | (__| | | (_| | |_) | || | | | (_| |  __/>  <| |_| |  _|
|____/ \___|_|  \__,_| .__/___|_| |_|\__,_|\___/_/\_\\___/|_|  
                     |_|                                       

            # Created by TheWolfSecu - v1.0.0
        """)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", type=str,help="IP address or domain name")
    parser.add_argument("-e","--extension",type=str,help="Retrieve files according to the extension. Exemple : pdf,sql")
    args = parser.parse_args()
    domain.append(str(args.domain))
    if args.extension:
        for e in args.extension.split(','):
            usefulExtension.append(e)
    urls.append(args.domain)
    fileLink = open(nameFileLinkExist,"a")
    fileLink.write(args.domain+"\n")
    fileLink.close()


# Check Version of python

def checkVersion():
    if int(sys.version.split(".")[0]) == 3:
        return True
    else:
        return False


def retrieveOtherUrl(url):
    body_url = requests.get(url)
    
    if body_url.status_code == 200:
            print("\033[34m %s => %s\033[0m"%(url,str(body_url.status_code)))
            soup = BeautifulSoup(body_url.content,"html.parser")
            a = soup.find_all('a')
                
            for a in a:
                a_href = str(a.get("href"))
                last_carac = a_href[-1:]
                if last_carac == "/":
                    a_split = a_href.split('/')
                    if len(a_split) == 2 and a_split[0] != "":
                        urls.append(url+""+a_href)
                        fileLink = open(nameFileLinkExist,"a")
                        fileLink.write(url+""+a_href+"\n")
                        fileLink.close()
                else:
                    linkTrue = [l for l in linkHrefHeader if l == a_href ]
                    if len(linkTrue) == 0:
                        document_download.append(url+""+a_href)
                        fileDownload = open(nameFileElementExist,"a")
                        fileDownload.write(url+""+a_href+"\n")
                        fileDownload.close()
            urls.remove(url)
    else:
        print("\033[31m %s => %s\033[0m"%(url,str(body_url.status_code)))

def retrieveFiles(files):
    link_file = requests.get(files,stream=True)
    headers_contentType = str(link_file.headers['Content-Type'])
    extension = headers_contentType.split('/')
    extensionExist = [ e for e in usefulExtension if str(e) == str(extension[1]) ]
    if len(extensionExist) == 1:
        nameFile_split = files.split(domain[0])
        nameFile = nameFile_split[-1:]
        nameFile = str(nameFile[0]).replace("/","-")
        print("\033[35m File %s download \033[0m"%(nameFile))
        
        with open(nameDirectory+"/"+nameDirectorySearch+"/"+namedirectoryFile+"/"+nameFile,"wb") as fp:
            fp.write(link_file.content)

# Beginning of the program

if checkVersion():
    checkDirectoryExist()
    header()

    # Recup other url

    while len(urls) != 0:
        pool.map(retrieveOtherUrl, urls)

    pool.map(retrieveFiles,document_download)
    pool.close()
    pool.join()