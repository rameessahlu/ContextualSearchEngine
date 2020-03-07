import web_service_integrator as wsi
from flask import Flask, request, render_template
from flask_cors import CORS
import sys, os
from flask import jsonify


app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def index():
    template_path = os.path.join(os.getcwd(), os.path.join('static_files', 'index.html'))
    return render_template('index.html')

@app.route('/validate',methods=['POST'])
def get_data():
    app.logger.info(request.form['query'])
    app.logger.info(wsi.context_query(request.form['query']))
    return jsonify(wsi.context_query(request.form['query']))

if __name__ == '__main__':
   app.run(debug=True)