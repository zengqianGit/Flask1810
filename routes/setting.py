from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board


main = Blueprint('setting', __name__)


@main.route("/")
def index():
    # u = current_user()
    # t = new_csrf_token()
    # return render_template('setting.html', user=u, token=t)    board_id = int(request.args.get('board_id', -1))
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    u = current_user()
    return render_template("setting.html", ms=ms, token=token, bs=bs, bid=board_id, user=u)


@main.route("/update", methods=["POST"])
@csrf_required
def update():
    form = request.form
    u = current_user()
    if 'name' in form:
        User.update(u.id, username=form['name'])
        User.update(u.id, signature=form['signature'])
    elif 'old_pass' in form:
        if User.salted_password(form['old_pass']) == u.password:
            password = User.salted_password(form['new_pass'])
            User.update(u.id, password=password)
    return redirect(url_for('.index'))

