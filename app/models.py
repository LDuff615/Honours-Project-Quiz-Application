# This file will contain the models that will represent the database tables
from app.__init__ import db

# This model will be used to represent the USER table in the MySQL database
class user(db.Model):
    __tablename__ = 'user'

    userID = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # 28/03/2021 - create relationship between 'user' and 'user_test'
    testsTaken = db.relationship('user_test', backref='user', lazy='joined')

    # This function should return a printable representation of the user object
    def __repr__(self):
        return '<user: {}>'.format(self.name)

# This model will be used to represent the USER_TEST table in the MySQL database
class user_test(db.Model):
    __tablename__ = 'user_test'

    user_testID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False, primary_key=True)
    testID = db.Column(db.Integer, db.ForeignKey('test.testID'), nullable=False, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    # This function should return a printable representation of the user_test object
    def __repr__(self):
        return '<user_test: {}>'.format(self.user_testID)

# This model will be used to represent the TEST table in the MySQL database
class test(db.Model):
    __tablename__ = 'test'

    testID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    topicID = db.Column(db.Integer, db.ForeignKey('topic.topicID'), nullable=False)

    questions = db.relationship('test_question', backref='test', lazy='joined')

    # 28/03/2021 - create relationship between 'test' and 'user_test'
    testsAvailable = db.relationship('user_test', backref='test', lazy='joined')

    # This function should return a printable representation of the test object
    def __repr__(self):
        return '<test: {}>'.format(self.testID)

# This model will be used to represent the TEST_QUESTION table in the MySQL database
class test_question(db.Model):
    __tablename__ = 'test_question'

    testID = db.Column(db.Integer, db.ForeignKey('test.testID'), nullable=False, primary_key=True)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False, primary_key=True)

    # This function should return a printable representation of the test_question object
    def __repr__(self):
        return '<test_question: {}>'.format(self.testID)

# This model will be used to represent the QUESTION table in the MySQL database
class question(db.Model):
    __tablename__ = 'question'

    questionID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    description = db.Column(db.String(600), nullable=False)

    testQuestions = db.relationship('test_question', backref='question', lazy='joined')

    # 16/03/2021 - Create relationship between question and option classes, in order to load the multiple options related to a single question
    # A relationship will allow for both questions and options to be pulled from the database together in a single query statement
    options = db.relationship('option', backref='question', lazy='joined')

    # 24/03/2021 - Create a relationship between question and answer classes, in order to load the option the user selected to answer the current question
    answer = db.relationship('answer', backref='question', lazy='joined')

    # This function should be return a printable representation of the question object
    def __repr__(self):
        return '<question: {}>'.format(self.description)

# This model will be used to represent the OPTION table in the MySQL database
class option(db.Model):
    __tablename__ = 'option'

    optionID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    correct = db.Column(db.SmallInteger, nullable=False)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False)

    # This function should return a printable representation of the option object
    def __repr__(self):
        return '<option: {}>'.format(self.description)

# This model will be used to represent the ANSWER table in the MySQL database
class answer(db.Model):
    __tablename__ = 'answer'

    answerID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_testID = db.Column(db.Integer, db.ForeignKey('user_test.user_testID'), nullable=False)
    questionID = db.Column(db.Integer, db.ForeignKey('question.questionID'), nullable=False)
    optionID = db.Column(db.Integer, db.ForeignKey('option.optionID'), nullable=False)

    # This function should return a printable representation of the answer object
    def __repr__(self):
        return '<answer: {}>'.format(self.answerID)

# This model will be used to represent the TOPIC table in the MySQL database
class topic(db.Model):
    __tablename__ = 'topic'

    topicID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    domainID = db.Column(db.Integer, db.ForeignKey('domain.domainID'), nullable=False)

    # This function should return a printable representation of the topic object
    def __repr__(self):
        return '<topic: {}>'.format(self.name)

# This model will be used to represent the DOMAIN table in the MySQL database
class domain(db.Model):
    __tablename__ = 'domain'

    domainID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

    # This function should return a printable representation of the domain object
    def __repr__(self):
        return '<domain: {}>'.format(self.name)