import marimo

__generated_with = "0.23.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import fedfred as fd
    import yfinance as yf
    import plotly.express as px
    from dotenv import load_dotenv
    import os

    return fd, load_dotenv, mo, os, px


@app.cell
def _(mo):
    mo.md(r"""
    1. Use the fedfred package from PyPI to download the daily spot oil prices from FRED for West Texas Intermediate (WTI) and Brent oil. These are known as the DCOILWTICO and DCOILBRENTEU data sets. Also download data on the Consumer Price Index (CPI) and daily natural gas prices. These are the series: CPIAUCSL and DHHNGSP. Only keep rows for which there's data on all four series. Join all four series into a  single data frame.
    """)
    return


@app.cell
def _(fd, load_dotenv, os):
    load_dotenv()
    api_key = os.getenv("FEDFRED_API_KEY")

    fred = fd.FredAPI(api_key)
    return (fred,)


@app.cell
def _(fred):
    wti = fred.get_series_observations('DCOILWTICO')
    return (wti,)


@app.cell
def _(wti):
    wti.head(3)
    return


@app.cell
def _(fred):
    brent = fred.get_series_observations('DCOILBRENTEU')
    return (brent,)


@app.cell
def _(brent):
    brent.head(3)
    return


@app.cell
def _(fred):
    cpi = fred.get_series_observations('CPIAUCSL')
    return (cpi,)


@app.cell
def _(cpi):
    cpi.head(3)
    return


@app.cell
def _(fred):
    natural_gas = fred.get_series_observations('DHHNGSP')
    return (natural_gas,)


@app.cell
def _(natural_gas):
    natural_gas.head(3)
    return


@app.cell
def _(brent, cpi, natural_gas, wti):
    wti_df = wti[["value"]].rename(columns={"value": "wti"})
    brent_df = brent[["value"]].rename(columns={"value": "brent"})
    cpi_df = cpi[["value"]].rename(columns={"value": "cpi"})
    gas_df = natural_gas[["value"]].rename(columns={"value": "natural_gas"})

    oil_df = (
        wti_df
        .join(brent_df, how="inner")
        .join(cpi_df, how="inner")
        .join(gas_df, how="inner")
        .dropna()
    )
    return (oil_df,)


@app.cell
def _(oil_df):
    oil_df.sample(15)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    2. Plot oil prices over time. Are oil prices currently at an all-time high? (If not, then when were they?)
    """)
    return


@app.cell
def _(oil_df, px):
    (
        oil_df
        .sort_index()
        .pipe(lambda df_: px.line(df_, x=df_.index, y=['wti', 'brent']))
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Oil Prices Levels:

    According to the plot, oil prices are about \$62 per barrel most recently as of Dec 2025, which is not the all time high. Oil prices were highest in Jul 2008 at ~\$140 per barrel.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    3.  Is one price (WTI vs. Brent) consistently higher than the other in all data? Since 2000? Since 2010? Create a line plot showing both spot prices over time. Also show a scatterplot, with a trend line, showing the correlation between the two measures. How do you explain this correlation?
    """)
    return


@app.cell
def _(oil_df, px):
    (
        oil_df
        .sort_index()
        .pipe(lambda df_: px.scatter(df_, x='wti', y='brent', trendline='ols'))
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    4. Now plot oil prices against inflation. Is there a correlation? If yes, what is explanation for the relationship between oil prices and inflation?
    """)
    return


@app.cell
def _(cpi):
    inflation = (
        cpi
        .filter(like='value')
        .sort_index()
        .pct_change(12)
        .mul(100)
        .dropna()
    )
    return (inflation,)


@app.cell
def _(inflation):
    inflation.head(4)
    return


@app.cell
def _(oil_df):
    monthly_oil_prices = (
        oil_df
        .resample('1MS')
        .mean()
    )
    return (monthly_oil_prices,)


@app.cell
def _(monthly_oil_prices):
    monthly_oil_prices.head(4)
    return


@app.cell
def _(inflation, monthly_oil_prices):
    inf_oil = (
        inflation
        .join(monthly_oil_prices, how='left')
        .rename(columns={'value': 'inflation', 'value_wti': 'wti', 'value_brent': 'brent'})
    )
    return (inf_oil,)


@app.cell
def _(inf_oil):
    inf_oil.head(3)
    return


@app.cell
def _(inf_oil):
    (
        inf_oil
        .sort_index()
        .pipe()
    )
    return


if __name__ == "__main__":
    app.run()
