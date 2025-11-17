import {useState, useEffect} from 'react';
import {Routes, Route, Link} from "react-router-dom";
import dayjs from "dayjs"

import HomePage from "./pages/HomePage";

function App() {
    const [selectedKeyword, setSelectedKeyword] = useState("");
    const [data, setData] = useState([]);
    const [warning, setWarning] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [graphType, setGraphType] = useState("stock")
    const [newsType, setNewsType] = useState("graph")

    const handle_dates_change = async ({ start_date, end_date }) => {
        if (!(start_date && end_date)) return;
        if (dayjs(end_date).isAfter(dayjs())) {
            setWarning("End date can't be future");
            setData([]);
            return;
        }

        if (dayjs(start_date) > dayjs(end_date)) {
            setWarning("Start date must be earlier than End date")
            setData([]);
            return
        }

        setWarning("");
        setStartDate(start_date);
        setEndDate(end_date);
    };

    const handleSubjectToggle = (type) => {
        setGraphType(type);
        setSelectedKeyword("");
        setData([]);
        setWarning("");
    }

    const handleNewsToggle = (type) => {
        setNewsType(type);
    }

    useEffect(() => {
        if (!selectedKeyword || !startDate || !endDate) return;

        const fetchAll = async() => {
            try {

                const trendUrl = `http://127.0.0.1:8000/trend?start=${startDate}&end=${endDate}&keyword=${encodeURIComponent(selectedKeyword)}`
                let priceUrl = ""

                if (graphType === "stock") priceUrl = `http://127.0.0.1:8000/stock?start=${startDate}&end=${endDate}&keyword=${encodeURIComponent(selectedKeyword)}`
                else priceUrl = `http://127.0.0.1:8000/apartment-trades?start_ym=${startDate.slice(0,7)}&end_ym=${endDate.slice(0,7)}&start_day=${startDate.slice(7,10)}&end_day=${endDate.slice(7,10)}`

                const [trendRes, priceRes] = await Promise.all([
                    fetch(trendUrl),
                    fetch(priceUrl)
                ])

                if (!trendRes.ok || !priceRes.ok) {
                    throw new Error("API Error");
                }

                const trendJson = await trendRes.json();
                const priceJson = await priceRes.json();

                const trendData = trendJson.data;
                const stockData = priceJson.data ? priceJson.data : priceJson;

                const mergedData = mergeWith(trendData, stockData);

                setData(mergedData);

            } catch (err) {
                console.error(err);
                setWarning("Data Error");
            }
        };

        fetchAll();
    }, [selectedKeyword, startDate, endDate, graphType]);

    return (
        <div>
            <nav style={{padding: "12px", marginBottom: "16px", borderBottom: "1px solid #ddd"}}>
                <Link to="/" style={{marginRight: "12px"}}>홈</Link>
            </nav>

            <Routes>
                <Route
                    path="/"
                    element={
                        <HomePage
                            selectedKeyword={selectedKeyword}
                            setSelectedKeyword={setSelectedKeyword}
                            data={data}
                            warning={warning}
                            startDate={startDate}
                            endDate={endDate}
                            graphType={graphType}
                            newsType={newsType}
                            handle_dates_change={handle_dates_change}
                            handleSubjectToggle={handleSubjectToggle}
                            handleNewsToggle={handleNewsToggle}
                        />
                    }
                />
            </Routes>
        </div>
    );
}

function mergeWith(trendData, stockData) {
    const stockMap = new Map(stockData.map(s => [s.date, s.price]));
    let lastPrice = null;

    return trendData.map(t => {
        const date = t.date;
        if(stockMap.has(date)) lastPrice = stockMap.get(date);

        return {
            date,
            value: t.value,
            price: lastPrice
        }
    })
}

export default App;