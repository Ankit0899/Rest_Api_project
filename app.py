from flask import Flask
from flask import Flask, render_template
import mysql.connector



app = Flask(__name__)
from controller import *


@app.route("/")
def Helloworld():
   return "Welcome"

@app.route("/home/")
def Home():
   return "this is home page"

if __name__ == '__main__':
   app.run(debug=True)