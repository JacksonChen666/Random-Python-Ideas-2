"""
It downloads web-pages and does stuff
"""
import logging
import os
import re
import threading

import requests as r


def getPage(fullURL):
    validateURL(fullURL)
    return r.get(fullURL)


def download(fullURL, fileName=None, fileLoc="."):
    fullURL: str
    validateURL(fullURL)
    logging.info("Downloading HTML file")
    x = r.get(fullURL)
    logging.info("Downloaded")
    logging.debug("Filename checks...")
    if fileName is None:
        removeText = ["['<title>", "</title>']"]
        if re.findall('<title>[^*"?·<>]+</title>', x.text, re.IGNORECASE) != '':
            fileName = str(re.findall('<title>[^*"?·<>]+</title>', x.text, re.IGNORECASE))
        for i in removeText:
            fileName = fileName.replace(i, "")
    if fileLoc != "." and not os.path.isdir(fileLoc):
        os.mkdir(fileLoc)
    with open("{}/{}.html".format(str(fileLoc), str(fileName)), "w") as f:
        logging.info("Writing HTML file...")
        f.write(x.text)
        logging.info("Written HTML file")


def validateURL(fullURL):
    logging.debug("Validating URL...")
    if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fullURL) != '':
        logging.debug("URL is valid")
        return True
    else:
        logging.exception("URL is invalid")
        raise Exception("Invalid URL passed through input")


def validateEndURL(fullURL):
    logging.debug("Validating end of URL...")
    if fullURL.endswith("/"):
        logging.debug("Validated")
        return True
    else:
        logging.debug("Invalidated")
        return False


def findURLs(fullURL):
    validateURL(fullURL)
    logging.info("Downloading...")
    x = r.get(fullURL).text
    logging.info("Downloaded")
    logging.info("Finding URL...")
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', x)
    logging.info("Finished finding URLs")
    return urls


def treeDownload(fullURL, allowExternalDomains=False):
    # find urls, and put them all into a list, and check again until there's no more
    # also check if the domain is the same
    # after all of that, download all of then in a separate thread in a folder
    t = []
    urls = findURLs(fullURL)
    urlsAlt = [urlss for urlss in urls]
    for i in range(len(urlsAlt)):
        logging.info("Checking {}...".format(urls[i]))
        if urlsAlt[i].startswith(fullURL) and allowExternalDomains:
            urls.append(findURLs(urlsAlt[i]))
            logging.info("OK (Domain matches)")
        elif not allowExternalDomains:
            urls.append(findURLs(urlsAlt[i]))
            logging.info("OK")
        else:
            logging.info("Domain does not match")
    urls = [urlss for urlss in urls]
    for i in range(len(urls)):
        t.append(threading.Thread(target=download, args=(urls[i], None, "tree download")))
        t[i].start()
        logging.info("Started thread-{}".format(i))
    print(urls)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    print("Hello there, console")
    download("https://jacksonchen666.github.io/", fileLoc="Downloads")
