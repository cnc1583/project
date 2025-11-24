import Date from "../components/Date.jsx";
import Graph from "../components/Graph.jsx";
import Dashboard from "../components/Dashboard";
import NEWS_DATA from "../components/News";
import LoadingSpinner from "../components/LoadingSpinner";

import "./HomePage.css"
import {useState, useRef} from "react";

export default function HomePage({
    selectedKeyword,
    setSelectedKeyword,
    data,
    warning,
    startDate,
    endDate,
    graphType,
    newsType,
    handle_dates_change,
    handleSubjectToggle,
    handleNewsToggle,
    loading
}) {

    return (
        <div>
            <div className="home-layout">

                <div className="home-sidebar">
                    <Dashboard
                        selectedKeyword={selectedKeyword}
                        onKeywordSelect={setSelectedKeyword}
                        graphType={graphType}
                        newsType={newsType}
                        handleSubjectToggle={handleSubjectToggle}
                        handleNewsToggle={handleNewsToggle}
                    />
                </div>

                <div className="home-content">
                    <div className="homepage-header">
                        <h1 className="homepage-title">CSE 9</h1>
                        <Date onDateChange={handle_dates_change} />
                    </div>

                    {loading ? (
                        <LoadingSpinner height={graphType === "stock" ? 660 : 660}/>
                    ) : newsType === "news" ?
                    (
                    <div className="news-section">
                        <h2>관련 뉴스</h2>
                            <div className="news-cards">
                                {NEWS_DATA.filter(n =>
                                    n.date >= startDate &&
                                    n.date <= endDate &&
                                    n.subject === graphType).map((n, idx) => (
                                        <NewsCard key={idx} news={n}/>
                                ))}
                            </div>
                    </div>
                    )
                    : warning ? <p>{warning}</p> :
                    (<Graph data={data} graphType={graphType} />)
                    }
                </div>
            </div>
        </div>
    );
}

function NewsCard({news}) {
    const [expanded, setExpanded] = useState(false);
    const contentRef = useRef(null);
    const previewLength = expanded ? 120 : 60;
    const isOverflow = news.content.length > previewLength;
    const displayText = news.content.slice(0, previewLength) + (isOverflow ? "..." : "")

    const toggleExpand = (e) => {
        e.stopPropagation();
        setExpanded(!expanded);
    }

    const handleCardClick = () => {
        window.open(news.url, "_blank");
    }

    return (
        <div className="news-card" onClick={handleCardClick}>
            <h3 className="news-card-title">{news.title}</h3>
            <p className="news-card-date">{news.date}</p>

            <div className={`news-card-content-wrapper ${expanded ? "expanded" : ""}`}
                 ref={contentRef}
            >
                <p className="news-card-content">
                    {displayText}
                </p>
            </div>
            {news.content.length > 60 && (
                <div className="news-card-footer">
                    <button className="news-card-toggle" onClick={toggleExpand}>{
                        expanded ? "접기 ▲" : "더보기 ▼"}
                    </button>
                </div>
            )}
        </div>
    )
}