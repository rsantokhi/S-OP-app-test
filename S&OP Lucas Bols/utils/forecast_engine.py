"""Forecasting engine with multiple models: ETS, SARIMA, Prophet, Ensemble."""

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
import warnings

warnings.filterwarnings("ignore")


def calculate_mape(actual: np.ndarray, forecast: np.ndarray) -> float:
    """Calculate Mean Absolute Percentage Error."""
    if len(actual) == 0 or len(forecast) == 0:
        return np.nan

    # Filter out zero actuals to avoid division by zero
    mask = actual != 0
    if not mask.any():
        return np.nan

    return mean_absolute_percentage_error(actual[mask], forecast[mask]) * 100


def run_ets_forecast(series: pd.Series, horizon: int = 12) -> dict:
    """
    Run ETS (Exponential Smoothing) forecast.

    Args:
        series: Time series data
        horizon: Number of periods to forecast

    Returns:
        Dict with 'forecast' (array) and 'mape' (float)
    """
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        if len(series) < 13:
            # Not enough data for seasonal model
            return None

        # Remove NaN values
        series_clean = series.dropna()

        if len(series_clean) < 13:
            return None

        try:
            # Try multiplicative first (more common for positive-only series)
            model = ExponentialSmoothing(
                series_clean,
                trend="add",
                seasonal="add",
                seasonal_periods=12,
            )
            fit = model.fit(optimized=True, disp=False)
        except:
            # Fallback to simpler model
            model = ExponentialSmoothing(series_clean, trend="add", seasonal=None)
            fit = model.fit(optimized=True, disp=False)

        # Forecast
        forecast = fit.forecast(steps=horizon).values

        # Calculate MAPE on last 6 months if available
        if len(series_clean) >= 6:
            actual_last = series_clean.iloc[-6:].values
            fitted_last = fit.fittedvalues.iloc[-6:].values
            mape = calculate_mape(actual_last, fitted_last)
        else:
            mape = np.nan

        return {"forecast": forecast, "mape": mape, "model_name": "ETS"}

    except Exception as e:
        return None


def run_sarima_forecast(series: pd.Series, horizon: int = 12) -> dict:
    """
    Run SARIMA forecast with auto parameter selection.

    Args:
        series: Time series data
        horizon: Number of periods to forecast

    Returns:
        Dict with 'forecast' (array) and 'mape' (float)
    """
    try:
        from statsmodels.tsa.statespace.sarimax import SARIMAX

        series_clean = series.dropna()

        if len(series_clean) < 24:
            # Not enough data
            return None

        # Grid search over p,d,q
        best_aic = np.inf
        best_order = None
        best_fit = None

        for p in range(3):
            for d in range(2):
                for q in range(3):
                    try:
                        model = SARIMAX(
                            series_clean,
                            order=(p, d, q),
                            seasonal_order=(1, 0, 1, 12),
                            enforce_stationarity=False,
                            enforce_invertibility=False,
                        )
                        fit = model.fit(disp=False, maxiter=200)

                        if fit.aic < best_aic:
                            best_aic = fit.aic
                            best_order = (p, d, q)
                            best_fit = fit

                    except:
                        continue

        if best_fit is None:
            return None

        forecast = best_fit.get_forecast(steps=horizon).predicted_mean.values

        # Calculate MAPE
        if len(series_clean) >= 6:
            actual_last = series_clean.iloc[-6:].values
            fitted_last = best_fit.fittedvalues.iloc[-6:].values
            mape = calculate_mape(actual_last, fitted_last)
        else:
            mape = np.nan

        return {"forecast": forecast, "mape": mape, "model_name": "SARIMA"}

    except Exception as e:
        return None


