import {use, useEffect, useState} from 'react'

function App() {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [result, setResult] = useState("");

    useEffect(()=> {
        if (startDate && endDate) {
            const fetchDate = async () => {
                try {
                    const response = await fetch("http://127.0.0.1:8000/date", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ start_date: startDate, end_date: endDate }),
                    });

                    const data = await response.json();
                    setResult(data.result);
                } catch (error) {
                    console.log("서버 요청 오류", error);
                    setResult("서버 요청 중 오류 발생");
                }
            };

            fetchDate();
        }
    }, [startDate, endDate]);

    return (
        <div style={{ padding: "10px" }}>
            <h1>날짜 선택</h1>

            <div style={{ marginBottom: "10px"}}>
                <label>start: </label>
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
            </div>

            <div style={{ marginBottom: "10px" }}>
                <label>end: </label>
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>

            {result && (
                <div style={{ marginTop: "10px" }}>
                    <h3>result:</h3>
                    <p>{result}</p>
                </div>
            )}
        </div>
    )
}

export default App;
