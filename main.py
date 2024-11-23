from flask import Flask, render_template

app = Flask(__name__)

# Routes for each HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/copy')
def copy():
    return render_template('copy.html')

@app.route('/datapatient')
def datapatient():
    return render_template('datapatient.html')

@app.route('/dataset_test')
def dataset_test():
    return render_template('Dataset_test.html')

@app.route('/description')
def description():
    return render_template('description.html')

@app.route('/forgotpassword')
def forgot_password():
    return render_template('forgotpassword.html')

@app.route('/individual_test')
def individual_test():
    return render_template('Individual-Test.html')

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
