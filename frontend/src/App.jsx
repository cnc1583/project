import {use, useEffect, useState} from 'react'
import Date from "./components/Date.jsx"
import Graph from "./components/Graph.jsx"

function App() {
    const [data, setData] = useState([]);
    const handle_dates_change = async ({ start_date, end_date }) => {
        if (!(start_date && end_date)) return;

        try {
            const response = await fetch(`/data?start=${start_date}&end=${end_date}`);
            console.log("type:", response.headers.get("content-type"));
            const json = await response.json();
            setData(json.data);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h1>데이터 시각화</h1>
            <Date onDateChange={handle_dates_change} />
            <Graph data={data} />
        </div>
    );
}

export default App;