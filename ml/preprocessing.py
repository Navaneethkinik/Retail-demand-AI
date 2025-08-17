import pandas as pd

STANDARD_COLS = {
    'Product ID': 'sku',
    'Units Sold': 'sales',
    'Inventory Level': 'inventory',
    'Units Ordered': 'orders',
    'Price': 'price',
    'Discount': 'discount',
    'Holiday/Promotion': 'promo',
    'Seasonality': 'season',
    'Weather Condition': 'weather'
}

REQUIRED_COLS = ['date', 'Product ID', 'Units Sold']

def preprocess_csv(file_path: str) -> pd.DataFrame:
    """
    Preprocess uploaded CSV for a company.
    """
    df = pd.read_csv(file_path)

    # Check required columns
    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Rename columns
    df = df.rename(columns=STANDARD_COLS)

    # Convert types
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    numeric_cols = ['sales', 'inventory', 'orders', 'price', 'discount', 'promo']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0

    categorical_cols = ['season', 'weather']
    for col in categorical_cols:
        if col not in df.columns:
            df[col] = 'Unknown'

    # Sort
    df = df.sort_values(['sku', 'date']).reset_index(drop=True)

    # Feature engineering
    df = add_features(df)

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add lag features, rolling averages, and encode categorical variables
    """
    # Lag features
    df['sales_lag_1'] = df.groupby('sku')['sales'].shift(1).fillna(0)
    df['sales_lag_7'] = df.groupby('sku')['sales'].shift(7).fillna(0)

    # Rolling averages
    df['sales_7d_avg'] = df.groupby('sku')['sales'].rolling(window=7, min_periods=1).mean().reset_index(0, drop=True)
    df['sales_14d_avg'] = df.groupby('sku')['sales'].rolling(window=14, min_periods=1).mean().reset_index(0, drop=True)

    # One-hot encode categorical variables
    df = pd.get_dummies(df, columns=['season', 'weather'], drop_first=True)

    return df

# Example usage:
# cleaned_df = preprocess_csv('company_sales.csv')
# print(cleaned_df.head())
