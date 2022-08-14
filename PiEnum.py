#!/usr/bin/env python3

import argparse
import requests

# flag handling
flag = argparse.ArgumentParser()

flag.add_argument("-s", "--subdomain", help="Enumerate subdomains. Default is www.")
flag.add_argument("-d", "--directory", help="Enumerate directories. Default is /")
flag.add_argument("-u", "--url", help="Enter the desired url! Default is localhost")
flag.add_argument("-z", "--secured", default=False, action=argparse.BooleanOptionalAction, help="Uses HTTPS instead of HTTP")
flag.add_argument("-v", "--version", default=False, action=argparse.BooleanOptionalAction, help="Version number and other important information")

args = flag.parse_args()

#get around some ips systems
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}

# I use these to handle various situations
stopSubDomain = 0
useProtocol = 0
appWww = 0

# Initializing list and variables
subList = ""
finalList = ""
protocol = ""
version = "0.0.2"

# These are used for the z switch
secured = "https://"
insecured = "http://"

if args.version != False:
    print(f"{version}\nJustin Powell\nNo Warranty Implied or Expressed")
    exit(0)

# If not given, then it runs the urls as http. Will have to pass the -z switch if they don't have https redirects
if args.secured != False:
    protocol = secured
else:
    protocol = insecured

# If no url is given, it will fail. It also trys to handle a few different ways urls are given. Will still fail if http(s) is given
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

# Handles subdomains, iterates over them, makes a list out of successful ones
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
                    requests.get(sUrl, headers=headers)
                except requests.ConnectionError:
                    pass
                else:
                    subList += f"{sUrl}\n"
                    finalList += f"{sUrl} :: {requests.status_codes}\n"
        except:
            print("Couldn't make subdomain list:\nFile likely not found")
    else:
        pass
else:
    print("Ignoring Subdomains")
    if appWww == 1:
        url = f"www.{url}"
    pass
print(finalList)

# Handles directories, if given. makes a list of them too
if args.directory != None:
    if useProtocol != 1:
        url = f"{protocol}{url}"
        subList += url
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
                    requests.get(dUrl, headers=headers)
                    finalList += f"{dUrl} :: {requests.status_codes}\n"
                except:
                    print("Error is dir block")
    except:
        print("Couldn't make directory list:\nFile likely not found")
else:
    print("Ignoring Directories")
    pass

finalList += "\n\nEnd of list"
print(finalList)
exit(0)
