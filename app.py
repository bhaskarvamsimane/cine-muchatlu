from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Here you can add code to save user to DB
        message = "User registered successfully!"
        
    return render_template('signup.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
