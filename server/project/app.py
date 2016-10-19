from flask import Flask, render_template, request
from forms import SignupForm

app = Flask(__name__)

app.secret_key = "dev-key"	#CSRF

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():    
    form = SignupForm()
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            return "Dummy Signup"
    elif request.method == 'GET':
        return render_template('signup.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/listofprojects')
def listofprojects():
    return render_template('listofprojects.html')


if __name__ == '__main__':
    app.run(debug=True)
