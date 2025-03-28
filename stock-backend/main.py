from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.middleware.cors import CORSMiddleware
import requests

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys and URLs
GEMINI_API_KEY = "AIzaSyBwh2u-7WC_yapXaa3wY9Hh56PhxXhrxOA"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

RAPIDAPI_KEY = "75b4a1898cmsh366dc2dd8a3eca3p18243djsn0a59e3a4ff69"
RAPIDAPI_HOST = "yahoo-finance15.p.rapidapi.com"
RAPIDAPI_URL = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes"

# Database Connection
DATABASE_URL = "sqlite:///./stocks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# Stock Model
class Stock(Base):
    __tablename__ = "stocks"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)

# Create Tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Model for Adding Stock
class StockRequest(BaseModel):
    stock_symbol: str

# API Endpoints

@app.get("/get_stocks")
def get_stocks():
    session = SessionLocal()
    stocks = session.query(Stock).all()
    session.close()
    return {"stocks": [stock.symbol for stock in stocks]}

@app.get("/get_stock/{name}")
def get_stock(name: str):
    stock_symbol = get_actual_stock_name(name)
    return {"input": name, "stock_symbol": stock_symbol}

@app.post("/add_stock")
def add_stock(request: StockRequest):
    session = SessionLocal()
    existing_stock = session.query(Stock).filter(Stock.symbol == request.stock_symbol).first()

    if existing_stock:
        session.close()
        return {"message": f"{request.stock_symbol} is already in the database"}

    new_stock = Stock(symbol=request.stock_symbol)
    session.add(new_stock)
    session.commit()
    session.close()

    return {"message": f"{request.stock_symbol} added successfully!"}

@app.get("/get_stock_prices")
def get_stock_prices():
    session = SessionLocal()
    stocks = session.query(Stock).all()
    session.close()

    stock_prices = {}
    for stock in stocks:
        stock_prices[stock.symbol] = get_stock_price(stock.symbol)

    return stock_prices

# Function to Fetch Stock Prices
def get_stock_price(symbol):
    querystring = {"ticker": f"{symbol}"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    response = requests.get(RAPIDAPI_URL, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        try:
            quote_data = data["body"][0]  # Extract the first result
            return {
                "symbol": quote_data.get("symbol", "N/A"),
                "name": quote_data.get("shortName", "Unknown"),
                "price": quote_data.get("regularMarketPrice", "Price Not Available"),
                "currency": quote_data.get("currency", "N/A"),
                "market_state": quote_data.get("marketState", "N/A")
            }
        except (IndexError, KeyError):
            return {"error": "Stock data not found"}
    else:
        return {"error": f"Failed to fetch data. Status Code: {response.status_code}"}

# Function to Get Correct Stock Symbol using AI
def get_actual_stock_name(user_input: str):
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Find the correct or related stock ticker symbol for '{user_input}' and just reply back with only the ticker symbol or related one. I don't want a full sentence if no publicly traded ticker. Just reply with only the related symbol"
            }]
        }]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
