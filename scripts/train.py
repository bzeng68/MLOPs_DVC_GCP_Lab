"""
Simple training script for clustering credit card customers.
Uses K-means clustering on preprocessed data.
"""

import pandas as pd
import pickle
import json
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def train_model(input_path: str, model_path: str, metrics_path: str, n_clusters: int = 4):
    """
    Train K-means clustering model on credit card data.
    
    Args:
        input_path: Path to processed CSV file
        model_path: Path to save trained model
        metrics_path: Path to save metrics JSON
        n_clusters: Number of clusters for K-means
    """
    print(f"Loading processed data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Drop customer ID column if exists
    if 'CUST_ID' in df.columns:
        df = df.drop('CUST_ID', axis=1)
    
    print(f"Training data shape: {df.shape}")
    
    # Check for NaN values before training
    if df.isnull().sum().sum() > 0:
        print("ERROR: Data contains NaN values!")
        print(f"Columns with NaN:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
        raise ValueError("Preprocessing failed: NaN values detected. Re-run preprocessing.")
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)
    
    # Train K-means model
    print(f"Training K-means with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    # Calculate metrics
    inertia = float(kmeans.inertia_)
    n_samples = len(df)
    
    print(f"Training complete!")
    print(f"Inertia: {inertia:.2f}")
    print(f"Samples: {n_samples}")
    
    # Save model
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump({'kmeans': kmeans, 'scaler': scaler}, f)
    print(f"Model saved to {model_path}")
    
    # Save metrics
    metrics = {
        "n_clusters": n_clusters,
        "inertia": inertia,
        "n_samples": n_samples,
        "n_features": df.shape[1]
    }
    
    Path(metrics_path).parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {metrics_path}")


if __name__ == "__main__":
    train_model(
        input_path="data/processed.csv",
        model_path="models/model.pkl",
        metrics_path="metrics.json",
        n_clusters=4
    )
