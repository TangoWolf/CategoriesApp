from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask import flash, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Subject, Course, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open(
    'client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Categories Application"

engine = create_engine('sqlite:///categories.db?check_same_thread=false')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # First we check that the state parameter from login matches our request's.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Cotent-Type'] = 'application/json'
        return response

    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        reponse = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # We need to check that our request doesn't return an error.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']

    # And that our id_token and client_ids match our result's.
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    # Here we check to see if the user is already signed in.
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # We make a call for the user's information from google+
    userinfo_url = "https://www.googleapis.com/plus/v1/people/me"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store the information in our login_session.
    login_session['username'] = data['displayName']
    login_session['picture'] = data['image']['url']
    login_session['email'] = data['emails'][0]['value']
    login_session['id'] = data['id']
    if login_session['username'] == '':
        login_session['username'] = login_session['email']

    if getUserID(login_session['email']) is None:
        createUser(login_session)

    # And display a nice welcoming message.
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    output += ' -webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnet():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
            'Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        return redirect(url_for('showSubjects'))
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/subjects/JSON')
def subjectsJSON():
    subjects = session.query(Subject).all()
    return jsonify(subjects=[s.serialize for s in subjects])


@app.route('/subjects/<int:subject_id>/courses/JSON')
def subjectCoursesJSON(subject_id):
    subject = session.query(Subject).filter_by(id=subject_id).one()
    courses = session.query(Course).filter_by(subject_id=subject_id).all()
    return jsonify(Course=[c.serialize for c in courses])


@app.route('/subjects/<int:subject_id>/courses/<int:course_id>/JSON')
def coursesJSON(subject_id, course_id):
    course = session.query(Course).filter_by(id=course_id).one()
    return jsonify(course=course.serialize)


@app.route('/')
@app.route('/subjects/')
def showSubjects():
    subjects = session.query(Subject).order_by(asc(Subject.name))
    return render_template('subjects.html', subjects=subjects)


@app.route('/subjects/new/', methods=['GET', 'POST'])
def newSubject():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        user = getUserID(login_session['email'])
        newSubject = Subject(name=request.form['name'],
                             user_id=user)
        session.add(newSubject)
        flash('New Subject %s Successfully Created!' % newSubject.name)
        session.commit()
        return redirect(url_for('showSubjects'))
    else:
        return render_template('newSubject.html')


@app.route('/subjects/<int:subject_id>/edit/', methods=['GET', 'POST'])
def editSubject(subject_id):
    if 'username' not in login_session:
        return redirect('/login')

    editedSubject = session.query(Subject).filter_by(id=subject_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedSubject.name = request.form['name']
            flash('%s Successfully Edited!' % editedSubject.name)
            return redirect(url_for('showSubjects'))
    else:
        return render_template('editSubject.html', subject=editedSubject)


@app.route('/subjects/<int:subject_id>/delete/', methods=['GET', 'POST'])
def deleteSubject(subject_id):
    if 'username' not in login_session:
        return redirect('/login')

    subjectToDelete = session.query(Subject).filter_by(id=subject_id).one()

    if request.method == 'POST':
        session.delete(subjectToDelete)
        flash('%s Successfully Deleted' % subjectToDelete.name)
        session.commit()
        return redirect(url_for('showSubjects', subject_id=subject_id))
    else:
        return render_template('deleteSubject.html', subject=subjectToDelete)


@app.route('/subjects/<int:subject_id>/')
@app.route('/subjects/<int:subject_id>/courses')
def showCourses(subject_id):
    user = -1
    if 'username' in login_session:
        user = getUserID(login_session['email'])
    subject = session.query(Subject).filter_by(id=subject_id).one()
    courses = session.query(Course).filter_by(subject_id=subject_id).all()
    return render_template('courses.html', courses=courses, subject=subject,
                           user=user, check=subject.user_id)


@app.route('/subjects/<int:subject_id>/courses/new/', methods=['GET', 'POST'])
def newCourse(subject_id):
    if 'username' not in login_session:
        return redirect('/login')

    subject = session.query(Subject).filter_by(id=subject_id).one()

    if request.method == 'POST':
        user = getUserID(login_session['email'])
        newCourse = Course(name=request.form['name'],
                           summary=request.form['summary'],
                           subject_id=subject_id, user_id=user)
        session.add(newCourse)
        session.commit()
        flash('New Course %s Successfully Created!' % (newCourse.name))
        return redirect(url_for('showCourses', subject_id=subject_id))
    else:
        return render_template('newCourse.html', subject_id=subject_id)


@app.route('/subjects/<int:subject_id>/courses/<int:course_id>/edit/',
           methods=['GET', 'POST'])
def editCourse(subject_id, course_id):
    if 'username' not in login_session:
        return redirect('/login')

    editedCourse = session.query(Course).filter_by(id=course_id).one()
    subject = session.query(Subject).filter_by(id=subject_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedCourse.name = request.form['name']
        if request.form['summary']:
            editedCourse.summary = request.form['summary']
        session.add(editedCourse)
        session.commit()
        flash('Course successfully Edited!')
        return redirect(url_for('showCourses', subject_id=subject_id))
    else:
        return render_template('editCourse.html', subject_id=subject_id,
                               course_id=course_id, course=editedCourse)


@app.route('/subjects/<int:subject_id>/courses/<int:course_id>/delete/',
           methods=['GET', 'POST'])
def deleteCourse(subject_id, course_id):
    if 'username' not in login_session:
        return redirect('/login')

    subject = session.query(Subject).filter_by(id=subject_id).one()
    courseToDelete = session.query(Course).filter_by(id=course_id).one()

    if request.method == 'POST':
        session.delete(courseToDelete)
        session.commit()
        flash('Course Successfully Deleted')
        return redirect(url_for('showCourses', subject_id=subject_id))
    else:
        return render_template('deleteCourse.html', course=courseToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
