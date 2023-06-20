from flask import Flask, request, render_template
import openai

# Initialize Flask
app = Flask(__name_)

# Input API key here
openai.api_key = '' 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        response1 = openai.Completion.create(engine="text-davinci-003", prompt=email, max_tokens=10)
        response2 = openai.Completion.create(engine="text-davinci-003", prompt=email, max_tokens=10)
        response3 = openai.Completion.create(engine="text-davinci-003", prompt=email, max_tokens=10)
        return render_template('index.html', email=email, response1=response1.choices[0].text.strip(), response2=response2.choices[0].text.strip(), response3=response3.choices[0].text.strip())
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
