from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('base.html')

# @app.route('/signup')
# def new_user():
#     return render_template('auth/register.html')

# ##TEMP##
# @app.route('/')
# def main():
#     return render_template('homepage.html', title = "Home")

# @app.route('/addrec',methods = ['POST', 'GET'])
# def addrec():
#    if request.method == 'POST':
#       try:
#          nm = request.form['nm']
#          psw = request.form['psw']
         
#          with sql.connect("database.db") as con:
#             cur = con.cursor()
#             cur.execute("INSERT INTO USERS (name,password) VALUES (?,?)",(nm,psw) )
            
#             con.commit()
#             msg = "Record successfully added"
#       except:
#          con.rollback()
#          msg = "error in insert operation"
      
#       finally:
#          return "<p>Hello, World!</p>"
#          con.close()

if __name__ == '__main__':
   app.run(debug = True)
