from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Dummy success message (you can later connect to DB)
        return render_template('signup.html', message="User registered successfully!")

    return render_template('signup.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)
