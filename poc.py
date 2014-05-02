from wikitools import wiki
from wikitools import api
import os.path

# List of chapters to build into the subject
# chapters = ["Category:Tata"]
categories = ["Category:Artificial_intelligence","Category:Optics", "Category:Mechanics", "Category:Computer_science", "Category:Operating_systems", "Category:Software", "Category:Computer_networks", "Category:Software_engineering", "Category:Systems_engineering", "Category:Computer_programming", "Category:Computer_security"]

# Fetch chapters from Wikipedia
site = wiki.Wiki("http://en.wikipedia.org/w/api.php")

params = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "",
    "cmtype": "page",
    "cmlimit": 400
}

for category in categories:
    params["cmtitle"] = category
    req = api.APIRequest(site, params)
    data = req.query()

    articles = [(art['pageid'], art['title']) for art in data['query']['categorymembers']]
    i = 0
    for art in articles:
        pageid = art[0]
        title = art[1]
        print "Loading '%s' into '%s'" % (title, category)
        p = {
            "action": "query", 
            "pageids": pageid, 
            "prop": "revisions", 
            "rvprop": "content", 
            "format": "jsonfm"
        }
        r = api.APIRequest(site, p)
        d = r.query()     
        body = d['query']['pages'][str(pageid)]['revisions'][0]['*']

        subdirectory="data/"+category

        body = body.encode('ascii','ignore')

        title = title.replace('/','-')

        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)
        text_file = open(os.path.join(subdirectory, title + ".txt"), "w+")

        text_file.write(body)

        text_file.close()
        # print body # To be persisted onto a file