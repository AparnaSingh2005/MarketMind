
from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PATH = DATA_DIR / "nifty50_daily.csv"

TICKER = "^NSEI"


def download_market_data(period: str = "5y") -> pd.DataFrame:
    """Download daily NIFTY 50 historical market data."""

    df = yf.download(
        TICKER,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        multi_level_index=False,
    )

    if df.empty:
        raise RuntimeError(
            "No market data received. Check your internet connection "
            "or try again later."
        )

    # Handle both regular and MultiIndex column formats.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"
    df = df.reset_index()

    required = ["Date", "Open", "High", "Low", "Close", "Volume"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[required].copy()
    df = df.dropna(subset=["Date", "Close"])
    df = df.drop_duplicates(subset=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    if (df["Close"] <= 0).any():
        raise ValueError("Invalid non-positive closing prices found.")

    return df


def save_market_data(df: pd.DataFrame) -> Path:
    """Save the validated dataset locally."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    return DATA_PATH


def main() -> None:
    print("Downloading NIFTY 50 historical data...")

    df = download_market_data()
    path = save_market_data(df)

    print(f"\nRows downloaded: {len(df)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Saved to: {path}")
    print("\nLatest 5 records:")
    print(df.tail().to_string(index=False))
    print("\nMissing values:")
    print(df.isnull().sum().to_string())


if __name__ == "__main__":
    main()
