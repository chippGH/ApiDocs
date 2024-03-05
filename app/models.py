from sqlalchemy import Integer, Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship, backref, attribute_mapped_collection

from app import db


class DocNode(db.Model):
    __tablename__ = 'api_doc'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('api_doc.id'))
    name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    link = Column(String(255), nullable=False)
    children = relationship('DocNode',
                            # cascade deletions
                            cascade="all",

                            # many to one + adjacency list - remote_side
                            # is required to reference the 'remote'
                            # column in the join condition.
                            backref=backref("parent", remote_side='DocNode.id'),

                            # children will be represented as a dictionary
                            # on the "name" attribute.
                            #collection_class=attribute_mapped_collection('name'),
                            )

    def __init__(self, name, content, link, parent=None):
        self.name = name
        self.content = content
        self.link = link
        self.parent = parent

    def append(self, nodename, content, link):
        self.children.append(DocNode(nodename, content, link, parent=self))

    def get_tree(self):
        def custom_enumerate(numerable):
            n = 0
            for item in numerable:
                yield n, item

        res = {'title': self.name, 'link': self.link}
        children = self.children
        if children:
            res['children'] = []
            for e, child in custom_enumerate(children):
                res['children'].append(child.get_tree())
        return res

    def __repr__(self):
        return f"DocNode(name={self.name}, id={self.id}, parent_id={self.parent_id})"


'''flask shell
from app import db
from app.models import *
node = DocNode('root', 'content')
'''
