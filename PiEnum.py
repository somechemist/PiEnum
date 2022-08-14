#!/usr/bin/env python3

import argparse
import requests

flag = argparse.ArgumentParser()

flag.add_argument("-s", "--subdomain", help="enumerate subdomains? default is www.")
flag.add_argument("-d", "--directory", help="enumerate directories? default is /")
flag.add_argument("-u", "--url", help="enter the desired url! default is localhost")
flag.add_argument("-z", "--secured", default=False, action=argparse.BooleanOptionalAction, help="enabled https instead of http")

args = flag.parse_args()

stopSubDomain = 0
useProtocol = 0
appWww = 0

subList = ""
finalList = ""
protocol = ""

secured = "https://"
insecured = "http://"

if args.secured != False:
    protocol = secured
else:
    protocol = insecured

if args.url == None:
    print("Please use the --url flag to list the url")
else:
    url = str(args.url)
    urlLen = int(len(url))
    urlLen = urlLen - 5
    urlTrimmed = url[:urlLen]
    subDom = "."
    if subDom in urlTrimmed:
        print("Subdomain found in URL, ignoring subdomain flags")
        stopSubDomain = 1
    else:
        print("No subdomain given, will use 'www.' unless --subdomain list is given")
        appWww = 1

if args.subdomain != None:
    if stopSubDomain != 1:
        useProtocol = 1
        try:
            subDomList = str(args.subdomain)
            subDomList = open(subDomList).read()
            subDomains = subDomList.splitlines()

            for sd in subDomains:
                sUrl = f"{protocol}{sd}.{url}"
                try:
                    subList += f"{sUrl}\n"
                except:
                    print("error in subdomains function")
        except:
            print("Couldn't make subdomain list:\nFile likely not found")
    else:
        pass
else:
    print("Ignoring Subdomains")
    if appWww == 1:
        url = f"www.{url}"
    pass
print(subList)

if args.directory != None:
    if useProtocol != 1:
        url = f"{protocol}{url}"
        subList = url
    else:
        pass
    try:
        dirFile = str(args.directory)
        dirFile = open(dirFile).read()
        dirList = dirFile.splitlines()
        subList = subList.splitlines()

        for dom in subList:
            for dir in dirList:
                dUrl = f"{dom}/{dir}"
                try:
                    print(dUrl)
                    finalList += f"{dUrl}\n"
                except:
                    print("Error is dir block")
    except:
        print("Couldn't make directory list:\nFile likely not found")
else:
    print("Ignoring Directories")
    pass
