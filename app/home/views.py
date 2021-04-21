# This file will provide the view functions to connect to each HTML page
# Importing modules from flask and SQLAlchemy packages
from flask import render_template, redirect, url_for, request, session, flash

# Importing hpApp blueprint from __init__.py
from sqlalchemy.exc import InvalidRequestError

from .__init__ import hpApp

# Importing every db model from app/models.py
from ..models import *

# Importing random module in order to be able to generate a random number
import random

# 16/03/2021 - making score a global variable
score = 0

# 16/03/2021 - importing custom-made form from app/forms.py
from ..forms import MultipleChoiceForm
from ..forms import initializeSessionForm

# 28/03/2021 - importing date from datetime
from datetime import date

from sqlalchemy import and_

# hpApp.route is a decorator which passes along a URL route as a parameter
@hpApp.route('/')
@hpApp.route('/menu')
# startmenu() view function will render the menu.html template
def startmenu():
    return render_template('menu.html')

# 29/03/2021 - setSession() view function will be used to prompt users into entering their email addresses
@hpApp.route('/setSession', methods=['GET', 'POST'])
def setSession():
    # instantiate form
    form = initializeSessionForm()

    # If the request method is POST, and the form is validated...
    if request.method == 'POST' and form.validate():
        # Grab all of the user records in the User table
        users = db.session.query(user).all()

        # If there are any user records...
        if users is not None:
            # Query database to retrieve the user record whose 'name' field matches the form email data
            sessionID = db.session.query(user).filter_by(name=form.email.data).first()

            # If 'sessionID' contains the only record whose name field matches that of the email form data...
            if sessionID is not None:
                session['username'] = form.email.data
                session['userID'] = sessionID.userID
                return redirect(url_for('hpApp.universe'))
            # Otherwise, if we don't recognize the email address...
            else:
                # We increment the session ID/ Create new session
                lastUser = db.session.query(user).order_by(user.userID.desc()).first()
                session['userID'] = lastUser.userID+1
                newSession = user(userID=session.get('userID'), name=form.email.data)
                db.session.add(newSession)
                db.session.commit()
                return redirect(url_for('hpApp.universe'))
        # Otherwise, if there aren't any user records
        else:
            # Initialize the session
            session['userID'] = 1
            newSession = user(userID=session.get('userID'), name=form.email.data)
            db.session.add(newSession)
            db.session.commit()
            return redirect(url_for('hpApp.universe'))
    return render_template('establish_session.html', form=form)

@hpApp.route('/universe', methods=['GET'])
# universe() view function will query the database for every domain record & render the universe_select.html template
def universe():
    result = db.session.query(domain).all()
    return render_template('universe_select.html', result=result) # template is rendered with query result set passed as parameter

@hpApp.route('/character/<chosenUni>')
# character() view function will query the database for every topic record related to the chosen domain & render the char_select.html template, with the query result set passed along as a parameter
def character(chosenUni):
    Chars = db.session.query(topic).filter(topic.domainID == chosenUni)
    return render_template('char_select.html', cResults=Chars) # Pass along the chars variable in order to specify which character icons will be displayed

