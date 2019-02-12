from flask import Flask, request
from flask_cors import CORS
import WebServiceIntegrator as wsi
import sys
from flask import jsonify
app = Flask(__name__)
CORS(app)

@app.route('/')
def world():
	print("hello",file=sys.stderr)
	return "World"

@app.route('/validate',methods=['POST'])
def get_data():
	app.logger.info(request.form['query'])
	app.logger.info(wsi.context_query(request.form['query']))
	return jsonify(wsi.context_query(request.form['query']))

if __name__ == '__main__':
   app.run(debug=True)