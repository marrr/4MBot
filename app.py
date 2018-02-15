from flask import Flask, render_template, url_for
import process, db4m

app = Flask(__name__)



@app.route("/")
def main():
	total = process.get_count()
	return render_template('index.html', count=total)

if __name__ == "__main__":
    app.run(debug=True)