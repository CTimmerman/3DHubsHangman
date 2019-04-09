"""The Engineering Challenge - 3D Hubs
Great! You’re reading this because you’re getting one step closer to joining the 3D Hubs
Engineering team. As mentioned we would love to check your programming skills and
therefore would like to present you the following challenge:
The challenge is to build a simple 'hangman' game that works as follows:
+ Chooses a random word out of 6 words: [3dhubs, marvin, print, filament, order, layer]
+ Display the spaces for the letters of the word (eg: '_ _ _ _ _' for 'order')
+ The user can choose a letter and if that letter exists in the chosen word it should be
shown on the puzzle (eg: asks for 'r' and now it shows '_ r _ _ r' for 'order')
+ The user can only ask 5 letters that don't exist in the word and then it's game over. If the
user wins, congratulate the user and save their high score (you are free to define what is
a “high score”)
Additional requirements:
- Provide a simple API for clients to play the game
- Provide an interface for users to play the game
The assignment shouldn't take longer than 4 hours: think of it as a minimum viable
product to test with users and try to focus on the overall architecture, maintainability, and
extendability.
Good luck!"""

import random
from database import Database
# python -m pip install flask
from flask import Flask, escape, request, session, g  # g = app global

man = [
r'''
____
|/
|
|
|_____
''',
r'''
____
|/  o
|
|
|_____
''',
r'''
____
|/  o
|   |
|
|_____
''',
r'''
____
|/  o
|  /|
|
|_____
''',
r'''
____
|/  o
|  /|\
|
|_____
''',
r'''
____
|/  o
|  /|\
|  /
|_____

''',
r'''
____
|/  o
|  /|\
|  / \
|_____
'''
]

def board(session):
	fails = session['fails']
	shown = session['shown']
	return man[len(fails) if len(fails) < len(man) else len(man)-1] + \
		''.join([escape(letter) for letter in fails]) + \
		'\n' + (' '.join(shown))

def init_game(session):
	word = random.choice(open('words.txt', 'r').read().splitlines())  # splitlines() because readlines() leaves the newlines on.
	session['shown'] = ['_'] * len(word)
	session['word'] = word
	session['fails'] = []
	session['name'] = 'Anon'
	session['template'] = open("index.html", 'r').read()
	session['try_again'] = open("try_again.html", 'r').read()
	session['guess'] = open("guess.html", 'r').read()
	session['done'] = False

app = Flask(__name__)
app.secret_key = b'34u89nqg45hg29q5n3hg5n9l459olqnm4q5oieorahadr'
#Done for every request!
@app.before_request
def before_request():
	g.db = Database('scores.sqlite')

@app.teardown_appcontext
def teardown_db(context):
	db = g.pop('db', None)
	if db is not None: db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'reset' in request.form or not 'word' in session:
		print("RESET")
		init_game(session)
	if 'name' in request.form:
		name = request.form['name']
		if name: session['name'] = request.form['name']
	
	content = 'Playing as %s' % escape(session['name'])
	letter = ''
	if 'letter' in request.form:
		letter = request.form['letter'].lower()
	if letter:
		content += guess(session, letter, g.db)
	else:
		content += board(session)

	content = session['template'].replace("CONTENT", content)
	content = content.replace("FORM", session['try_again'] if session['done'] else session['guess'])
	print(content)
	return content

def guess(session, letter, db):
	print("guess", session, letter)
	found = False
	word = session['word']
	shown = session['shown']
	for i, c in enumerate(shown):
		if word[i] == letter:
			shown[i] = letter
			found = True
	session['shown'] = shown
	message = ""
	if not found:
		session['fails'].append(letter)
		if len(session['fails']) > 5:
			session['done'] = True
			message = "Game over."
	elif not '_' in shown:
		session['done'] = True
		score = len(word)
		message = "\nCongratulations! Your score is %s." % score
		name = session['name']
		id = db.set_score(score, name)
		scores = db.get_scores()
		for score, name in scores:
			message += '\n%s %s' % (score, name)
	return board(session) + '\n' + message
	
if __name__ == "__main__":
	app.run()
