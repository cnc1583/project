import {useState, useEffect} from 'react';
import {Routes, Route} from "react-router-dom";
import dayjs from "dayjs"

import HomePage from "./pages/HomePage";

function App() {
    const [selectedKeyword, setSelectedKeyword] = useState("");
    const [data, setData] = useState([]);
    const [stockTopicData, setStockTopicData] = useState([]);
    const [warning, setWarning] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [graphType, setGraphType] = useState("stock");
    const [newsType, setNewsType] = useState("graph");
    const [loading, setLoading] = useState(false);
    const [selectedClusterId, setSelectedClusterId] = useState(null);

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
        if(!startDate || !endDate) return;

        const fetchTopics = async() => {
            try {
                const topicUrl = `http://127.0.0.1:8000/articles?start=${startDate}&end=${endDate}`;
                const res = await fetch(topicUrl);

                if(!res.ok) throw new Error("Topic Error");

                const topicJson = await res.json();
                const stockTopics = topicJson.stock.slice(0, 10);

                setStockTopicData(stockTopics);
            } catch (err) {
                console.error(err);
            }
        };

        fetchTopics();
    }, [startDate, endDate]);

    useEffect(() => {
        if(graphType === "stock" && stockTopicData.length > 0) {
            setSelectedKeyword(stockTopicData[0].representative_keyword);
            setSelectedClusterId(stockTopicData[0].cluster_id)
        }
    }, [stockTopicData, graphType]);

    useEffect(() => {
        if (!selectedKeyword || !startDate || !endDate) return;

        const fetchAll = async() => {
            try {
                setLoading(true);
                console.log(selectedKeyword)

                const trendUrl = `http://127.0.0.1:8000/trend?start=${startDate}&end=${endDate}&keyword=${encodeURIComponent(selectedKeyword)}`;
                const matchedTopic = stockTopicData.find(
                    t => t.representative_keyword === selectedKeyword
                );
                const item_code = matchedTopic?.item_code || "";
                const priceUrl = `http://127.0.0.1:8000/stock?start=${startDate}&end=${endDate}&item_code=${item_code}`;

                const [trendRes, priceRes] = await Promise.all([
                    fetch(trendUrl),
                    fetch(priceUrl),
                ])

                if (!trendRes.ok || !priceRes.ok) {
                    throw new Error("API Error");
                }

                const trendJson = await trendRes.json();
                const priceJson = await priceRes.json();

                const trendData = trendJson.data;
                const stockData = priceJson.data;

                const mergedData = mergeWith(trendData, stockData);
                setData(mergedData);

            } catch (err) {
                console.error(err);
                setWarning("Data Error");
            } finally {
                setLoading(false);
            }
        };

        fetchAll();
    }, [selectedKeyword, startDate, endDate, graphType, stockTopicData]);

    return (
        <div>
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
                            loading={loading}
                            stockTopicData={stockTopicData}
                            selectedClusterId={selectedClusterId}
                            setSelectedClusterId={setSelectedClusterId}
                        />
                    }
                />
            </Routes>
        </div>
    );
}

function mergeWith(trendData, stockData) {
    const stockMap = new Map(stockData.map(s => [
        s.date,
        {
            price: s.price,
            vol: s.vol,
            hgpr: s.hgpr,
            lwpr: s.lwpr,
            sign: s.sign
        }
        ]));
    let last = {
        price: null,
        vol: null,
        hgpr: null,
        lwpr: null,
        sign: null
    };

    return trendData.map(t => {
        const date = t.date;

        const day = new Date(date).getDay();
        const isWeekend = (day === 0 || day === 6);
        const hasDate = stockMap.has(date);
        if(hasDate) {
            last = stockMap.get(date);
        }

        return {
            date,
            value: t.value,
            price: last.price,
            vol: (isWeekend || !hasDate) ? 0 : last.vol,
            hgpr: last.hgpr,
            lwpr: last.lwpr,
            sign: last.sign
        }
    })
}

export default App;