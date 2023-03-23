from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

# from random import randint, choice, samples

app = Flask(__name__)

app.config['SECRET_KEY'] = "iloverollerderby12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def home_page():
    """Displays home page/ title survey, the instructions and button to start survey"""
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    
    return render_template('home.html', instructions=instructions, title=title)

@app.route('/question/<int:i>')
def displays_questions(i):
    """Displays the questions in survey"""
    if len(responses) is None:  
        return redirect("/")
    if len(responses) != i:
        flash("Please finish the survey.", 'error')
        return redirect(f"/question/{len(responses)}")
    if len(responses) is i + 1: 
        return redirect('/thank_you')
    if i >= len(satisfaction_survey.questions):
        flash("Please finish the survey.", 'error')
        return redirect(f"/question/{len(responses)}")
    if i < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[i].question
        return render_template('questions.html', question=question)

    
    # else: question = "Post not found."
    # return render_template('questions.html', question=question)

@app.route('/answer', methods=["POST"])
def sends_answers(): 
    """Logging answers to survey"""
    answer = request.form['answer']
    responses.append(answer)
    i = len(responses)
    if i < len(satisfaction_survey.questions): 
        return redirect(f"/question/{i}")
    else: 
        return redirect('/thank_you')

@app.route('/thank_you')
def thank_you():
    """Displays thank you page"""
    # responses *= 0
    return render_template('thank_you.html')

# not really sure about this but I am assuming we want to redirect to the next question

#    import pdb
#     pdb.set_trace()
    
    
    
    