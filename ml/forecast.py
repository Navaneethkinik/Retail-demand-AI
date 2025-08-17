import pandas as pd
from prophet import Prophet

def forecast_company(df: pd.DataFrame, forecast_horizon: int = 30) -> dict:
    """
    Generate forecasts for all SKUs in the company dataset using Prophet.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe with 'sku', 'date', 'sales'.
        forecast_horizon (int): Number of days to forecast.
        
    Returns:
        dict: {sku: forecast_df} where forecast_df has columns ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
    """
    forecasts = {}
    skus = df['sku'].unique()
    
    for sku in skus:
        sku_df = df[df['sku'] == sku][['date', 'sales']].rename(columns={'date': 'ds', 'sales': 'y'})
        
        # Skip if not enough data
        if len(sku_df) < 2:
            continue
        
        model = Prophet()
        model.fit(sku_df)
        
        future = model.make_future_dataframe(periods=forecast_horizon)
        forecast = model.predict(future)
        
        # Keep only relevant columns
        forecasts[sku] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    
    return forecasts

# Example usage:
# cleaned_df = preprocess_csv('company_sales.csv')
# forecast_dict = forecast_company(cleaned_df, forecast_horizon=30)
# for sku, fc in forecast_dict.items():
#     print(f"Forecast for SKU {sku}")
#     print(fc.tail())
