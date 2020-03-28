import urllib
from bs4 import BeautifulSoup, NavigableString
from tags import tags
import json

class Element:
    def __init__(self, tag, attr, has_global, has_events):
        self.tag = tag
        self.attr = attr
        self.has_global = has_global
        self.has_events = has_events

    def to_dict(self):
        return { "tag": self.tag, "attr": self.attr, "has_global": self.has_global, "has_events": self.has_events }

def make_soup(url):
    html = urllib.request.urlopen(url)
    #with open("a_tag.html") as fp:
    #   html = fp.read()
    return BeautifulSoup(html, features="lxml")
    

def make_tag_link(base, tag):
    return base + 'tag_' + tag + '.asp'

def process(tag, tag_soup):

    has_global = tag_soup.find(string='Global Attributes') is not None
    has_events = tag_soup.find(string='Event Attributes') is not None

    table = tag_soup.find(id='table1')
    if table is None:
        return Element(tag, [], has_global, has_events)
    
    rows = table.find_all('tr')
    iter = 0
    attributes = []
    
    for row in rows[1:]:
        ch = row.find_all('td')
        link = ch[0].find('a')
        if link is None:
            continue
        css_class = link.get('class')
        if css_class is not None and css_class[0] == 'notsupported':
            continue
        attributes.append(link.contents[0])

    return Element(tag, attributes, has_global, has_events)

def main():
    base = 'https://www.w3schools.com/tags/'
    root = base + 'default.asp'
    root_soup = make_soup(root)

    elements = []

    for tag in tags:
        print(tag)
        tag_soup = make_soup(make_tag_link(base, tag))
        elements.append(process(tag, tag_soup).to_dict())

    print(json.dumps(elements))

if __name__ == '__main__':
    main()
        
    
    

