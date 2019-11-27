#!/usr/bin/env python
# encoding: utf-8

from urllib.parse import urlparse
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
            with open(partition, "r") as f:
                self.publications.extend(json.load(f))


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
        subdir = "partitions"
        PARTITIONS = [ "/".join([subdir, name]) for name in os.listdir(subdir) ]

    print(PARTITIONS)
    unittest.main()
