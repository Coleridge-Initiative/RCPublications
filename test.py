#!/usr/bin/env python
# encoding: utf-8

from pathlib import Path
from urllib.parse import urlparse
import codecs
import json
import os
import sys
import unittest


PARTITIONS = []


def url_validator (url):
    """validate the format of a URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


class TestVerifyPublications (unittest.TestCase):
    ALLOWED_FIELDS = set([
            "title",
            "datasets",
            "original"
            ])


    def allow_arg (self):
        return None
    

    def setUp (self):
        """load the publications list"""
        self.publications = []

        for partition in PARTITIONS:
            with codecs.open(partition, "r", encoding="utf8") as f:
                try:
                    part = json.load(f)
                    self.publications.extend(part)
                except:
                    print(f"failing partition read: {partition}")
                    sys.exit(-1)


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
                    raise Exception("{}: unknown field name {} in publication {}".format(publication["title"], key,publication))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PARTITIONS.append(sys.argv.pop())
    else:
        PARTITIONS = [ p for p in Path("partitions").glob("*.json") ]

    #print(PARTITIONS)
    unittest.main()
