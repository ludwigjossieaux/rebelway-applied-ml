import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.write("""
Hello, this is a simple Iris Flower Prediction App
""")

st.sidebar.header('User Input Data Features')
st.sidebar.markdown("""
[CSV Input File:]
""")

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    def user_input_features():
        SepalLengthCm = st.sidebar.slider('SepalLengthCm', 4.3, 8.0, 6.0)
        SepalWidthCm = st.sidebar.slider('SepalWidthCm', 2.0, 5.0, 3.0)
        PetalLengthCm = st.sidebar.slider('PetalLengthCm', 1.0, 7.0, 4.0)
        PetalWidthCm = st.sidebar.slider('PetalWidthCm', 0.1, 3.0, 2.0)
        data = {
            'SepalLengthCm': SepalLengthCm,
            'SepalWidthCm': SepalWidthCm,
            'PetalLengthCm': PetalLengthCm,
            'PetalWidthCm': PetalWidthCm
        }
        features = pd.DataFrame(data, index=[0])
        return features
    input_df = user_input_features()
    
iris_raw = pd.read_csv('iris.csv')
iris = iris_raw.drop(columns=['Id', 'Species'])
df = pd.concat([input_df, iris], axis=0)

df = df[:1] # Selects only the first row (the user input data)

st.subheader('User Input Features')
if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)
    
    
# model
load_clf = pickle.load(open('iris_clf.pkl', 'rb'))
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Prediction')
species = np.array(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
st.write(species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)
st.write("""
The app is developed by [Your Name].
""")