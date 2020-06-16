"""
It downloads web-pages and does stuff
"""
import logging
import os
import re
from shutil import rmtree
from urllib.parse import *

import requests as r

oLoc, TEMP_FOLDER = os.getcwd(), "htmlDL TEMP"


def getPage(fullURL):
    validateURL(fullURL)
    return r.get(fullURL)


def download(fullURL, fileName=None, dirName="htmlDL"):
    fullURL: str
    if not validateURL(fullURL): return False
    logging.info("Downloading HTML file...")
    x = r.get(fullURL)
    logging.debug("Filename checks...")
    os.chdir(oLoc)
    if fileName is None:
        parsed = urlparse(fullURL)
        try:
            fileName = str(re.search(r'\s*<title>(.+)</title>\s*', x.text, re.IGNORECASE).group(1))
            if re.search(r'(<title>|</title>)', fileName): fileName = re.sub(r'(<title>|</title>)+.*', '', fileName)
            if len(fileName) >= 255: raise Exception("File name is too long")
        except (AttributeError, Exception):
            logging.exception("Unable to find title or file too long")
            fileName = parsed.path.split("/")[-1] if parsed.path != "" else "index"
            fileName = fileName[:-1] if fileName.endswith("/") else fileName
        folders = [dirName, parsed.netloc]
        folders.extend(parsed.path.split("/"))
        if not str(parsed.path).rfind("."): folders = folders[:-1]
        for f in folders:
            if not f: continue
            if not os.path.isdir(f): os.mkdir(f)
            os.chdir(f)
        fileName = re.sub(r'[^\x00-\x7F]+', '_', fileName)
    logging.info("Writing HTML file...")
    try:
        open(fileName, "w").write(x.text)
    except FileNotFoundError:
        logging.exception("Unable to save")
    logging.info("Finished")
    return fileName


def validateURL(fullURL):
    logging.debug("Validating URL...")
    try:
        if re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', fullURL) != '':
            logging.debug("URL is valid")
            return True
        else:
            logging.warning("URL is invalid")
            return False
    except (TypeError,):
        logging.exception("Unable to verify URL")
        return False


def findURLs(fullURL, allowExternalDomains=False, dirName=TEMP_FOLDER):
    fileName = download(fullURL, dirName=dirName)
    urls = list(dict.fromkeys(
            re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                       open(fileName).read())))
    if not allowExternalDomains:
        domain = urlparse(fullURL).netloc
        for i in urls:
            if urlparse(i).netloc != domain: urls.remove(i)
    logging.info("Finished finding URLs")
    return urls


def downloadAllOnPage(fullURL, allowExternalDomains=False):
    # check again until there's no more
    folder_name = "htmlDL Tree Download"
    urls, newURL, domain = list(dict.fromkeys(findURLs(fullURL, dirName=folder_name))), [], urlparse(fullURL).netloc
    for i in urls:
        logging.info("Checking {}...".format(i))
        if (urlparse(i).netloc == domain and not allowExternalDomains) or allowExternalDomains:
            logging.info("OK")
            newURL.extend(findURLs(i, allowExternalDomains))
        else:
            logging.info("Domain does not match")
    for i in newURL:
        logging.info("Downloading {}".format(i))
        download(i, dirName=folder_name)
    os.chdir(oLoc)
    rmtree(TEMP_FOLDER)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    downloadAllOnPage("https://www.google.com")
