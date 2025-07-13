from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/demonMode', methods=['GET'])
def demon():
    return "Demon Mode on 😈"

# ✅ Challenge 1: Angel mode
@app.route('/angelMode', methods=['GET'])
def angel():
    return render_template('angel.html')

# ✅ Challenge 2: Frog mode with count
@app.route('/frog', methods=['GET'])
def frog():
    count = 10
    return render_template('frog.html', frogCount=count)

# ✅ Challenge 3: Elon mode with romanSalute level
@app.route('/elon', methods=['GET'])
def elon():
    really = 2  # Try 1, 2, or 3
    return render_template('elon.html', romanSalute=really)

# ✅ Challenge 4: Wishlist
@app.route('/wishlist', methods=['GET'])
def wishlist():
    wishlist = ['iPhone', 'Mac', 'MacBook', 'Tesla', 'Jetpack']
    return render_template('wishlist.html', hilingKo=wishlist)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
