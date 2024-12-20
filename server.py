#In this file, we will use the flask web framework to handle the POST requests that we will get from the request.py and from HTML file

#import packages
import os
import numpy as np
import flask
from flask import Flask, request, jsonify,  render_template
import pickle

app = Flask(__name__)

model = pickle.load(open('models/regressor.pkl','rb'))

#to tell flask what url shoud trigger the function index()
@app.route('/')
@app.route('/index')
def index():

    return flask.render_template('index.html')


# get data from the html form and perform prediction
@app.route('/result',methods = ['POST'])
def result():
	print(request.form)
	if request.method == 'POST':
		data = request.form['year1']
		data2 = request.form['year2']
		input = float(data)
		input2 = float(data2)		

		# convert the data into numpy array and perform prediction
		array = np.array([[input], [input2]])
		prediction = model.predict(np.array([[input], [input2]]))
		output = prediction[0]
		ouput2 = prediction[1]

		# round output into two decimals
		output = round(output, 2)
		ouput2 = round(ouput2, 2)

		return render_template("result.html", prediction=[output,ouput2], years = [data,data2])


# get data from script file and perfrom prediction
@app.route('/api',methods=['POST'])
def predict():

	#get the data in json format
	data = request.get_json(force=True)

	#convert the data into numpy array and perform prediction
	prediction = model.predict([[np.array(data['exp'])]])
	output = prediction[0]

	#return result in json format
	return jsonify(output)


# set port into 5000 and debug is True
if __name__ == '__main__':
	app.run(port=5000, debug=True)
