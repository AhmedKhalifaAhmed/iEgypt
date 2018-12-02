"""
Routes and views for the flask application.
"""
from flask import (
    Blueprint, session, redirect, url_for, request, flash
)
from iEgypt.model.overloaded import load_template
from iEgypt.model.db.user_model import(
    user_search_oc, user_search_contributor, user_show_contributors,
    user_show_oc, user_get_profile
)
from iEgypt.blueprints.auth import login_required


#Create the blueprint
bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/')
def index():
    """Renders the home page."""
    return load_template('user/home.html', title='Home')


@bp.route('/home')
def home():
    """Renders the home page."""
    if session.get('user_id'):
        home_url = '{user_type}.index'.format(user_type=session.get('user_type'))
        return redirect(url_for(home_url))
    return load_template('user/home.html', title='Home')


@bp.route('/oc-search', methods=('GET', 'POST'))
def oc_search():
    """Renders the page to search for original content"""
    col_names = ['Content ID', 'Contributor ID', 'Category', 'Subcategory',
        'Type', 'Link', 'Rating']
    table = dict()
    if request.method == 'POST':
        type = 'NULL'
        cat = 'NULL'
        if request.form['type'] != '':
            type = request.form['type']
        if request.form['category'] != '':
            cat = request.form['category']
        table = user_search_oc(type, cat)
    return load_template('user/oc-search.html', title='Search Original Content',
        table=table, col_names=col_names)


@bp.route('/contributor-search', methods=('GET', 'POST'))
def contributor_search():
    """Renders the page to search for contributors"""
    col_names = ['ID', 'Full name', 'age', 'Years of experience',
        'Portfolio link', 'Specialization']
    table = dict()
    if request.method == 'POST':
        name = request.form['name']
        table = user_search_contributor(name)

    return load_template('user/contributor-search.html',
        title='Search Contributor', table=table, col_names=col_names)


@bp.route('/show-contributors')
def show_contributors():
    """Renders the page to show contributors in order of
    highest years of experience"""
    col_names = ['ID', 'Full name', 'Years of experience',
        'Specialization', 'Portfolio_link']
    table = user_show_contributors()
    return load_template('user/show-contributors.html',
        title='Show Contributors', table=table, col_names=col_names)


@bp.route('/show-oc', methods=('GET', 'POST'))
def show_oc():
    """Renders a page to show original content"""
    col_names = ['Contributor ID', 'Contributor fullname', 'E-mail', 'Birthday',
        'Age', 'Years of experience', 'Portfolio link', 'Specialization',
        'Content ID', 'Category', 'Subcategory', 'Year', 'Rating']
    table = dict()
    if request.method == 'POST':
        if request.form['id'] == '':
            table = user_show_oc()
        else:
            error = None
            try:
                int(request.form['id'])
            except ValueError:
                error = 'Invalid ID'
            if not error:
                table = user_show_oc(request.form['id'])
            else:
                flash('Invalid input.')
    return load_template('user/show-oc.html', title='Show Original Content',
        table=table, col_names=col_names)


@bp.route('/show-profile')
@login_required
def show_profile():
    """Renders a page to show a user's profile"""
    user_id = session.get('user_id')
    row = user_get_profile(user_id)
    user_type = session.get('user_type')
    col_names = ['Email', 'Password', 'First name', 'Middle name', 'Last name',
        'Birthday', 'Working place name', 'Working place type',
        'Working place description', 'Specialization', 'Portfolio link',
        'Years of experience', 'Hire date', 'Working hours', 'Payment rate']
    labels = dict()
    for i in range(len(row)):
        labels[col_names[i]] = row[i]
    viewer_labels = ('Working place name', 'Working place type', \
    'Working place type')
    contributor_labels = ('Specialization', 'Portfolio link', \
    'Years of experience')
    staff_labels = ('Hire date', 'Working hours', 'Payment rate')
    if user_type == 'viewer':
        for label in staff_labels+contributor_labels:
            labels.pop(label, None)
    elif user_type == 'Contributor':
        for label in viewer_labels+staff_labels:
            labels.pop(label, None)
    else:
        for label in viewer_labels+contributor_labels:
            labels.pop(label, None)
    return load_template('user/show-profile.html', labels=labels)


@bp.route('/edit-profile')
@login_required
def edit_profile():
    """Renders a page to edit a user's profile"""
    
