from flask import Flask,render_template,url_for,request, redirect
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import logging

from chunker import *


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
	# backend code
	if request.method == 'POST':
		message = request.form['message']			# text from textarea
		checkbtn = request.form.getlist('check')	# out: ['N4', 'N3']

		print(message, checkbtn)
		tree = rule_ident(message)
		marked = traverse_tree(tree, [])
		rules, text = to_html(marked, checkbtn)

		return render_template('result.html', htmlRules=rules, htmlText=text)
	else:
		return render_template('result.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=2000, debug=False)