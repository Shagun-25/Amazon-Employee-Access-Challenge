import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter
from scipy import sparse

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

def concat_features_duplet(df_train, cols):
    dup_features = []
    for indicies in combinations(range(len(cols)), 2):
        dup_features.append([hash(tuple(v)) for v in df_train[:,list(indicies)]])
    return np.array(dup_features).T

def concat_features_triplet(df_train, cols):
    tri_features = []
    for indicies in combinations(range(len(cols)), 3):
        tri_features.append([hash(tuple(v)) for v in df_train[:,list(indicies)]])
    return np.array(tri_features).T

def category_freq(X):
    X_new = X.copy()
    for f in X_new.columns:
        col_count = dict(Counter(X_new[f].values))

        for r in X_new.itertuples():
            X_new.at[r[0], f'{f}_freq'] = col_count[X_new.loc[r[0], f]]
    return X_new

#Loading models from disk
with open('one_hot.pickle', 'rb') as f:
 one_enc = pickle.load(f)

with open('lab_dup.pickle', 'rb') as g:
 lab_dup_enc = pickle.load(g)

with open('lab_tri.pickle', 'rb') as h:
 lab_tri_enc = pickle.load(h)

with open('scaler.pickle', 'rb') as i:
 scaler = pickle.load(i)

filename = 'logreg1_updated.sav'
loaded_model = pickle.load(open(filename, 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    int_features = np.array([int(x) for x in request.form.values()])
    X = pd.DataFrame([int_features[:-1]], columns = ['RESOURCE', 'MGR_ID', 'ROLE_ROLLUP_1', 'ROLE_ROLLUP_2', 'ROLE_DEPTNAME',
                                                'ROLE_TITLE', 'ROLE_FAMILY_DESC', 'ROLE_FAMILY'])
                                                
    X_dup_test = concat_features_duplet(np.array(X), ['RESOURCE', 'MGR_ID', 'ROLE_ROLLUP_1', 'ROLE_ROLLUP_2', 'ROLE_DEPTNAME',
                                                        'ROLE_TITLE', 'ROLE_FAMILY_DESC', 'ROLE_FAMILY'])
                                                        
    X_tri_test = concat_features_triplet(np.array(X), ['RESOURCE', 'MGR_ID', 'ROLE_ROLLUP_1', 'ROLE_ROLLUP_2', 'ROLE_DEPTNAME',
                                                        'ROLE_TITLE', 'ROLE_FAMILY_DESC', 'ROLE_FAMILY'])
    
    X_dup_test= lab_dup_enc.transform(X_dup_test)
    X_tri_test= lab_tri_enc.transform(X_tri_test)
    X_freq_test = np.array(category_freq(X).iloc[:,8:])
    X_all_categorical = np.hstack((X, X_dup_test, X_tri_test))
       
    X_freq = scaler.transform(X_freq_test)
    X_all_categorical_selected= X_all_categorical[:, [64, 42, 69, 11, 85, 0, 65, 67, 29, 9, 66, 47, 60, 10, 12, 71, 8, 53, 79, 19, 36, 63, 37, 43, 41]]
    X_freq_selected = X_freq[:, [1, 5, 7]]
    X_selected = sparse.hstack((one_enc.transform(X_all_categorical_selected), X_freq_selected))

    preds = loaded_model.predict_proba(X_selected)[:, 1]
    access_or_not = loaded_model.predict(X_selected)
    if access_or_not[0] == 1:
        return render_template('index.html', prediction_text='Access Granted!')
    else:
        return render_template('index.html', prediction_text='Access Revoked!')

if __name__ == "__main__":
    app.run(debug=True)