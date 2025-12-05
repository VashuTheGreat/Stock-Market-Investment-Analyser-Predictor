import streamlit as st
from main import give_analysis
import json

# Page configuration
st.set_page_config(
    page_title="Stock Market Investment Analyser",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 2rem;
    }
    
    /* Title styling */
    h1 {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d2d44 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #8fd3f4;
        font-weight: 600;
    }
    
    /* Input field styling */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(143, 211, 244, 0.3);
        border-radius: 12px;
        color: white;
        padding: 12px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #8fd3f4;
        box-shadow: 0 0 20px rgba(143, 211, 244, 0.3);
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        color: #0f0c29;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(132, 250, 176, 0.4);
    }
    
    /* Card styling */
    .stock-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .stock-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(143, 211, 244, 0.2);
        border-color: rgba(143, 211, 244, 0.3);
    }
    
    .stock-ticker {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
    }
    
    .stock-reason {
        color: rgba(255, 255, 255, 0.8);
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Suggestion box */
    .suggestion-box {
        background: linear-gradient(135deg, rgba(132, 250, 176, 0.1) 0%, rgba(143, 211, 244, 0.1) 100%);
        border-left: 4px solid #84fab0;
        border-radius: 12px;
        padding: 24px;
        margin: 24px 0;
        color: white;
    }
    
    .suggestion-title {
        font-size: 24px;
        font-weight: 600;
        color: #84fab0;
        margin-bottom: 12px;
    }
    
    .suggestion-text {
        font-size: 18px;
        line-height: 1.8;
        color: rgba(255, 255, 255, 0.9);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin-left: 12px;
    }
    
    .badge-buy {
        background: linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%);
        color: #0f0c29;
    }
    
    .badge-sell {
        background: linear-gradient(120deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .badge-hold {
        background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%);
        color: #0f0c29;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-color: #8fd3f4 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(143, 211, 244, 0.5), transparent);
        margin: 32px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>📈 Stock Market Investment Analyser</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Analysis Settings")
    st.markdown("---")
    
    tickers = st.text_input(
        "Stock Tickers",
        placeholder="e.g., AAPL, MSFT, GOOGL",
        help="Enter stock tickers separated by commas",
        key="tickers"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    analyze_button = st.button("🚀 Analyze Stocks")
    
    st.markdown("---")
    st.markdown("""
    ### 💡 Tips
    - Use valid stock tickers (e.g., AAPL for Apple)
    - Separate multiple tickers with commas
    - Analysis includes technical & sentiment data
    """)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'stock_data_cache' not in st.session_state:
    st.session_state.stock_data_cache = {}

# Main content
result = None

if analyze_button:
    if not tickers or tickers.strip() == "":
        st.error("⚠️ Please enter at least one stock ticker")
    else:
        ticker_list = [ticker.strip() for ticker in tickers.split(",") if ticker.strip()]
        
        with st.spinner("🔍 Analyzing stocks... This may take a moment."):
            result = give_analysis(ticker_list=ticker_list)
            st.session_state.analysis_result = result

# Use session state result if available
if st.session_state.analysis_result:
    result = st.session_state.analysis_result

if result:
    # Parse JSON result
    try:
        if isinstance(result, str):
            data = json.loads(result)
        else:
            data = result
        
        # Display suggestions
        st.markdown(f"""
        <div class="suggestion-box">
            <div class="suggestion-title">💼 Investment Recommendations</div>
            <div class="suggestion-text">{data['suggestions']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Display stocks in columns
        st.markdown("### 📊 Detailed Stock Analysis")
        
        for ticker, info in data['stocks'].items():
            reason = info['reason']
            
            # Determine badge based on keywords in reason
            badge_html = ""
            reason_lower = reason.lower()
            if any(word in reason_lower for word in ['buy', 'strong', 'uptrend', 'positive']):
                badge_html = '<span class="badge badge-buy">BUY</span>'
            elif any(word in reason_lower for word in ['sell', 'downtrend', 'negative', 'avoid']):
                badge_html = '<span class="badge badge-sell">SELL</span>'
            else:
                badge_html = '<span class="badge badge-hold">HOLD</span>'
            
            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-ticker">{ticker}{badge_html}</div>
                <div class="stock-reason">{reason}</div>
            </div>
            """, unsafe_allow_html=True)
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Error parsing results: {e}")
        st.code(result)
    except KeyError as e:
        st.error(f"❌ Missing expected field in results: {e}")
        st.code(result)
else:
    # Welcome message when no analysis has been run
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; color: rgba(255, 255, 255, 0.7);">
        <h2 style="color: #8fd3f4; margin-bottom: 20px;">Welcome to Stock Market Investment Analyser</h2>
        <p style="font-size: 18px; line-height: 1.8;">
            Get AI-powered investment recommendations based on:<br>
            ✨ Technical Analysis<br>
            ✨ Sentiment Analysis<br>
            ✨ Market Trends<br><br>
            Enter stock tickers in the sidebar to get started!
        </p>
    </div>
    """, unsafe_allow_html=True)





# predictor and graphs



# app.py
import pandas as pd
import datetime as dt
import yfinance as yf
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import RendererAgg
import threading
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

_lock = threading.Lock()

model = load_model('stock_model.keras')


def graphable(df):
    df = df.iloc[1:]

    for col in df.columns:
        if df[col].dtype == "object" and col != "Date":
            df[col] = df[col].astype(float)
    return df

def get_stock_data(stock, days=200):
    start = (dt.datetime.now() - dt.timedelta(days=days)).date()
    end = dt.datetime.now().date()
    df = yf.download(stock, start=start, end=end)
    df.reset_index(inplace=True)
    df.to_csv('stock_data.csv')
    df=pd.read_csv('stock_data.csv')
    df=graphable(df)
    return df

def predict_next_price(stock):
    df = get_stock_data(stock)
    last_100 = df['Close'].tail(100).values.reshape(-1, 1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(last_100)
    scaled = scaled.reshape(1, 100, 1)

    pred = model.predict(scaled)
    pred = scaler.inverse_transform(pred.reshape(-1, 1))

    return pred[0, 0]
def plot_candlestick_streamlit(df):
    fig = go.Figure(
        data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])

    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

def plot_matplotlib_streamlit(y, title="Plot", xlabel="X", ylabel="Y"):
    # plt.figure(figsize=(12, 6))
    # plt.plot(df['Close'], label=f'{stock} Close Price', linewidth=2)
    # plt.title('Close Price vs Close Price')
    # plt.xlabel('Date')
    # plt.ylabel('Close Price')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # plt.figure(figsize=(12, 6))
    # plt.plot(df['High'], label=f'{stock} Close Price', linewidth=2)
    # plt.title('Close Price vs Close Price')
    # plt.xlabel('Date')
    # plt.ylabel('Close Price')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    # %%
    # plt.figure(figsize=(12, 6))
    # plt.plot(df['Volume'], label=f'{stock} Close Price', linewidth=2)
    # plt.title('Close Price vs Close Price')
    # plt.xlabel('Date')
    # plt.ylabel('Close Price')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(y, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    st.pyplot(fig)

def plot_moving_average_streamlit(df, stock):

    ma100 = df['Close'].rolling(100).mean()
    ma200 = df['Close'].rolling(200).mean()
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df['Close'], label=f'{stock} Close', linewidth=2)
    ax.plot(ma100, label='MA 100', linewidth=2)
    ax.plot(ma200, label='MA 200', linewidth=2)
    ax.set_title(f'{stock} Close Price & Moving Averages')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def plot_ema_streamlit(df, stock):
    ema100 = df['Close'].ewm(span=100, adjust=False).mean()
    ema200 = df['Close'].ewm(span=200, adjust=False).mean()
    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df['Close'], label=f'{stock} Close', linewidth=2)
    ax.plot(ema100, label='EMA 100', linewidth=2)
    ax.plot(ema200, label='EMA 200', linewidth=2)
    ax.set_title(f'{stock} Close Price & EMA')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def model_performance_streamlit(df):
    if len(df) < 101:
        st.warning("Not enough data for performance plot.")
        return

    data = df['Close'].values.reshape(-1,1)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data)

    x_test, y_test = [], []
    for i in range(100, len(scaled_data)):
        x_test.append(scaled_data[i-100:i,0])
        y_test.append(scaled_data[i,0])
    x_test, y_test = np.array(x_test), np.array(y_test)
    x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

    y_pred = model.predict(x_test)
    y_pred = scaler.inverse_transform(y_pred)
    y_test = scaler.inverse_transform(y_test.reshape(-1,1))

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(y_test, label='Original Price', linewidth=1)
    ax.plot(y_pred, label='Predicted Price', linewidth=1)
    ax.set_title('Model Performance')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)


# Stock Prediction Dashboard Section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("## 📊 Stock Prediction Dashboard", unsafe_allow_html=True)

# Initialize chart display state
if 'show_charts' not in st.session_state:
    st.session_state.show_charts = False
if 'chart_tickers' not in st.session_state:
    st.session_state.chart_tickers = []

if st.button("📈 Load Data & Show Plots for All Stocks"):
    if not tickers or tickers.strip() == "":
        st.error("⚠️ Please enter at least one stock ticker in the sidebar first")
    else:
        ticker_list = [ticker.strip() for ticker in tickers.split(",") if ticker.strip()]
        st.session_state.show_charts = True
        st.session_state.chart_tickers = ticker_list

# Display charts if they were loaded
if st.session_state.show_charts and st.session_state.chart_tickers:
    for stock_ticker in st.session_state.chart_tickers:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(132, 250, 176, 0.15) 0%, rgba(143, 211, 244, 0.15) 100%); 
                    border-radius: 16px; padding: 20px; margin: 30px 0;">
            <h2 style="color: #84fab0; text-align: center; margin: 0;">
                📈 {stock_ticker} - Complete Analysis
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            with st.spinner(f"Loading data for {stock_ticker}..."):
                df = get_stock_data(stock_ticker, days=2000)
            
            # Candlestick Chart
            st.markdown("### 🕯️ Candlestick Chart")
            plot_candlestick_streamlit(df)
            
            # Close Price Chart
            st.markdown("### 💰 Close Price Chart")
            plot_matplotlib_streamlit(df['Close'], title=f"{stock_ticker} Close Price", ylabel="Close Price")
            
            # High Price Chart
            st.markdown("### 📊 High Price Chart")
            plot_matplotlib_streamlit(df['High'], title=f"{stock_ticker} High Price", ylabel="High Price")
            
            # Volume Chart
            st.markdown("### 📦 Volume Chart")
            plot_matplotlib_streamlit(df['Volume'], title=f"{stock_ticker} Volume", ylabel="Volume")
            
            # Moving Averages
            st.markdown("### 📉 Moving Averages")
            plot_moving_average_streamlit(df, stock_ticker)
            
            # Exponential Moving Averages
            st.markdown("### 📈 Exponential Moving Averages")
            plot_ema_streamlit(df, stock_ticker)
            
            # Model Performance
            st.markdown("### 🎯 Model Performance")
            model_performance_streamlit(df)
            
            # Divider between stocks
            st.markdown("<hr style='margin: 50px 0;'>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error loading data for {stock_ticker}: {str(e)}")
            st.markdown("<hr style='margin: 50px 0;'>", unsafe_allow_html=True)

if st.button("🔮 Predict Next Price for All Stocks"):
    if not tickers or tickers.strip() == "":
        st.error("⚠️ Please enter at least one stock ticker in the sidebar first")
    else:
        ticker_list = [ticker.strip() for ticker in tickers.split(",") if ticker.strip()]
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(132, 250, 176, 0.1) 0%, rgba(143, 211, 244, 0.1) 100%); 
                    border-left: 4px solid #84fab0; border-radius: 12px; padding: 24px; margin: 24px 0;">
            <h3 style="color: #84fab0; margin-bottom: 20px;">🔮 Price Predictions</h3>
        """, unsafe_allow_html=True)
        
        for stock_ticker in ticker_list:
            try:
                with st.spinner(f"Predicting price for {stock_ticker}..."):
                    next_price = predict_next_price(stock_ticker)
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 16px; margin: 12px 0;">
                    <span style="font-size: 20px; font-weight: 600; color: #8fd3f4;">{stock_ticker}</span>
                    <span style="float: right; font-size: 24px; font-weight: 700; color: #84fab0;">${next_price:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error predicting price for {stock_ticker}: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)