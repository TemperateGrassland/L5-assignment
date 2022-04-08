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
        'SELECT f.id, f.left_entity, f.relation_entity, f.right_entity, user.username, user.userid, user.admin  FROM fact f JOIN user ON f.author_id = user.userid  ORDER BY id DESC'
    ).fetchall()

    # print("the requests args are: ")
    # print(request.get_data())


    # for row in facts_and_users:
    #
    #     print("ID: " + str(row[0]))
    #     print("LEFT: " + row[1])
    #     print("RELATION: " + row[2])
    #     print("RIGHT: " + row[3])
    #     print("USERNAME: " + row[4])
    #     print("USERID: " + str(row[5]))

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
        'SELECT fact.id, fact.left_entity, fact.relation_entity, fact.right_entity, user.userid FROM fact JOIN user ON fact.author_id = user.userid WHERE id = ?',
        (id,)
    ).fetchone()

    if fact is None:
        abort(404, f"Fact id {id} doesn't exist.")
    # todo why is the userid key missing?
    #     if check_author and fact['userid'] != g.user['id']:
    #         abort(403)

    return fact


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    fact = get_fact(id)
    print("fact id is: ")
    print(fact[0])
    print("fact left is: ")
    print(fact[1])


    if request.method == 'POST':
        print("the update requests args are: ")
        print(request.get_data())
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
                'UPDATE fact SET left_entity = ?, relation_entity = ?, right_entity = ? WHERE id = ?',
                (left_entity, relation, right_entity, id)
            )
            db.commit()
            return redirect(url_for('fact.index'))

    return render_template('fact/update.html', fact=fact)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_fact(id)
    db = get_db()
    db.execute(
        'DELETE FROM fact WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('fact.index'))
