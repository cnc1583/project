import { useState, useEffect } from "react";

function Date({ onDateChange }) {
    const [start_date, setStart_date] = useState("");
    const [end_date, setEnd_date] = useState("");

    useEffect(() => {
        if (start_date && end_date) {
            onDateChange({ start_date, end_date });
        }
    }, [start_date, end_date]);

    return (
        <div id="set_date">
            <label>
                start_date:{" "}
                <input
                    type="date"
                    value={start_date}
                    onChange={(e) => setStart_date(e.target.value)}
                />
            </label>
            <br></br>
            <label>
                end_date:{" "}
                <input
                    type="date"
                    value={end_date}
                    onChange={(e) => setEnd_date(e.target.value)}
                />
            </label>
        </div>
    )
}

export default Date;