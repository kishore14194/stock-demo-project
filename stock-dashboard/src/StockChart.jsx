import React, { useState, useEffect } from "react";
import axios from "axios";

const StockDashboard = () => {
    const [stocks, setStocks] = useState([]); // Store stock list
    const [stockPrices, setStockPrices] = useState({}); // Store stock prices
    const [loading, setLoading] = useState(false);
    const [inputStock, setInputStock] = useState(""); // User input for AI search
    const [suggestedStock, setSuggestedStock] = useState(null); // AI suggested stock

    // ✅ Fetch stock list from backend (SQLAlchemy DB)
    useEffect(() => {
        const fetchStocks = async () => {
            try {
                const response = await axios.get("http://localhost:8000/get_stocks");
                setStocks(response.data.stocks);  // Extract stock symbols
            } catch (error) {
                console.error("Error fetching stocks:", error);
            }
        };
        fetchStocks();
    }, []);

    // ✅ Fetch all stock prices dynamically
    const fetchStockPrices = async () => {
        setLoading(true);
        try {
            const response = await axios.get("http://localhost:8000/get_stock_prices");
            setStockPrices(response.data);
        } catch (error) {
            console.error("Error fetching stock prices:", error);
        }
        setLoading(false);
    };

    // ✅ Use Gemini AI API to find related stock name
    const fetchStockSuggestion = async () => {
        try {
            const response = await axios.get(`http://localhost:8000/get_stock/${inputStock}`);
            setSuggestedStock(response.data);
        } catch (error) {
            console.error("Error fetching stock suggestion:", error);
        }
    };

    // ✅ Add AI-suggested stock to the database
    const addStockToDatabase = async () => {
        if (!suggestedStock) return;
        try {
            await axios.post("http://localhost:8000/add_stock", {
                stock_symbol: suggestedStock.stock_symbol
            });
            setStocks([...stocks, suggestedStock.stock_symbol]); // Update state
            setSuggestedStock(null);
            setInputStock("");
        } catch (error) {
            console.error("Error adding stock:", error);
        }
    };

    // Fetch stock prices on component mount
    useEffect(() => {
        if (stocks.length > 0) {
            fetchStockPrices();
        }
    }, [stocks]);

    return (
        <div className="p-4 bg-gray-100 min-h-screen">
            <h1 className="text-2xl font-bold mb-4">📈 Stock Market Dashboard</h1>

            {/* 🔹 Find Stock Section (Moved to the Top) */}
            <div className="flex flex-col md:flex-row items-center gap-3 mb-6">
                <input
                    type="text"
                    placeholder="Enter a stock name (e.g., Jio)"
                    value={inputStock}
                    onChange={(e) => setInputStock(e.target.value)}
                    className="p-2 border rounded-md w-full md:w-auto"
                />
                <button onClick={fetchStockSuggestion} className="bg-blue-500 text-white px-4 py-2 rounded">
                    🔍 Find Stock
                </button>
            </div>

            {/* 🔹 AI-Suggested Stock */}
            {suggestedStock && (
                <div className="mt-4 p-4 bg-green-100 shadow-md rounded-lg">
                    <h2 className="text-lg font-semibold">{suggestedStock.input} ({suggestedStock.stock_symbol})</h2>
                    <button onClick={addStockToDatabase} className="bg-green-500 text-white px-4 py-2 rounded mt-2">
                        ✅ Add to Database
                    </button>
                </div>
            )}

            {/* 🔹 Show Stock Data */}
            {loading ? (
                <p>Loading stock prices...</p>
            ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {stocks.map((symbol) => {
                        const stockData = stockPrices[symbol] || {};
                        return (
                            <div key={symbol} className="p-4 bg-white shadow-md rounded-lg">
                                <h2 className="text-lg font-semibold">{stockData.name || symbol}</h2>
                                <p>Symbol: {symbol}</p>
                                <p>Price: ${stockData.price} {stockData.currency || "N/A"}</p>
                                <p>Market State: {stockData.market_state || "N/A"}</p>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default StockDashboard;
