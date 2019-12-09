#!/usr/bin/env python
# encoding: utf-8

from urllib.parse import urlparse
import glob
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
        self.publications = {}

        for partition in PARTITIONS:
            with open(partition, "r") as f:
                print("loading: {}".format(partition))
                self.publications[partition] = json.load(f)[0]


    def test_file_loaded (self):
        print("\n{} publications loaded".format(len(self.publications)))
        self.assertTrue(len(self.publications) > 0)


    def test_has_required_fields (self):
        for partition, publication in self.publications.items():
            if not set(["title", "datasets"]).issubset(publication.keys()):
                raise Exception("{}: missing required fields\n{}".format(publication["id"], partition))


    def test_has_valid_url (self):
        for partition, publication in self.publications.items():
            if "url" in publication:
                url = publication["url"]

                if url == "" or not url:
                    pass
                elif not url_validator(url):
                    raise Exception("{}: badly formed URL {}\n{}".format(publication["title"], url, partition))


    def test_each_field (self):
        for partition, publication in self.publications.items():
            for key in publication.keys():
                if key not in self.ALLOWED_FIELDS:
                    raise Exception("{}: unknown field name {}\n{}".format(publication["title"], key, partition))


    def test_original_fields (self):
        for partition, publication in self.publications.items():
            if "original" in publication.keys():
                orig = publication["original"]

                for key in ["url", "doi", "pdf", "journal"]:
                    if key in orig:
                        if not orig[key] or not isinstance(orig[key], str):
                            print(orig)
                            raise Exception("{}: bad value for {}\n{}".format(publication["title"], partition))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PARTITIONS.append(sys.argv.pop())
    else:
        subdir = "partitions"

        for partition in glob.glob(subdir + "/*.json"):
            PARTITIONS.append(partition)

    unittest.main()
