from flask import Flask, request, render_template, redirect, url_for, session
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a real secret key

# Simple user credentials (not secure for production)
USER_CREDENTIALS = {
    "username": "admin",
    "password": "password"
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid Credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['datafile']
        if not file:
            return render_template('index.html', error="No file")

        df = pd.read_csv(file)

        # Generate visualization for the first 5 columns
        fig, axs = plt.subplots(5, 1, figsize=(10, 20))
        for i, column in enumerate(df.columns[:5]):
            sns.scatterplot(data=df, x=column, y=df[df.columns[-1]], ax=axs[i])
        plt.tight_layout()
        plot_path = 'static/plot.png'
        plt.savefig(plot_path)
        plt.close()

        return render_template('index.html', plot_url=plot_path)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
