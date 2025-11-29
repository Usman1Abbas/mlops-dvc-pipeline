import kfp
from kfp import components
from kfp.components import InputPath, OutputPath

def load_data(data_path: OutputPath(str)):
    import pandas as pd
    from sklearn.datasets import fetch_california_housing
    
    print("Loading data...")
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    
    df.to_csv(data_path, index=False)

def preprocess_data(input_data_path: InputPath(str), 
                    train_data_path: OutputPath(str), 
                    test_data_path: OutputPath(str)):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    
    print("Preprocessing data...")
    df = pd.read_csv(input_data_path)
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_df['target'] = y_train.values
    
    test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_df['target'] = y_test.values
    
    train_df.to_csv(train_data_path, index=False)
    test_df.to_csv(test_data_path, index=False)

def train_model(train_data_path: InputPath(str), 
                model_path: OutputPath(str)):
    import pandas as pd
    from sklearn.ensemble import RandomForestRegressor
    import joblib
    
    print("Training model...")
    df = pd.read_csv(train_data_path)
    X_train = df.drop('target', axis=1)
    y_train = df['target']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, model_path)

def evaluate_model(test_data_path: InputPath(str), 
                   model_path: InputPath(str), 
                   metrics_path: OutputPath(str)):
    import pandas as pd
    import joblib
    from sklearn.metrics import mean_squared_error, r2_score
    import json
    
    print("Evaluating model...")
    df = pd.read_csv(test_data_path)
    X_test = df.drop('target', axis=1)
    y_test = df['target']
    
    model = joblib.load(model_path)
    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    metrics = {
        'mse': mse,
        'r2': r2
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f)
        
    print(f"Metrics: {metrics}")

if __name__ == '__main__':
    components.create_component_from_func(
        load_data,
        output_component_file='components/load_data.yaml',
        base_image='python:3.9',
        packages_to_install=['pandas', 'scikit-learn']
    )
    
    components.create_component_from_func(
        preprocess_data,
        output_component_file='components/preprocess_data.yaml',
        base_image='python:3.9',
        packages_to_install=['pandas', 'scikit-learn']
    )
    
    components.create_component_from_func(
        train_model,
        output_component_file='components/train_model.yaml',
        base_image='python:3.9',
        packages_to_install=['pandas', 'scikit-learn', 'joblib']
    )
    
    components.create_component_from_func(
        evaluate_model,
        output_component_file='components/evaluate_model.yaml',
        base_image='python:3.9',
        packages_to_install=['pandas', 'scikit-learn', 'joblib']
    )
