
import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_loader import DATA_PATH, download_market_data, save_market_data

st.set_page_config(
    page_title="MarketMind",
    page_icon="📈",
    layout="wide",
)

st.title("MarketMind")
st.subheader("AI-Powered Financial Risk Intelligence")
st.caption("Day 1 | Historical Market Data Explorer")

if st.button("Download / Refresh NIFTY 50 Data"):
    try:
        with st.spinner("Fetching historical data..."):
            df = download_market_data()
            save_market_data(df)
        st.success("Market data downloaded and saved.")
    except Exception as exc:
        st.error(f"Data download failed: {exc}")

if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])

    if df.empty:
        st.warning("The saved dataset is empty.")
        st.stop()

    col1, col2, col3 = st.columns(3)
    col1.metric("Records", f"{len(df):,}")
    col2.metric("Latest Close", f"{df['Close'].iloc[-1]:,.2f}")
    col3.metric("Latest Date", df["Date"].iloc[-1].strftime("%d %b %Y"))

    fig = px.line(
        df,
        x="Date",
        y="Close",
        title="NIFTY 50 Historical Closing Prices",
        labels={"Close": "Adjusted closing price", "Date": "Date"},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Latest Market Records")
    st.dataframe(df.tail(10), use_container_width=True)

    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="nifty50_daily.csv",
        mime="text/csv",
    )
else:
    st.info(
        "No local dataset found. Run the data pipeline first "
        "or click the download button above."
    )
