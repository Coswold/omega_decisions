import uuid
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask(__name__)

conn = sqlite3.connect('decision.db')

conn.execute('CREATE TABLE decisions (_id INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT, dec TEXT, del_key TEXT)')

conn.close()

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/enternew")
def new_decision():
	return render_template('decision.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route('/list')
def list():
	con = sqlite3.connect("decision.db")
	con.row_factory = sqlite3.Row

	cur = con.cursor()
	cur.execute("SELECT * FROM decisions")

	rows = cur.fetchall();
	return render_template("list.html", rows = rows)

@app.route('/delrec',methods = ['DELETE', 'GET'])
def delrec():
	print("\n\nMade it!\n\n")
	if request.method == 'DELETE':
		print("\n\nMade it!\n\n")
		try:
			d_key = request.form['del_key']
			with sqlite3.connect("decision.db") as con:
				cur = con.cursor()
				cur.execute("DELETE FROM decisions WHERE _id == ?;", (d_key))
				print("COOL")

				con.commit()
				msg = "Decision Completed"
		except:
			con.rollback()
			msg = "Error in completion"

		finally:
			return render_template("delete.html", msg = msg)
			con.close()

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():	
	if request.method == 'POST':
		try:
			dec = request.form['dec']
			email = request.form['email']
			d_key = str(uuid.uuid4())

			with sqlite3.connect("decision.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO decisions (owner,dec,del_key) VALUES (?,?,?)", (email,dec,d_key) )

				con.commit()
				msg = "Record Successfully Added"

		except:
			con.rollback()
			d_key = ""
			msg = "Error in insert operation"

		finally:
			return render_template("result.html",msg = msg, d_key = d_key)
			con.close()


if __name__ == "__main__":
	app.run()
