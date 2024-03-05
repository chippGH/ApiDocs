from flask import render_template, send_file

from app import app, db
from app.models import DocNode


@app.route('/')
@app.route('/api')
@app.route('/api/')
@app.route('/api/<doc_link>')
def api_doc(doc_link='root'):
    tree = db.session.query(DocNode).first().get_tree()
    current_node = db.session.query(DocNode).filter_by(link=doc_link).first()
    if current_node is None:
        return "404"
    else:
        active_nodes = [current_node.link]
        next_node = current_node.parent_id
        while next_node is not None:
            new_node = db.session.query(DocNode).filter_by(id=next_node).first()
            active_nodes.append(new_node.link)
            next_node = new_node.parent_id
        return render_template('api_doc.html', title=current_node.name, doc_tree=tree, active_nodes=active_nodes,
                               content=current_node.content)


@app.route('/apiTest')
def api_doc_test():
    tree = db.session.query(DocNode).first().get_tree()
    with open('app/views-test.html', 'r', encoding='UTF-8') as f:
        return render_template('api_doc.html', title='test', doc_tree=tree, active_nodes=[],
                               content=''.join(f.readlines()))


@app.route('/favicon.ico')
def favicon():
    return send_file('static/images/favicon.png')
