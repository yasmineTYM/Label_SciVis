from flask import Flask, jsonify,request
from flask_cors import CORS
import pandas as pd 
import ast
import numpy as np
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/getGraphData', methods=['GET'])
def getGraphData():
    data = pd.read_csv('../frontend/public/vispub.csv')
    #filter scivis 
    data = data.loc[data['Conference'].isin(['SciVis'])]
    #remove nan
    data = data.replace(np.nan, '', regex=True)
    output_data = data.to_dict('records')
    return jsonify({
        'tableData':output_data
    })

@app.route('/addKeyword', methods=['POST'])
def addKeyword():
    data = request.get_json()
    doi = data['DOI']
    keyword = data['keyword']

    data = pd.read_csv('../frontend/public/vispub.csv')
    new_label = []
    for index, row in data.iterrows():
        if row['DOI']==doi:
            new_label.append(keyword)
        else:
            new_label.append(row['LabelKeyword'])
    new_df = pd.DataFrame({'LabelKeyword': new_label})
    data.update(new_df)
    data.to_csv('../frontend/public/vispub.csv',index=False)

    return jsonify('success')
@app.route('/getKeyword', methods=['POST'])
def getKeyword():
    paramter = request.get_json()
    data = pd.read_csv('../frontend/public/vispub.csv')
    data = data.replace(np.nan, '', regex=True)
    doi = paramter['DOI']
    for index, row in data.iterrows():
        if row['DOI']==doi:
            if row['LabelKeyword']=="":
                return jsonify({'keyword':[]})
            else:
                return jsonify({'keyword':ast.literal_eval(row['LabelKeyword'])})

if __name__ == '__main__':
    app.run()