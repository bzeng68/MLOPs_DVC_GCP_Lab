"""
Simple preprocessing script for Credit Card dataset.
Handles missing values and saves cleaned data.
"""

import pandas as pd
from pathlib import Path


def preprocess_data(input_path: str, output_path: str):
    """
    Preprocess credit card data by handling missing values.
    
    Args:
        input_path: Path to raw CSV file
        output_path: Path to save processed CSV
    """
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    print(f"Original shape: {df.shape}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    
    # Fill missing values with median for numerical columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64', 'float32', 'int32']).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            # If median is NaN (all values missing), use 0
            fill_value = median_val if pd.notna(median_val) else 0
            missing_count = df[col].isnull().sum()
            df[col] = df[col].fillna(fill_value)
            print(f"  Filled {missing_count} missing values in {col}")
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    
    print(f"Rows after removing duplicates: {initial_rows} → {len(df)}")
    
    # Final verification - ensure no NaN values remain
    remaining_nan = df.isnull().sum().sum()
    print(f"Missing values after cleaning: {remaining_nan}")
    
    if remaining_nan > 0:
        print("Warning: Some NaN values remain. Filling with 0...")
        df = df.fillna(0)
        print(f"Final missing values: {df.isnull().sum().sum()}")
    
    # Save processed data
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")


if __name__ == "__main__":
    preprocess_data(
        input_path="data/CC_GENERAL.csv",
        output_path="data/processed.csv"
    )
