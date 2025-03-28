import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this_is_a_secret_key"

    # Gemini API settings
    GEMINI_API_KEY = "AIzaSyBwh2u-7WC_yapXaa3wY9Hh56PhxXhrxOA"
    GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    # RapidAPI settings for Yahoo Finance
    RAPIDAPI_KEY = "75b4a1898cmsh366dc2dd8a3eca3p18243djsn0a59e3a4ff69"
    RAPIDAPI_HOST = "yahoo-finance15.p.rapidapi.com"
    RAPIDAPI_URL = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes"
