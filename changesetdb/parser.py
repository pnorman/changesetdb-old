import os
import xml.sax
from changesetdb.changeset import Changeset, ChangesetHandler
from changesetdb.user import UserHandler, User


class Parser:
    def __init__(self, diff_mode, database):
        self.diff_mode = diff_mode
        assert(not diff_mode)
        self.database = database

    def load(self, file):
        decompressed = None
        if os.path.splitext(file.name)[1] == '.bz2':
            import bz2
            decompressed = bz2.BZ2File(file)
        else:
            decompressed = file

        parser = xml.sax.make_parser(['xml.sax.xmlreader.IncrementalParser'])
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        user_handler = UserHandler(self.database)
        changeset_handler = ChangesetHandler(self.database)
        handler = OsmHandler(changeset_handler, user_handler)
        parser.setContentHandler(handler)
        self.database.lock()
        parser.parse(decompressed)


class OsmHandler(xml.sax.ContentHandler):
    def __init__(self, changeset_handler, user_handler):
        self.changeset_handler = changeset_handler
        self.user_handler = user_handler

    changeset_attributes = {}
    changeset_tags = {}

    def startElement(self, tag, attributes):
        if tag == 'changeset':
            # Handle the user by itself since it has its own table
            if "uid" in attributes:
                self.user_handler.add(User(attributes.get("user"),
                                           attributes.get("uid")))
            # Store other changeset attributes until endElement
            self.changeset_attributes = attributes
        elif tag == 'tag':
            self.changeset_tags[attributes["k"]] = attributes["v"]

    def endElement(self, tag):
        if tag == 'changeset':
            self.changeset_handler.add(Changeset(self.changeset_attributes,
                                                 self.changeset_tags))
            self.changeset_attributes = {}
            self.changeset_tags = {}
