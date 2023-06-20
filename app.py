from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import openai
from textblob import TextBlob

# Initialize Flask
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'
app.config['SECRET_KEY'] = 'Your-Secret-Key'

# Initialize SQLAlchemy and LoginManager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Input API key here
openai.api_key = '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'

# Database model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        # Create user if not exists
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        email = request.form['email']

        responses = []
        sentiments = []

        for _ in range(3):
            try:
                response = openai.Completion.create(engine="text-davinci-003", prompt=email, max_tokens=10)
                responses.append(response.choices[0].text.strip())

                # Save the response to the database
                db_response = Response(user_id=current_user.id, content=response.choices[0].text.strip())
                db.session.add(db_response)
                db.session.commit()

                # Sentiment analysis
                blob = TextBlob(response.choices[0].text.strip())
                sentiments.append(blob.sentiment.polarity)

            except Exception as e:
                return f"An error occurred: {str(e)}"

        return render_template('index.html', email=email, responses=responses, sentiments=sentiments)

    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)
