import {use, useEffect, useState} from 'react'
import Date from "./components/Date.jsx"
import Graph from "./components/Graph.jsx"
import dayjs from "dayjs"

function App() {
    const [data, setData] = useState([]);
    const [warning, setWarning] = useState("");

    const handle_dates_change = async ({ start_date, end_date }) => {
        if (!(start_date && end_date)) return;
        if (dayjs(end_date).isAfter(dayjs())) {
            setWarning("타임머신을 타고 오셨나요?");
            setData([]);
            return;
        }

        setWarning("");

        try {
            const response = await fetch(`/data?start=${start_date}&end=${end_date}`);
            const json = await response.json();
            setData(json.data);
        } catch (error) {
            setDate([]);
            setWarning("데이터를 가져오는 중 오류 발생.");
        }
    };

    return (
        <div>
            <h1>데이터 시각화</h1>
            <Date onDateChange={handle_dates_change} />
            {warning ? <p>{warning}</p> : <Graph data={data} />}
        </div>
    );
}

export default App;