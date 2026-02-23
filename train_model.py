import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Example dataset
data = {
    'hours': [1,2,3,4,5,6,7,8],
    'score': [35,40,50,55,65,70,80,90]
}

df = pd.DataFrame(data)

X = df[['hours']]
y = df['score']

model = LinearRegression()
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained and saved successfully!")