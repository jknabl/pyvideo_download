import pprint
import lxml.html
import requests
import os
import re
# Set the (EXISTING) path where you want the videos downloaded
# e.g. /Users/me/Documents/videos/
#
# Leave blank to download to wherever you run this script from
DL_PATH = "/Users/jasonknabl/Documents/pycon-us-2011/"
PYVIDEO_URL = "http://pyvideo.org/category/7/pycon-us-2011/files"
# Begin logic

f = requests.get(PYVIDEO_URL)
parsed = lxml.html.document_fromstring(f.content)
XMLItems = parsed.cssselect("table.table td")
item_list = {}
#get links, make a dict.
for td in XMLItems:
    if td.cssselect("a"):
        for a in td.cssselect('a'):
            if a.text_content() == "video/mp4":
                item_list[curr_title] = a.attrib['href']
    else:
        curr_title = re.sub(r'\W+', '', td.text_content())
        curr_title = curr_title.encode('ascii', 'ignore')
        item_list[curr_title] = ""
#iterate through dict & pull video data
for talk in item_list:
    new_path = DL_PATH + talk
    if os.path.exists("%s.mp4" % new_path):
        print "Already downloaded %s.mp4. Skipping...\n---\n" % new_path
        continue
    print "Creating file: %s.mp4" % new_path
    with open('%s.mp4' % new_path, 'wb') as handle:
        print "File %s.mp4 created." % new_path
        print "Downloading and writing to %s.mp4..." % talk
        if item_list[talk] == "":
            print "NO URL: can't download.\n---\n"
            os.remove('%s.mp4' % new_path)
            continue
        try:
            req = requests.get(item_list[talk], stream=True)
        except OSError:
            print "Invalid filepath. Try a new one.\n---\n"
            continue
        for block in req.iter_content(1024):
            if not block:
                break
            handle.write(block)
        print "Success!\n---\n"
print "All done."

