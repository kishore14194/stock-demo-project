import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/stock/";

const StockSelector = () => {
    const [stocks] = useState(["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]);
    const [selectedStock, setSelectedStock] = useState(stocks[0]);
    const [stockData, setStockData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchStockData(selectedStock);
    }, [selectedStock]);

    const fetchStockData = async (symbol) => {
        setLoading(true);
        try {
            const response = await axios.get(`${API_URL}${symbol}`);
            setStockData(response.data);
        } catch (error) {
            console.error("Error fetching stock data:", error);
        }
        setLoading(false);
    };

    return (
        <div className="p-4 bg-white shadow-md rounded-lg">
            <h2 className="text-xl font-semibold mb-2">Select a Stock</h2>
            <select
                className="p-2 border rounded"
                value={selectedStock}
                onChange={(e) => setSelectedStock(e.target.value)}
            >
                {stocks.map((stock) => (
                    <option key={stock} value={stock}>
                        {stock}
                    </option>
                ))}
            </select>

            {loading ? (
                <p className="mt-4">Loading...</p>
            ) : (
                stockData && (
                    <div className="mt-4">
                        <h3 className="text-lg font-semibold">{selectedStock} Stock Price</h3>
                        <p>Price: ${stockData.price || "N/A"}</p>
                    </div>
                )
            )}
        </div>
    );
};

export default StockSelector;
