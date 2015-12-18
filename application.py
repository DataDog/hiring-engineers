__author__ = 'stephenlechner'

# ***NB: This file is from another web app and will not run as a stand-alone
#    file. I include it here becuase it is the file I used to collect http
#    metrics for the Datadog hiring-engineers coding challenge.***


# run this file to run the catalog app locally on port 8000.
# this file contains the functions for interacting with the database (the
# CRUD operations) and all the Flask framework functions.
# The file uses the database set up in db_setup.py and relies on page_design.py
# for all html creation. The html content is styled with catalog.css.


import flask
import psycopg2
import random
import string
import httplib2
import json
import requests
import time
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from datadog import initialize, threadstats
from datadog.dogstatsd.base import DogStatsd

import page_design


def connect():
    return psycopg2.connect('dbname=catalog_db')


# create functions
def create_category(cat, user_string):
    db = connect()
    c = db.cursor()
    cat_name = cat
    if cat_name == '':
        cat_name = 'untitled'
    c.execute("INSERT INTO category (name, creator_id) VALUES(%s, %s);",
              (cat_name, user_string,))
    db.commit()
    db.close()


def add_item(item_name, cat, description, user_string, new_pic):
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO items(name, description, category_id, creator_id, pic_url) "
              "VALUES (%s, %s, %s, %s, %s);",
              (item_name, description, cat, user_string, new_pic))
    db.commit()
    db.close()


# read functions
def get_categories():
    db = connect()
    c = db.cursor()
    c.execute('SELECT * FROM category ORDER BY name;')
    res = c.fetchall()
    db.close()
    return res


def get_items_by_cat_id(cat_id):
    db = connect()
    c = db.cursor()
    c.execute("""
              SELECT items.id, items.name, items.creator_id, items.description
              FROM items WHERE items.category_id = %s;""",
              (cat_id,))
    res = c.fetchall()
    db.close()
    return res


def get_category_name(cat_id):
    db = connect()
    c = db.cursor()
    c.execute("SELECT name FROM category WHERE id = %s;", (cat_id,))
    res = c.fetchall()
    db.close()
    if res[0][0]:
        return res[0][0]
    else:
        return None


def get_item(item_id):
    db = connect()
    c = db.cursor()
    c.execute("""
              SELECT name, description, category_id, creator_id, pic_url FROM items
              WHERE id = %s;
              """, (item_id,))
    res = c.fetchall()
    db.close()
    if res[0]:
        return res[0]
    else:
        return None


# update functions
def edit_item(item_id, new_name, new_desc, new_cat_id, new_pic):
    db = connect()
    c = db.cursor()
    c.execute(
        """
        UPDATE items SET name = %s, description = %s, category_id = %s, pic_url = %s
        WHERE id = %s;
        """, (new_name, new_desc, new_cat_id, new_pic, item_id)
    )
    db.commit()
    db.close()


# destroy functions
def delete_category_by_id(cat_id):
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM items WHERE category_id = %s;", (cat_id,))
    c.execute("DELETE FROM category WHERE id = %s;", (cat_id,))
    db.commit()
    db.close()


def delete_item(item_id):
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    db.commit()
    db.close()


app = flask.Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read()
)['web']['client_id']



init_stuff = {
    'api_key':'b79f2e891614183a0a6fded2c1d2301b',
    'app_key':'catalog_app_key_test_1a5e2h8',
}

initialize(**init_stuff)

stats = threadstats.ThreadStats(constant_tags=['category_app'])
stad = DogStatsd()
stats.start()

@app.route('/catalog', methods=['GET', 'POST'])
def home():
    begin = time.time()
    tags = ['support']
    # grab user id if user is logged in
    user_id = ''
    if 'gplus_id' in flask.session:
        user_id = flask.session['gplus_id']

    # set defaults
    item_list = []
    cat_to_sel = ''
    desc_to_show = None
    please_edit_item = False
    saved_item = False

    # handle form responses. Code written in order of possible use
    if flask.request.method == 'POST':

        # 1. New Category
        if 'newcat' in flask.request.form:
            new_cat = flask.request.form['new_category']
            create_category(new_cat.strip(), user_id)
            tags += ['catalog:new_cat']
        else:
            for each in flask.request.form:
                # 2A. Delete Category
                if each[:6] == 'catdel':
                    cat_to_del = each[each.find('_')+1:each.rfind('_')]
                    delete_category_by_id(cat_to_del)
                    tags += ['catalog:cat_deleted']
                # 2B. Select Category
                elif (
                    each[:6] == 'catsel' or each[:5] == 'newit' or
                    each[:5] == 'itdel' or each[:5] == 'itsel' or
                    each[:4] == 'ited' or each[:5] == 'nited'
                ):
                    form_name = each[each.find('_')+1:each.rfind('_')]
                    if form_name.count('-') > 0:
                        cat_to_sel = form_name[form_name.rfind('-')+1:]
                        it_to_sel = form_name[:form_name.find('-')]
                    else:
                        cat_to_sel = form_name

                    # 3A. New Item in Selected Category
                    if each[:5] == 'newit':
                        new_it = flask.request.form['new_item']
                        new_it_desc = flask.request.form['new_item_desc']
                        new_pic = flask.request.form['new_pic']
                        add_item(new_it, cat_to_sel, new_it_desc, user_id,
                                 new_pic)
                        tags += ['catalog:new_item']
                    # 3B. Delete Item in Selected Category
                    elif each[:5] == 'itdel':
                        delete_item(it_to_sel)
                    # 3C. Select Item (for/not for edit) in Selected Category
                    elif each[:5] == 'itsel' or each[:4] == 'ited':
                        item_stuff = get_item(it_to_sel)
                        desc_to_show = item_stuff[1]
                        item_name = item_stuff[0]
                        if each[:4] == 'ited':
                            please_edit_item = True
                    # 3D. Edit Item in Selected Category
                    elif each[:5] == 'nited':
                        ed_it_desc = flask.request.form['desc_edit']
                        ed_it_name = flask.request.form['it_name']
                        ed_it_cat = flask.request.form['cat_edit']
                        ed_it_pic = flask.request.form['pic_edit']
                        edit_item(it_to_sel, ed_it_name, ed_it_desc, ed_it_cat,
                                  ed_it_pic)
                        # item_stuff = get_item(it_to_sel)
                        # desc_to_show = item_stuff[1]
                        item_name = get_item(it_to_sel)[0]
                        saved_item = True
                        tags += ['catalog:item_edited']

                    # all in 2B or above require getting items from a selected
                    #     category
                    item_list = get_items_by_cat_id(cat_to_sel)
                    if item_list == []:
                        # setting to None will trigger 'no categories' message
                        item_list = [None]

    # Make page content
    page_content = page_design.make_page_header(user_id)
    cats = get_categories()
    page_content += page_design.make_category_content(cats, user_id)

    # If Category selected, make item list content
    if cat_to_sel != '':
        page_content += page_design.make_item_content(
            get_category_name(cat_to_sel), item_list, cat_to_sel, user_id
        )
        # If Item selected/edited, make description content
        if saved_item is True:
            page_content += page_design.make_saved_item(item_name)
        elif desc_to_show is not None:
            page_content += page_design.make_description(
                it_to_sel, item_stuff, cat_to_sel,
                please_edit_item, cats, user_id
            )
        else:
            page_content += '<td width="33%"><td>'
    page_content += '</tr></table></body>'
    if tags == ['support']:
        tags += ['catalog:home']
    # Datadog Add: page counting increments
    stats.increment('home.page.hits', tags=tags)
    stad.increment('page.views', tags=tags)
    stats.gauge('process.runtime', time.time() - begin, tags=tags)
    stats.histogram('home.page.hits', 1, tags=tags)
    stats.histogram('user.query.seconds', time.time() - begin, tags=tags)

    return flask.render_template_string(page_content)


