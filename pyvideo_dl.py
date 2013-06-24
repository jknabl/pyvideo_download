#!/usr/bin/env python
import lxml.html
import requests
import os
import re
# Set the (EXISTING) path where you want the videos downloaded
# e.g. /Users/me/Documents/videos/
#im
# Leave blank to download to wherever you run this script from
DL_PATH = ""
PYVIDEO_URL = "http://pyvideo.org/category/7/pycon-us-2011/files"

def get_links(url):
    """Scrape a bunch of links from the given pyvideo url."""
    req_result = requests.get(url)
    parsed = lxml.html.document_fromstring(req_result.content)
    elements = parsed.cssselect("table.table td")
    item_list = {}
    for td in elements:
        if td.cssselect("a"):
            #column has links. find the video/mp4 links.
            for a in td.cssselect("a"):
                if a.text_content() == "video/mp4":
                    #this never scrapes before the video title, so
                    #dict is already initialized for this key
                    item_list[curr_title] = a.attrib['href']
        else:
            curr_title = re.sub(r'\W+', '', td.text_content()).encode('ascii', 'ignore')
            item_list[curr_title] = ""
    return item_list

def download_video(title, url):
    new_path = DL_PATH + title
    if os.path.exists("%s.mp4" % new_path):
        print "Already downloaded %s.mp4. Skipping...\n---\n" % new_path
        return None
    print "Creating file: %s.mp4" % new_path
    with open("%s.mp4" % new_path, "wb") as the_file:
        print "File %s.mp4 created. Downloading and writing..." % new_path
        if url == None:
            print "No URL, can't download...\n---\n"
            os.remove("%s.mp4" % new_path)
            return None
        try:
            req = requests.get(url, stream=True)
        except OSError:
            #TODO: this is silly, we can get rid of this by checking +
            #creating the path at the function's beginning.
            print "Invalid filepath. Try a new one.\n---\n"
            return None
        for block in req.iter_content(1024):
            if not block:
                break
            the_file.write(block)
        print "Success!\n---\n"
    return True

def main():
    urls = get_links(PYVIDEO_URL)
    for talk in urls:
        if urls[talk] != "": download_video(talk, urls[talk])
    print "All done."

if __name__=='__main__':
    main()
