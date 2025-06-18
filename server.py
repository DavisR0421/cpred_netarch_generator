from flask import Flask, render_template, url_for, request, redirect
from netarchgenerator import create_net
from forms_radiobuttons import NET_Difficulty_Form
# waitress is a production WSGI server for Python web applications
# use serve() instead of app.run() to remove the warning about the app being for development use only
from waitress import serve

app = Flask(__name__)

@app.route('/')
def myredirect():
    return redirect(url_for('index'))

@app.route('/index',methods=['GET','POST'])
def index():
    form = NET_Difficulty_Form()
    if form.validate_on_submit():
        # Get the difficulty rating from the form
        v_difficulty_rating = form.difficulty.data
        # Call the create_net function with the difficulty rating
        message = create_net(v_difficulty_rating)
        return render_template('index.html', form=form, message=message)
    return "Sup, Choom!"

if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=8000)
    serve(app, host="0.0.0.0",port=8000)