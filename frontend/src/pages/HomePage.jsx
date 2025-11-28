import Date from "../components/Date.jsx";
import Graph from "../components/Graph.jsx";
import Dashboard from "../components/Dashboard";
import NEWS_DATA from "../components/News";
import LoadingSpinner from "../components/LoadingSpinner";

import "./HomePage.css"

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
                        <ul>
                            {NEWS_DATA.filter(n =>
                                n.date >= startDate &&
                                n.date <= endDate &&
                                n.subject === graphType).map((n, idx) => (
                                    <li key={idx}>
                                        <a href={n.url} target="_blank" rel="noreferrer">{n.title}</a>
                                    </li>
                            ))}
                        </ul>
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