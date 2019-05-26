from json import dumps

from flask import Response, render_template, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user
from hashlib import md5

from goo_gl__2_0 import app
from goo_gl__2_0.config import BaseConfig
from goo_gl__2_0.decorators import add_session_decorator, add_user_id
from goo_gl__2_0.constants import BlankConstants
from goo_gl__2_0.forms import LoginForm, RegistrationForm
from goo_gl__2_0.models import User, Link


def make_landing_identificator(numb, base=len(BlankConstants.NUMB_SYSTEM_MAP)):
    out_str = ''
    while True:
        if numb < base:
            return BlankConstants.NUMB_SYSTEM_MAP[numb] + out_str
        out_str = BlankConstants.NUMB_SYSTEM_MAP[numb % base] + out_str
        numb = numb // base


def validate_url(url):
    if not url:
        return False
    http_url_matches = BlankConstants.URL_VALIDATE_REGEX.match(url)
    if http_url_matches:
        return True
    else:
        return False


def repair_url(url):
    if validate_url(url):
        return url
    else:
        if validate_url('http://' + url):
            return 'http://' + url
        url_address = BlankConstants.PARTIAL_HTTP_REGEX.sub('', url)
        url_address = 'http://' + url_address
        if validate_url(url_address):
            return url_address
        else:
            return False


def throw_error_in_response(status_constant):
    response = (BlankConstants.JSON_STATUSES[status_constant])
    response = {'status': response}
    response = dumps(response, separators=(',', ':'))
    return Response(response, mimetype='application/json')


@app.route('/')
@app.route('/index/')
@add_user_id
def index_web_page(**kwargs):
    user_id = kwargs['current_user_id']
    if user_id == '0':
        checkbox_display = 'none'
    else:
        checkbox_display = 'inline'
    return render_template('index.html',
                           additional_script='var user_id = ' + user_id + ';',
                           style='../static/css/s.css',
                           display_private_checkbox=checkbox_display,
                           display_pstat=current_user.is_authenticated,
                           display_login=not current_user.is_authenticated,
                           display_logout=current_user.is_authenticated,
                           script='../static/js/s.js')


@app.route('/stat/')
@app.route('/pstat/')
@add_user_id
def stat_web_page(**kwargs):
    user_id = kwargs['current_user_id']
    return render_template('stat.html',
                           additional_script='var user_id = ' + user_id + ';',
                           style='../static/css/stat.css',
                           display_pstat=current_user.is_authenticated,
                           display_login=not current_user.is_authenticated,
                           display_logout=current_user.is_authenticated,
                           script='../static/js/stat.js')


@app.route('/login/', methods=['GET', 'POST'])
@add_session_decorator
@add_user_id
def login_web_page(**kwargs):
    user_id = kwargs['current_user_id']
    session = kwargs['session']
    if current_user.is_authenticated:
        return redirect(url_for('index_web_page'))
    form = LoginForm()
    if form.is_submitted():
        if not form.username.data or not form.password.data:
            return redirect(url_for('login_web_page', errorcode=4))
        user = session.query(User). \
            filter_by(username=form.username.data). \
            first()
        if user is None:
            return redirect(url_for('login_web_page', errorcode=2))
        if not user.check_password(form.password.data):
            return redirect(url_for('login_web_page', errorcode=1))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index_web_page'))
    return render_template('login.html',
                           additional_script='var user_id = ' + user_id + ';',
                           style='../static/css/login.css',
                           script='../static/js/login.js',
                           form=form)


@app.route('/registration/', methods=['GET', 'POST'])
@add_session_decorator
@add_user_id
def registration_web_page(**kwargs):
    user_id = kwargs['current_user_id']
    session = kwargs['session']
    if current_user.is_authenticated:
        return redirect(url_for('index_web_page'))
    form = RegistrationForm()
    if form.is_submitted():
        if not form.username.data or not form.password.data:
            return redirect(url_for('registration_web_page', errorcode=4))
        user = session.query(User). \
            filter_by(username=form.username.data). \
            first()
        if user:
            return redirect(url_for('registration_web_page', errorcode=3))

        password = form.password.data.encode('utf-8')
        pwd_hash = md5(password).hexdigest()
        new_user = User(username=form.username.data, pwd_hash=pwd_hash)
        session.add(new_user)
        session.commit()

        login_user(new_user, remember=form.remember_me.data)
        return redirect(url_for('index_web_page'))
    return render_template('registration.html',
                           additional_script='var user_id = ' + user_id + ';',
                           style='../static/css/login.css',
                           script='../static/js/login.js',
                           form=form)


@app.route('/logout/')
def logout_web_page():
    logout_user()
    return redirect(url_for('index_web_page'))


@app.route('/s/')
@add_session_decorator
def save_link_web_page(**kwargs):
    session = kwargs['session']
    redirect_link = request.args.get('link')
    user_id = request.args.get('user_id')
    validate_answer = repair_url(redirect_link)
    if not validate_answer:
        return throw_error_in_response(BlankConstants.JSON_STATUS_INVALID_INPUT)
    if user_id is not None and user_id.isdigit():
        user_id = int(user_id)
    else:
        return throw_error_in_response(BlankConstants.JSON_STATUS_INVALID_INPUT)
    new_link = Link(landing='wait', redirect=validate_answer,
                    views=0, user_id=user_id)
    session.add(new_link)
    session.commit()
    landing = make_landing_identificator(new_link.id)
    new_link.landing = landing
    session.commit()
    response = {
        'status': BlankConstants.JSON_STATUSES[BlankConstants.JSON_STATUS_OK],
        'landing_url': BaseConfig.SITE_ADDRESS +
                       BaseConfig.REDIRECT_PATH +
                       landing
    }
    response = dumps(response)
    return Response(response, mimetype='application/json')


@app.route('/r/<landing>')
@add_session_decorator
def redirect_web_page(landing, **kwargs):
    session = kwargs['session']
    db_link_item = session.query(Link). \
        filter_by(landing=landing). \
        first()
    if db_link_item and db_link_item.redirect:
        redirect_url = db_link_item.redirect
        db_link_item.views += 1
        session.commit()
        return redirect(redirect_url)
    else:
        abort(404)


@app.route('/g/json')
@add_session_decorator
def get_items_web_page(**kwargs):
    session = kwargs['session']
    start_by = request.args.get('start_by')
    item_limit = request.args.get('limit')
    user_id = request.args.get('user_id')
    is_sort = request.args.get('is_sort')
    if user_id and user_id.isdigit():
        user_id = int(user_id)
    else:
        return throw_error_in_response(BlankConstants.JSON_STATUS_INVALID_INPUT)
    if is_sort:
        item_list = session.query(Link). \
            order_by(Link.views.desc()). \
            filter(Link.userID == user_id). \
            offset(start_by). \
            limit(item_limit). \
            all()
    else:
        item_list = session.query(Link). \
            filter(Link.id >= start_by). \
            filter(Link.userID == user_id). \
            limit(item_limit)
    response_dict = {}
    item_container_dict = []
    if not item_list:
        return throw_error_in_response(BlankConstants.JSON_STATUS_DATA_NOT_FOUND)
    response_dict['status'] = BlankConstants.JSON_STATUSES[BlankConstants.JSON_STATUS_OK]
    for item in item_list:
        db_item = {
            'id': item.id,
            'landing': item.landing,
            'redirect': item.redirect,
            'views': item.views
        }
        item_container_dict.append(db_item)
    response_dict['items'] = item_container_dict
    json_response = dumps(response_dict, separators=(',', ':'))
    return Response(json_response,
                    mimetype='application/json')
