import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import sys

def train_model(train_data_path, model_path):
    print("Training model...")
    df = pd.read_csv(train_data_path)
    X_train = df.drop('target', axis=1)
    y_train = df['target']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, model_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python model_training.py <train_data_path> <model_path>")
        sys.exit(1)
    train_model(sys.argv[1], sys.argv[2])
