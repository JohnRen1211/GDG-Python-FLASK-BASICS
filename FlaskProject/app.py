# Task created and done:
import requests
from flask import Flask, session, render_template, request, redirect, url_for
from cs50 import SQL
import bcrypt
import base64
import hashlib

# ✅ TODO 1: initialize SQLite
db = SQL("sqlite:///user.db")

app = Flask(__name__)

# ✅ TODO 2: generate a strong secret key
# You should generate your own, but here’s an example:
app.secret_key = 'f1b8a51aaf264d7d914a887ad46d923a'  # ← replace with your own secure key

@app.route('/')
def home():
    if 'user' in session:
        fake_store = requests.get("https://fakestoreapi.com/products?limit=20")
        return render_template('index.html', fake_store=fake_store.json())
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Missing email or password", 400 
        
        try:
            # ✅ TODO 3: Get user by email
            user = db.execute("SELECT * FROM users WHERE email = ?", email)
            
            if len(user) != 1:
                return 'Invalid email', 400

            if bcrypt.checkpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), user[0]['password']):
                session['user'] = {'email': user[0]['email'], 'username': user[0]['username']}
            else:
                return 'Invalid password', 400
            
            return redirect(url_for('home'))
        
        except:
            return 'Failed to login', 500
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        if not email or not password or not username:
            return "Missing email, username, or password", 400 
        
        try:
            # ✅ TODO 4: Check if user exists
            user = db.execute("SELECT * FROM users WHERE email = ?", email)
            
            if user:
                return 'Email already exists', 400
            
            # ✅ Hash password
            hash = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), bcrypt.gensalt())

            # ✅ TODO 5: Insert new user
            db.execute("INSERT INTO users (email, password, username) VALUES (?, ?, ?)", email, hash, username)

            session['user'] = {'email': email, 'username': username}

            return redirect(url_for('home'))

        except:
            return 'Failed to signup', 500
        
    return render_template('signup.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/change-username', methods=['POST'])
def update_username():
    if 'user' not in session:
        return redirect(url_for('login'))

    username = request.form.get('username')

    if not username:
        return 'Failed to change name', 400
    
    # ✅ TODO 6: Update username
    db.execute("UPDATE users SET username = ? WHERE email = ?", username, session['user']['email'])
    session['user']['username'] = username
    session.modified = True

    return redirect(url_for('settings'))

@app.route('/change-password', methods=['POST'])
def update_password():
    if 'user' not in session:
        return redirect(url_for('login'))

    password = request.form.get('password')

    if not password:
        return 'Failed to change password', 400
    
    hash = bcrypt.hashpw(base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()), bcrypt.gensalt())

    # ✅ TODO 7: Update password
    db.execute("UPDATE users SET password = ? WHERE email = ?", hash, session['user']['email'])

    return redirect(url_for('settings'))

@app.route('/delete-account', methods=['POST'])
def delete_account():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # ✅ TODO 8: Delete user
    db.execute("DELETE FROM users WHERE email = ?", session['user']['email'])
    session.pop('user', None)

    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login')) 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
