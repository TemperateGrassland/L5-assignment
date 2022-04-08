from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from factr.auth import login_required
from factr.db import get_db

bp = Blueprint('fact', __name__)


@bp.route('/')
def index():
    db = get_db()
    facts_and_users = db.execute(
        'SELECT f.id, f.left_entity, f.relation_entity, f.right_entity, user.username, user.userid  FROM fact f JOIN user ON f.author_id = user.userid  ORDER BY id DESC'
    ).fetchall()

    print("factanduserstext: ")
    print(facts_and_users.text)

    for row in facts_and_users:

        print("ID: " + str(row[0]))
        print("LEFT: " + row[1])
        print("RELATION: " + row[2])
        print("RIGHT: " + row[3])
        print("USERNAME: " + row[4])
        print("USERID: " + str(row.text))

    # print(str(facts_and_users)[1:-1])
    # print(facts_and_users.pop())
    return render_template('fact/index.html', facts=facts_and_users)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        left_entity = request.form['left_entity']
        relation_entity = request.form['relation_entity']
        right_entity = request.form['right_entity']
        error = None

        if not left_entity:
            error = 'Left Entity is required.'

        if not relation_entity:
            error = 'Relation Entity is required.'

        if not right_entity:
            error = 'Right Entity is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO fact (left_entity, relation_entity, right_entity, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (left_entity, relation_entity, right_entity, g.user['userid'])
            )
            db.commit()
            return redirect(url_for('fact.index'))

    return render_template('fact/create.html')


def get_fact(id, check_author=True):
    fact = get_db().execute(
        'SELECT f.id, left_entity, relation_entity, right_entity, userid'
        ' FROM fact f JOIN user d ON f.author_id = d.userid'
        # ' WHERE f.id = ?',
        # id
        # 'SELECT p.id, title, body, created, author_id, username'
        # ' FROM post p JOIN user u ON p.author_id = u.id'
        # ' WHERE p.id = ?',
    ).fetchone()

    if fact is None:
        abort(404, f"Fact id {id} doesn't exist.")
    # todo why is the author_id key missing?
    #     if check_author and fact['author_id'] != g.user['id']:
    #         abort(403)

    return fact


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_fact(id)

    if request.method == 'POST':
        left_entity = request.form['left_entity']
        relation = request.form['relation_entity']
        right_entity = request.form['right_entity']
        error = None

        if not left_entity:
            error = 'Left entity is required.'

        if not relation:
            error = 'relation is required.'

        if not right_entity:
            error = 'Right entity is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                # TODO update query
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('fact.index'))

    return render_template('fact/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_fact(id)
    db = get_db()
    # todo update query
    db.execute(
        'DELETE FROM fact WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('fact.index'))
