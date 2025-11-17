import React from "react";
import "./NewsToggleSwitch.css"

function NewsToggleSwitch({newsType, onToggle}) {
    return (
        <div className="news-toggle-switch">
            <input
                type="checkbox"
                id="news-toggle"
                className="news-toggle-input"
                checked={newsType === "news"}
                onChange={(e) => onToggle(e.target.checked ? "news" : "graph")}
            />
            <label htmlFor="news-toggle" className="news-toggle-label">
                <span className="news-toggle-inner"/>
                <span className="news-toggle-switcher"/>
            </label>
        </div>
    );
}

export default NewsToggleSwitch;