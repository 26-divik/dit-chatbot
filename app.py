from g4f.client import Client
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
client = Client()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

@app.route("/")
def home():
    return render_template('index.html')  # Render the login page initially

@app.route("/login", methods=['POST'])
def login():
    user_id = request.form['userId']
    if user_id.strip() != '':
        session['user_id'] = user_id  # Store user ID in session
        return redirect(url_for('chatbot'))
    else:
        return redirect(url_for('home'))

@app.route("/chatbot")
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('ChatBot.html')

@app.route("/chat", methods=['POST'])
def chat():
    user_input = request.json['message']
    try:
        response = client.chat.completions.create(
            model="blackbox",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_response = response.choices[0].message.content.strip()
    except AttributeError:
        bot_response = "Sorry, there was an error processing your request."
    except Exception as e:
        bot_response = f"An error occurred: {str(e)}"
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
   app.run()