# 16/03/2021 - the WTF Form will be placed in this function
@hpApp.route('/quiz/<chosenChar>', methods=['GET', 'POST'])
# quiz() view function will query the database for all of the questions and
# options related to the number of the selected test for the selected topic
# The view function will then instantiate the WTForm & render the quiz.html template.
# Once the form has been submitted, the form will be validated,
# and the template will be rendered again, this time with the next question.
# This cycle will repeat until the last question has been answered.
# After that, the quiz_result.html template will be rendered.
def quiz(chosenChar):
    #TODO: Select random quiz for this character

    testIdArray = []
    criteriaNotMet = True

    charRelatedIDs = []
    takenIDs = []
    availableQuizzes = []
    takenAllQuizzes = []
    takenTopics = []
    counter = 0

    # 31/03/2021 - restart
    # Query db to retrieve all test records whose topicID field matches the chosenChar value
    charRelatedQuizzes = db.session.query(test).filter_by(topicID=chosenChar).all()

    # 02/04/2021:
    # For each test record in charRelatedQuizzes...
    for q in charRelatedQuizzes:
        # Place the current element's test IDs into a list
        charRelatedIDs.append(q.testID)

    # Find out if the user has taken a test before
    # Grab the list of user_test records where the userID value matches the current user + where the testID exists within the charRelatedIDs list
    # This will return a list of records which show which character-specific tests the current user has taken
    testsTaken = db.session.query(user_test).filter_by(userID=session['userID']).filter(user_test.testID.in_(charRelatedIDs)).all() # 02/04/2021:

    # If the user has taken a test before
    if testsTaken:
        # 02/04/2021:
        # For each user_test record in testsTaken...
        for completedTest in testsTaken:
            # Place the current element's test ID into a list
            takenIDs.append(completedTest.testID)

        # 02/04/2021:
        # For each test record, whose testID does not appear within the takenIDs list...
        for incompletedTest in charRelatedQuizzes:
            # If test ID does not appear in takenIDs list...
            if incompletedTest.testID not in takenIDs:
                # Add test record to availableQuizzes list
                availableQuizzes.append(incompletedTest)
            # Otherwise, test ID does appear in takenIDs list
            else:
                takenTopics.append(incompletedTest.topicID)


        # 02/04/2021:
        if availableQuizzes:
            # Select a record at random
            chosenQuiz = random.choice(availableQuizzes)

            # Create new user_test record
            today = date.today()
            userId = session['userID']
            chosenQuizId = chosenQuiz.testID
            takingTest = user_test(date=today, userID=userId, testID=chosenQuizId, score=0)
            db.session.add(takingTest)
            db.session.commit()
            return redirect(url_for('hpApp.quiz_display', quiz_id=chosenQuizId))

        if takenTopics:
            # create flash message to display on-screen
            flash('Congratulations! You have completed every test for this character')
            selectedDomain = db.session.query(domain).join(topic).filter(topic.topicID.in_(takenTopics)).first()
            selectedDomainId = selectedDomain.domainID
            return redirect(url_for('hpApp.character', chosenUni=selectedDomainId))

    # Otherwise, user hasn't taken test before
    else:
        # 02/04/2021:
        # Iterate across each character-specific quiz
        for incompletedTest in charRelatedQuizzes:
            # Add each quiz record to the list of available quizzes
            availableQuizzes.append(incompletedTest)
        # Choose a quiz at random
        chosenQuiz = random.choice(availableQuizzes)

        # Create new user_test record
        today = date.today()
        userId = session['userID']
        chosenQuizId = chosenQuiz.testID
        takingTest = user_test(date=today, userID=userId, testID=chosenQuizId, score=0)
        db.session.add(takingTest)
        db.session.commit()
        return redirect(url_for('hpApp.quiz_display', quiz_id=chosenQuizId))

@hpApp.route('/quiz_display/<quiz_id>', methods=['GET', 'POST'])
def quiz_display(quiz_id):
    tst = db.session.query(test).get(quiz_id)

    # 05/04/2021 - querying db to retrieve the user_test record where userID matches session ID & testID matches that of the recently retrieved test
    currentUserTest = db.session.query(user_test).filter_by(userID=session['userID']).filter(user_test.testID==tst.testID).first()
    currentUserTestID = currentUserTest.user_testID

    #11/04/2021 - new list
    setOfQuestions = []

    form = MultipleChoiceForm()
    if request.method == 'POST':
        indx = int(request.form.get("hidden"))
    else:
        indx = 0

    form.answer.choices = [(option.optionID, option.description) for option in tst.questions[indx].question.options]
    if form.validate_on_submit():
        # This is the question we're answering
        # This is now a test_question object, and we can use any relationships it has to get the related information
        q = tst.questions[indx]

        # if right answer, store in database
        # 28/03/2021 - grabbing the required data, and inserting it into a new 'answer' record
        questionAnswered = answer(
            # 05/04/2021 - fixing to include user_testID
            user_testID=currentUserTestID,
            questionID=q.question.questionID,
            optionID=form.answer.data
        )
        db.session.add(questionAnswered)
        db.session.commit()

        try:
            lengthOfList = db.session.query(test_question).filter(test_question.testID == quiz_id).count()
        except InvalidRequestError:
            db.session.rollback()

        listIndex = lengthOfList-1
        if indx == listIndex:
            # 13/04/2021 - small test
            testRelatedQs = db.session.query(question).all()

            return redirect(url_for('hpApp.quiz_results', testResults=testRelatedQs))
        # Otherwise, render next question
        # 11/04/2021 - add else statement so that if the current question isn't the last question...
        # Increment index & prepare options
        else:
            indx = int(form.hidden.data) +1
            form.answer.choices = [(option.optionID, option.description) for option in tst.questions[indx].question.options]

    form.hidden.data = str(indx)
    return render_template('quiz.html', form=form, question=tst.questions[indx].question, quiz_id=quiz_id)

@hpApp.route('/quiz_results/<testResults>')
def quiz_results(testResults):
    return render_template('quiz_results.html', quizResults=testResults)
