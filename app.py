#use flask to create a web server consisting of a login page and an endpoint providing a webpage

from flask import Flask, render_template, request, redirect, url_for, session

from fileReader import addOpinion, getHumanReadableResults, getOpinions, getSubjects, getValuesForOpinions, isAdministrator, isUserAuthorized

app = Flask(__name__)

app.secret_key='ultra_secret_key_used_for_session_but_i_dont_care_so_this_shitty_string_will_be_used'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    session['username'] = request.form['username']
    return redirect(url_for('poll', index=0))

@app.route('/poll/<int:index>')
def poll(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    if not isUserAuthorized():
        return "You are not authorized to view this page"
    if index is None:
        index = 0
    subject = getSubjects(index)
    return render_template('poll.html', subject=subject, opinions=getOpinions(subject), isAdmin=isAdministrator(), index=index, values=getValuesForOpinions(subject, session['username']), zip=zip)

@app.route('/poll/<int:index>', methods=['POST'])
def submit_poll(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    if not isUserAuthorized():
        return "You are not authorized to view this page"
    subject = getSubjects(index).strip()
    mapValueOpinion = {}
    for opinion in getOpinions(subject):
        if opinion in request.form:
            mapValueOpinion[opinion] = request.form[opinion]

    for opinion, value in mapValueOpinion.items():
        addOpinion(subject, opinion, value, session['username'])
    return redirect(url_for('poll', index=index+1))

@app.route('/poll/addOpinion/<int:index>', methods=['POST'])
def add_opinion(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    if not isUserAuthorized():
        return "You are not authorized to view this page"
    subject = getSubjects(index)
    opinion = request.form['new_opinion']
    addOpinion(subject, opinion, -1, session['username'])
    return redirect(url_for('poll', index=index))

@app.route('/results/<int:index>', methods=['GET'])
def results(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    if not isUserAuthorized() or not isAdministrator():
        return "You are not authorized to view this page"
    if index is None:
        index = 0
    subject = getSubjects(index)
    return render_template('results.html', subject=subject, results=getHumanReadableResults(subject), index=index)