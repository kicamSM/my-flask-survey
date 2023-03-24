from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

# from random import randint, choice, samples

app = Flask(__name__)

app.config['SECRET_KEY'] = "iloverollerderby12"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

RESPONSES_ANSWERS = 'responses'
# responses = []

@app.route("/")
def home_page():
    """Displays home page/ title survey, the instructions and button to start survey"""
    instructions = satisfaction_survey.instructions
    title = satisfaction_survey.title
    
    return render_template('home.html', instructions=instructions, title=title)

@app.route('/verify_user', methods=["POST"])
def verify_user():
    session[RESPONSES_ANSWERS] = []
    return redirect('/question/0')

@app.route('/answer', methods=["POST"])
def sends_answers(): 
    """Logging answers to survey"""
    # session["answer"] = request.form["answer"]
    # answer = session["answer"]
    responses = session[RESPONSES_ANSWERS]
    
    answer = request.form['answer']
    responses.append(answer)
    session[RESPONSES_ANSWERS] = responses
    # responses.append(answer)
    i = len(responses)
    if i < len(satisfaction_survey.questions): 
        return redirect(f"/question/{i}")
    else: 
        return redirect('/thank_you')

@app.route('/question/<int:i>')
def displays_questions(i):
    """Displays the questions in survey"""
    responses = session.get(RESPONSES_ANSWERS)
    # i think we are obtaining the responses_answers here 
    
    if (responses is None):  
    # if len(responses) is None:  
        return redirect("/")
    
    # if len(responses) != i:
    if len(responses) != i:
        flash(f"Please answer question {len(responses) + 1} of the survey.", 'error')
        return redirect(f"/question/{len(responses)}")
    
    if i == len(satisfaction_survey.questions):
        return redirect('thank_you')

    if i < len(satisfaction_survey.questions):
        question = satisfaction_survey.questions[i].question
        return render_template('questions.html', question=question)


@app.route('/thank_you')
def thank_you():
    """Displays thank you page"""
    # responses *= 0
    return render_template('thank_you.html')

# not really sure about this but I am assuming we want to redirect to the next question

#    import pdb
#     pdb.set_trace()
    
    
    
    