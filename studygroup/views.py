from flask import (g, request, redirect, render_template,
                   session, url_for, jsonify, Blueprint)

from .models import User, Group
from .application import db, meetup
from .auth import login_required
from .messaging import  send_message

studygroup = Blueprint("studygroup", __name__, static_folder='static')


@studygroup.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
    else:
        g.user = None


@studygroup.route('/')
def index():
    return render_template(
        'index.html', groups=Group.all_actives()
    )


@studygroup.route('/members')
@studygroup.route('/members/<int:offset>')
@login_required
def show_members(offset=None):
    g.users = User.query.all()
    return render_template('members.html')

    # if 'meetup_token' in session:
    #     if offset is None:
    #         offset = 0
    #
    #     me = meetup.get(
    #         '2/members',
    #         data={
    #             'group_id': settings.MEETUP_GROUP_ID,
    #             'page': 20,
    #             'offset': offset
    #         })
    #
    #     return render_template(
    #         'members.html',
    #         members=me.data['results'],
    #         next_offset=offset + 1)
    #
    # return redirect(url_for('.login'))


@studygroup.route('/send_message/<int:member_id>', methods=['GET', 'POST'])
def send_message(member_id):
    if 'meetup_token' not in session:
        return redirect(url_for('.login'))

    if request.method == 'GET':
        member = meetup.get('2/member/%s' % member_id)
        return render_template("send_message.html", member=member.data)
    elif request.method == 'POST':
        response = send_message(
            request.form['subject'],
            request.form['member_id'],
            request.form['message']
        )
        return jsonify(response.data)
    else:
        return "Invalid Request", 500


@studygroup.route('/boom')
def boom():
    raise Exception('BOOM')


@studygroup.route('/login')
def login():
    return meetup.authorize(callback=url_for('.authorized', _external=True))


@studygroup.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.index'))


@studygroup.route('/login/authorized')
@meetup.authorized_handler
def authorized(resp):
    if resp is None or not isinstance(resp, dict):
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['meetup_token'] = (resp['access_token'], '')

    meetup_response = meetup.get('2/member/self')
    member_details = meetup_response.data
    member_id = str(member_details['id'])

    user = User.query.filter_by(meetup_member_id=member_id).first()
    if not user:
        user = User(
            full_name=member_details['name'],
            meetup_member_id=member_id
        )
        db.session.add(user)
        db.session.commit()
    session['user_id'] = user.id
    return redirect(url_for('.index'))


@meetup.tokengetter
def get_meetup_oauth_token():
    return session.get('meetup_token')
