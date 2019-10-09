#!/usr/bin/env python
# encoding: utf-8

from urllib.parse import urlparse
import json
import os
import sys
import unittest
import glob


def url_validator (url):
    """validate the format of a URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


class TestVerifypublications (unittest.TestCase):
    ALLOWED_FIELDS = set([
            "title",
            "datasets",
            "original"
            ])

# ALLOWED_FIELDS = set([
#             "alt_ids",
#             "keywords",
#             "date",
#             "doi",
#             "title",
#             "url",
#             "journal",
#             "publisher",
#             "related_dataset"
#             ])


    def test_logins_or_something(self):
        return None
    
    def setUp(self):
        """load the publications list"""
        self.publications = []
        filename = os.path.join('/Users/sophierand/RCPublications/',self.filename)
        # filename = os.path.join('/Users/sophierand/RCPublications/partitions/',self.filename)
        with open(filename, "r") as f:
            self.publications = json.load(f)


    def test_file_loaded (self):
        print("\n{} publications loaded".format(len(self.publications)))
        self.assertTrue(len(self.publications) > 0)


    def test_has_required_fields (self):
        for publication in self.publications:
            if not set(["title", "datasets"]).issubset(publication.keys()):
                raise Exception("{}: missing required fields".format(publication["id"]))


    def test_has_valid_url (self):
        for publication in self.publications:
            if "url" in publication:
                url = publication["url"]

                if url == "" or not url:
                    pass
                elif not url_validator(url):
                    raise Exception("{}: badly formed URL {}".format(publication["title"], url))


    def test_each_field (self):
        for publication in self.publications:
            for key in publication.keys():
                if key not in self.ALLOWED_FIELDS:
                    raise Exception("{}: unknown field name {}".format(publication["title"], key))


    def test_unique_titles (self):
        print('testing {} file now'.format(self.filename))
        title_set = set([])

        for publication in self.publications:
            title = publication["title"]

            if title in title_set:
                raise Exception("{}: duplicate title {}".format(publication["title"], title))
            else:
                title_set.add(title)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # TestVerifypublications.filename = os.path.join('/Users/sophierand/RCPublications/partitions/',sys.argv.pop())
        TestVerifypublications.filename = sys.argv.pop()
        # filename = os.path.join('/Users/sophierand/RCPublications/partitions/',self.filename)
        # MyTest.PASSWORD = sys.argv.pop()
    unittest.main()
