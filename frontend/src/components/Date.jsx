import { useState, useEffect } from "react";
import { FaRegCalendarAlt } from "react-icons/fa";
import ReactDatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./Date.css";

function Date({ onDateChange }) {
    const [start_date, setStart_date] = useState("");
    const [end_date, setEnd_date] = useState("");

    useEffect(() => {
        if (start_date && end_date) {
            onDateChange({start_date: start_date.toISOString().split("T")[0], end_date: end_date.toISOString().split("T")[0]});
        }
    }, [start_date, end_date, onDateChange]);


    return (
        <div className="date-picker-container">
            <div className="date-picker-item">
                <label htmlFor="start-date">Start Date:</label>
                <div className="date-input-wrapper">
                    <ReactDatePicker
                        selected={start_date}
                        onChange={(date) => setStart_date(date)}
                        dateFormat="yyyy-MM-dd"
                        placeholderText="Select start date"
                        className="custom-datepicker"
                        popperPlacement="bottom-start"
                    />
                    <FaRegCalendarAlt className="calendar-icon"/>
                </div>
            </div>

            <div className="date-picker-item">
                <label htmlFor="end-date">End Date:</label>
                <div className="date-input-wrapper">
                    <ReactDatePicker
                        selected={end_date}
                        onChange={(date) => setEnd_date(date)}
                        dateFormat="yyyy-MM-dd"
                        placeholderText="Select start date"
                        className="custom-datepicker"
                        popperPlacement="bottom-start"
                    />
                    <FaRegCalendarAlt className="calendar-icon"/>
                </div>
            </div>
        </div>
    )
}

export default Date;