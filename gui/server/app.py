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
    # a  = []
    # b = []
    # data = data.drop(['additional_keyword', 'comment'], axis=1)
    # for i in range(len(data)):
    #     a.append('')
    #     b.append('')
    # data['AdditionalKeyword'] = a
    # data['Comment'] = b
    # data.to_csv('../frontend/public/vispub.csv',index=False)
    #filter scivis and vis
    data = data.loc[data['Conference'].isin(['SciVis','Vis'])]
    # remove nan abstract 
    data = data.dropna(subset=['Abstract'])
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
    a = data['additional_keyword']
    c = data['comment']
    keyword = data['keyword']
    data = pd.read_csv('../frontend/public/vispub.csv')
    
    a_list = []
    c_list = []
    new_label = []

    for index, row in data.iterrows():
        if row['DOI']==doi:
            a_list.append(a)
            c_list.append(c)
            new_label.append(keyword)
        else:
            a_list.append(row['AdditionalKeyword'])
            c_list.append(row['Comment'])
            new_label.append(row['LabelKeyword'])
    new_df = pd.DataFrame({'AdditionalKeyword': a_list, 'Comment': c_list,'LabelKeyword': new_label})
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
            return jsonify({
                'aKeyword': row['AdditionalKeyword'],
                'comment': row['Comment'],
                'keyword':ast.literal_eval(row['LabelKeyword'])
            })

if __name__ == '__main__':
    app.run()