def run_prophet_forecast(series: pd.Series, horizon: int = 12) -> dict:
    """
    Run Prophet forecast (Facebook's time series library).

    Args:
        series: Time series data with datetime index
        horizon: Number of periods to forecast

    Returns:
        Dict with 'forecast' (array) and 'mape' (float)
    """
    try:
        from prophet import Prophet

        series_clean = series.dropna()

        if len(series_clean) < 24:
            return None

        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        df_prophet = pd.DataFrame({
            "ds": series_clean.index,
            "y": series_clean.values,
        })

        # Handle non-numeric index
        if not isinstance(df_prophet["ds"], pd.DatetimeIndex):
            df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], errors="coerce")

        df_prophet = df_prophet.dropna()

        if len(df_prophet) < 24:
            return None

        # Fit model
        model = Prophet(
            yearly_seasonality=True,
            daily_seasonality=False,
            weekly_seasonality=False,
        )
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(df_prophet)

        # Forecast
        future = model.make_future_dataframe(periods=horizon, freq="MS")
        forecast_df = model.predict(future)
        forecast = forecast_df.iloc[-horizon:]["yhat"].values

        # Calculate MAPE
        if len(series_clean) >= 6:
            actual_last = series_clean.iloc[-6:].values
            # Use fitted values from training period
            fitted = forecast_df[forecast_df["ds"].isin(series_clean.index)]["yhat"].values
            if len(fitted) >= 6:
                mape = calculate_mape(actual_last, fitted[-6:])
            else:
                mape = np.nan
        else:
            mape = np.nan

        return {"forecast": forecast, "mape": mape, "model_name": "Prophet"}

    except ImportError:
        return None
    except Exception as e:
        return None


def run_naive_seasonal_forecast(series: pd.Series, horizon: int = 12) -> dict:
    """
    Run naive seasonal forecast (previous year's same month).

    Args:
        series: Time series data
        horizon: Number of periods to forecast

    Returns:
        Dict with 'forecast' (array) and 'mape' (float)
    """
    series_clean = series.dropna()

    if len(series_clean) < 12:
        return None

    # Use last 12 months as forecast
    if len(series_clean) >= 12:
        seasonal_pattern = series_clean.iloc[-12:].values
    else:
        seasonal_pattern = series_clean.values

    # Repeat pattern for horizon
    forecast = np.tile(seasonal_pattern, int(np.ceil(horizon / 12)))[:horizon]

    # Calculate MAPE
    if len(series_clean) >= 24:
        actual_test = series_clean.iloc[-12:-6].values
        forecast_test = seasonal_pattern[:6]
        mape = calculate_mape(actual_test, forecast_test)
    else:
        mape = np.nan

    return {"forecast": forecast, "mape": mape, "model_name": "Naive Seasonal"}


def run_ensemble(series: pd.Series, horizon: int = 12) -> dict:
    """
    Run ensemble forecast combining multiple models.

    All available models are run, weighted by 1/MAPE (inverse error).

    Args:
        series: Time series data
        horizon: Number of periods to forecast

    Returns:
        Dict with ensemble forecast, individual model results, and best model
    """
    results = {}

    # Run all models
    ets_result = run_ets_forecast(series, horizon)
    if ets_result:
        results["ETS"] = ets_result

    sarima_result = run_sarima_forecast(series, horizon)
    if sarima_result:
        results["SARIMA"] = sarima_result

    prophet_result = run_prophet_forecast(series, horizon)
    if prophet_result:
        results["Prophet"] = prophet_result

    naive_result = run_naive_seasonal_forecast(series, horizon)
    if naive_result:
        results["Naive_Seasonal"] = naive_result

    if not results:
        return None

    # Find best model by lowest MAPE
    best_model = None
    best_mape = np.inf
    for name, result in results.items():
        if not np.isnan(result["mape"]) and result["mape"] < best_mape:
            best_mape = result["mape"]
            best_model = name

    # If no MAPE available, pick first model
    if best_model is None:
        best_model = list(results.keys())[0]

    # Calculate weights: 1/MAPE for each model
    weights = {}
    valid_results = {k: v for k, v in results.items() if not np.isnan(v.get("mape", np.nan))}

    if valid_results:
        sum_inv_mape = sum(1 / v["mape"] for v in valid_results.values() if v["mape"] > 0)
        if sum_inv_mape > 0:
            for name, result in valid_results.items():
                if result["mape"] > 0:
                    weights[name] = (1 / result["mape"]) / sum_inv_mape
    else:
        # Equal weights if no valid MAPE
        for name in results.keys():
            weights[name] = 1.0 / len(results)

    # Ensemble forecast: weighted average
    ensemble_forecast = np.zeros(horizon)
    for name, result in results.items():
        weight = weights.get(name, 0)
        ensemble_forecast += weight * result["forecast"]

    return {
        "forecast": ensemble_forecast,
        "individual_models": results,
        "weights": weights,
        "best_model": best_model,
        "best_mape": best_mape,
        "model_name": "Ensemble",
    }


