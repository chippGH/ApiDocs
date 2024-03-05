from os import PathLike

from app import db, app
from app.models import DocNode

PAGE_NAME = 'СНМ'
PAGE_LINK = 'dsu'
TEXT_FILE: PathLike | str = 'app/views-test.html'

UPDATE = True

ROOT_LINK = 'olimpic'

with open(TEXT_FILE, 'r', encoding='UTF-8') as r:
    text = ''.join(r.readlines())

with app.app_context():
    if UPDATE:
        node = db.session.query(DocNode).filter_by(link=PAGE_LINK).first()
        node.name = PAGE_NAME
        node.content = text
        db.session.add(node)
        db.session.commit()
    else:
        root = db.session.query(DocNode).filter_by(link=ROOT_LINK).first()
        node = DocNode(PAGE_NAME, text, PAGE_LINK, root)
        db.session.add(node)
        db.session.commit()
