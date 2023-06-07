import streamlit as st
import pandas as pd
import os
import pickle
import json
from util import transform_data
from matplotlib import pyplot as plt
import seaborn as sns

# Set title
st.title('Customer Churn Prediction App')
st.write('Predict if your customer is likely to churn!')

# Load schema
with open('schema.json', 'r') as f:
    schema = json.load(f)


# Setup column orders
column_in = list(schema['column_info'].keys())[:-1]
column_out = list(schema['transformed_columns']['transformed_columns'])


# SIDEBAR Section
st.sidebar.info('Update these values to predict churn based on your customer')
# Collect input features from users 
options = {}
for column, column_properties in schema['column_info'].items():
    if column == 'churn':
        pass
    # Create numerical sliders
    elif column_properties['dtype'] == 'int64' or column_properties['dtype'] == 'float64':
        min_val, max_val = column_properties['values']
        data_type = column_properties['dtype']

        feature_mean = (min_val+max_val) / 2
        if data_type == 'int64':
            feature_mean = int(feature_mean)
        
        options[column] = st.sidebar.slider(column, min_val, max_val, value=feature_mean)
    # Create categorical select boxes
    elif column_properties['dtype'] == 'object':
        options[column] = st.sidebar.selectbox(column, column_properties['values'])

# Load in model and encoder
with open('models/experiment_1/xg.pkl', 'rb') as f:
    model = pickle.load(f)

with open('models/experiment_1/encoder.pkl', 'rb') as f:
    onehot = pickle.load(f)

# Mean evening minutes value
mean_eve_mins = 200.29 # because we didnt use scikit-learn imputer, we need to keep track of it

# Make prediction
if st.button('Predict'):
    # convert options to df
    scoring_data = pd.Series(options).to_frame().T
    scoring_data = scoring_data[column_in]

    # check datatypes
    for column, column_properties in schema['column_info'].items():
        if column != 'churn':
            dtype = column_properties['dtype']
            scoring_data[column] = scoring_data[column].astype(dtype)

    # Apply data transformation
    scoring = transform_data(scoring_data, column_out, mean_eve_mins, onehot)

    # Render predictions
    predict = model.predict(scoring)
    st.write('Predicted Outcome')
    if predict == 1:
        st.write('This customer will churn')
    elif predict == 0:
        st.write('This customer will not churn')

# save historical customers churn data history
try:
    historical = pd.Series(options).to_frame().T
    historical['prediction'] = predict
    if os.path.isfile('historical_data.csv'):
        historical.to_csv('historical_data.csv', mode='a', header=False, index=False)
    else:
        historical.to_csv('historical_data.csv', header=True, index=False)
except Exception as e:
    pass

st.header('Historical Outcomes')
# only if there exist such csv file, we render dataframe
# to prevent errors in the web app
if os.path.isfile('historical_data.csv'): 
    hist = pd.read_csv('historical_data.csv')
    st.dataframe(hist)
    fig, ax = plt.subplots()
    sns.countplot(x='prediction', data=hist, ax=ax).set_title('Historical Predictions')
    st.pyplot(fig)
else:
    st.write('No historical data')