def run_forecast(
    series: pd.Series, model: str = "ensemble", horizon: int = 12
) -> np.ndarray:
    """
    Run forecast with specified model.

    Args:
        series: Time series data
        model: One of ['ensemble', 'ets', 'sarima', 'prophet', 'naive']
        horizon: Number of periods to forecast

    Returns:
        Forecast array
    """
    if len(series) < 12:
        # Not enough data, return naive forecast
        series_clean = series.dropna()
        return np.full(horizon, series_clean.mean())

    model_lower = model.lower()

    if model_lower == "ensemble":
        result = run_ensemble(series, horizon)
    elif model_lower == "ets":
        result = run_ets_forecast(series, horizon)
    elif model_lower == "sarima":
        result = run_sarima_forecast(series, horizon)
    elif model_lower == "prophet":
        result = run_prophet_forecast(series, horizon)
    elif model_lower == "naive":
        result = run_naive_seasonal_forecast(series, horizon)
    else:
        # Default to ensemble
        result = run_ensemble(series, horizon)

    if result is None:
        # Fallback
        series_clean = series.dropna()
        if len(series_clean) > 0:
            return np.full(horizon, series_clean.mean())
        else:
            return np.zeros(horizon)

    return result.get("forecast", np.zeros(horizon))


def calculate_safety_stock(
    series: pd.Series, lead_time_days: float, service_level: float = 0.98
) -> float:
    """
    Calculate safety stock.

    Formula: SS = Z(service_level) × σ(demand) × √(lead_time_months)

    Args:
        series: Historical demand series
        lead_time_days: Lead time in days
        service_level: Service level (default 98%)

    Returns:
        Safety stock quantity
    """
    from scipy import stats

    series_clean = series.dropna()

    if len(series_clean) < 2:
        return 0

    # Calculate demand standard deviation
    demand_std = series_clean.std()

    # Z-score for service level
    z_score = stats.norm.ppf(service_level)

    # Lead time in months (assuming 30 days per month)
    lead_time_months = lead_time_days / 30.0

    # Safety stock
    safety_stock = z_score * demand_std * np.sqrt(lead_time_months)

    return max(0, safety_stock)


def forecast_with_confidence_interval(
    series: pd.Series, model: str = "ensemble", horizon: int = 12, confidence: float = 0.95
) -> dict:
    """
    Generate forecast with confidence intervals.

    Args:
        series: Time series data
        model: Forecast model to use
        horizon: Number of periods to forecast
        confidence: Confidence level for interval (default 95%)

    Returns:
        Dict with forecast, lower_bound, upper_bound
    """
    forecast = run_forecast(series, model, horizon)

    # Simple confidence interval based on historical std
    series_clean = series.dropna()
    if len(series_clean) > 1:
        std = series_clean.std()
        from scipy import stats

        z = stats.norm.ppf((1 + confidence) / 2)
        margin = z * std

        lower = forecast - margin
        upper = forecast + margin

        lower = np.maximum(lower, 0)  # Can't have negative quantity
    else:
        lower = forecast * 0.8
        upper = forecast * 1.2

    return {
        "forecast": forecast,
        "lower_bound": lower,
        "upper_bound": upper,
    }
