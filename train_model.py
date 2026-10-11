import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import os

def create_features(df):
    """
    Feature Engineering:
    1. Cyclical month encoding using sine and cosine (Dec and Jan are treated as neighbours).
    2. Lag 1: Previous month consumption.
    3. Lag 12: Same month consumption from the previous year.
    """
    df = df.copy()
    
    # Cyclical encoding for Month (1 to 12)
    df['month_sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    
    # Lag features
    df['lag_1'] = df['Units_Consumed'].shift(1)
    df['lag_12'] = df['Units_Consumed'].shift(12)
    
    # Drop rows that do not have 12 months history
    df_clean = df.dropna().reset_index(drop=True)
    return df_clean

def train_and_evaluate(csv_path="data/electricity_data.csv", model_output_path="model.pkl"):
    print("--- BijliSmart Model Training ---")
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset file not found at {csv_path}")
        return None
    
    df = pd.read_csv(csv_path)
    print(f"Total raw records loaded: {len(df)}")
    
    df_features = create_features(df)
    print(f"Records after creating lag features: {len(df_features)}")
    
    feature_cols = ['month_sin', 'month_cos', 'lag_1', 'lag_12']
    X = df_features[feature_cols]
    y = df_features['Units_Consumed']
    
    # Chronological Split: Train on first 75%, test on last 25% (no random shuffle)
    split_index = int(len(df_features) * 0.75)
    
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]
    
    print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")
    
    # Linear Regression Model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Simple Baseline: using same month from last year (lag_12)
    baseline_pred = X_test['lag_12']
    baseline_mae = mean_absolute_error(y_test, baseline_pred)
    
    print("\n--- Model Evaluation Results ---")
    print(f"Linear Regression MAE: {mae:.2f} units")
    print(f"Baseline (Same month last year) MAE: {baseline_mae:.2f} units")
    print(f"R-squared (R2) Score: {r2:.4f}")
    
    # Save trained model and feature list
    artifacts = {
        'model': model,
        'features': feature_cols
    }
    with open(model_output_path, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"\nModel saved successfully to '{model_output_path}'")
    
    return model

if __name__ == "__main__":
    train_and_evaluate()
