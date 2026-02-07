import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv('export_3d.csv')

x = df[['x', 'z', 'y']]
y = df['faction']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train.values, y_train)

# evaluate the model
y_pred = model.predict(x_test.values)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# save the model
joblib.dump(model, 'random_forest_model_3d.pkl')
print("Model saved as 'random_forest_model_3d.pkl'")