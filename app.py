from flask import Flask, render_template, request, flash, jsonify
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# A simple health-check endpoint
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# Homepage route: renders the form and (if submitted) displays stock info
@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    if request.method == "POST":
        stock_name = request.form.get("stock_name")
        if stock_name:
            # Convert stock name to ticker using Gemini API
            stock_ticker = get_stock_ticker(stock_name)
            # Fetch stock quote using RapidAPI
            stock_data = get_stock_quote(stock_ticker)
            if not stock_data:
                flash("Unable to retrieve stock data. Please try again.", "warning")
    return render_template("index.html", stock_data=stock_data)


def get_stock_ticker(stock_name):
    """Calls the Gemini API to convert a stock name into a ticker symbol."""
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Find the correct or related stock ticker symbol for '{stock_name}' and reply with just the ticker symbol. If the stock name is not found, reply with the corresponding or related company stock symbol."
            }]
        }]
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(app.config["GEMINI_URL"], json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        ticker = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        return ticker if ticker else stock_name
    except Exception as e:
        print("Error in get_stock_ticker:", e)
        return stock_name  # fallback


def get_stock_quote(ticker):
    """Calls RapidAPI to fetch stock quote for the given ticker."""
    querystring = {"ticker": ticker}
    headers = {
        "x-rapidapi-key": app.config["RAPIDAPI_KEY"],
        "x-rapidapi-host": app.config["RAPIDAPI_HOST"]
    }
    try:
        response = requests.get(app.config["RAPIDAPI_URL"], headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        # Expecting data["body"] to be a list with one element containing the quote
        quote_data = data.get("body", [{}])[0]
        return {
            "ticker": quote_data.get("symbol", "N/A"),
            "name": quote_data.get("shortName", "Unknown"),
            "price": quote_data.get("regularMarketPrice", "N/A"),
            "currency": quote_data.get("currency", "N/A"),
            "market_state": quote_data.get("marketState", "N/A")
        }
    except Exception as e:
        print("Error in get_stock_quote:", e)
        return None


if __name__ == "__main__":
    app.run(debug=True)