@app.route('/catalog/login', methods=['GET', 'POST'])
def login():
    begin = time.time()
    # set randomly generated login token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    flask.session['state'] = state
    # create login page
    content = page_design.login_content

    stats.increment('home.page.hits', tags=['support', 'catalog:login'])
    stad.increment('page.views', tags=['support', 'catalog:login'])
    stats.gauge(
        'process.runtime', time.time() - begin,
        tags=['support', 'catalog:login']
    )
    stats.histogram('home.page.hits', 1, tags=['support', 'catalog:login'])
    stats.histogram(
        'user.query.seconds', time.time() - begin,
        tags=['support', 'catalog:login']
    )

    return flask.render_template_string(content, STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # conducts the google plus log in
    # check to make sure the user code matches
    if flask.request.args.get('state') != flask.session['state']:
        response = flask.make_response(
            json.dumps('Invalid state parameter'), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    code = flask.request.data
    try:
        # turn authorization code into credential object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = flask.make_response(
            json.dumps('Failed to turn the authcode to cred.'), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    # make sure credentials has valid access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if error with access token, abort
    if result.get('error') is not None:
        response = flask.make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # make sure access token is the correct one
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = flask.make_response(
            json.dumps("Token user id does not match the given user id."), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response
    # see if user already logged in
    stored_credentials = flask.session.get('credentials')
    stored_gplus_id = flask.session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = flask.make_response(
            json.dumps('Current user already logged in.'), 200
        )
        response.headers['Content-Type'] = 'application/json'
    # store access token in session
    flask.session['credentials'] = credentials.access_token
    flask.session['gplus_id'] = gplus_id

    # get user info
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(user_info_url, params=params)
    data = json.loads(answer.text)

    flask.session['username'] = data['name']
    if 'email' in data.keys():
        flask.session['email'] = data['email']

    logged_cont = '<h1>Welcome, %s</h1>' % (data['name'])

    return logged_cont


@app.route('/catalog/logout')
def logout():
    # only disconnect if user is logged in
    creds = flask.session.get('credentials')
    if creds is None:
        response = flask.make_response(
            json.dumps('Current user not connected.'), 401
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    del flask.session['credentials']
    del flask.session['gplus_id']
    del flask.session['username']
    if 'email' in flask.session.keys():
        del flask.session['email']

    content = str(
        page_design.make_page_header('') +
        "<body><h3>You successfully logged out.</h3></body>"
    )
    return flask.render_template_string(content)


@app.route('/catalog/json')
def get_json():
    # returns to the user the json of the catalog content
    begin = time.time()
    js_data = dict()
    cats = get_categories()
    for cat in cats:
        item_dict = dict()
        item_stuff = get_items_by_cat_id(cat[0])
        for item in item_stuff:
            item_dict[item[0]] = {
                "item_name": item[1],
                "item_description": item[3]
            }
        js_data[cat[1]] = {
            "category_id": cat[0],
            "items": item_dict
        }
    stats.increment('home.page.hits', tags=['support', 'catalog:json'])
    stad.increment('page.views', tags=['support', 'catalog:json'])
    stats.gauge(
        'process.runtime', time.time() - begin,
        tags=['support', 'catalog:json']
    )
    stats.histogram('home.page.hits', 1, tags=['support', 'catalog:json'])
    stats.histogram(
        'user.query.seconds', time.time() - begin,
        tags=['support', 'catalog:json']
    )
    return json.dumps(js_data)


if __name__ == '__main__':
    app.secret_key = 'LRlMDsJMWUyDyxMbhadO_4Yv'
    app.run(host='0.0.0.0', port=8000, debug=True)
