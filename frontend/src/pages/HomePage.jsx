import Date from "../components/Date.jsx";
import Graph from "../components/Graph.jsx";
import Dashboard from "../components/Dashboard";
import LoadingSpinner from "../components/LoadingSpinner";
import {useEffect, useState} from "react";
import dayjs from "dayjs";
import isSameOrAfter from "dayjs/plugin/isSameOrAfter";
import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
import "./HomePage.css"

dayjs.extend(isSameOrAfter);
dayjs.extend(isSameOrBefore);


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
    loading,
    stockTopicData,
    selectedClusterId,
    setSelectedClusterId
}) {
    const [topicNews, setTopicNews] = useState([]);

    useEffect(() => {
        if(!selectedKeyword) return;

        const fetchNews = async() => {
            try {
                const newsUrl = `http://127.0.0.1:8000/news/${selectedClusterId}`;
                const res = await fetch(newsUrl);

                if(!res.ok) throw new Error("News Error");

                const json = await res.json();
                setTopicNews(json.data);
                console.log(json.data);

            } catch (err) {
                console.log(err);
            }
        }

        fetchNews();
    }, [selectedKeyword, selectedClusterId]);

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
                        stockTopicData={stockTopicData}
                        onTopicSelect={setSelectedClusterId}
                    />
                </div>

                <div className="home-content">
                    <div className="homepage-header">
                        <h1 className="homepage-title">CSE 9</h1>
                        <Date onDateChange={handle_dates_change} />
                    </div>

                    {loading ? (
                        <LoadingSpinner height={660}/>
                    ) : newsType === "news" ?
                    (
                    <div className="news-section">
                        <h2>{selectedKeyword}</h2>
                        <ul>
                            {topicNews.map((n, idx) => (
                                    <li key={idx} className="news-card">
                                        <div className="date">{n.article_date}</div>
                                        <h3>{n.title}</h3>
                                        <p>{n.content}</p>
                                        <a href={n.url} target="_blank" rel="noreferrer">Read more</a>
                                    </li>
                            ))}
                        </ul>
                    </div>
                    )
                    : warning ? <p>{warning}</p> :
                    (<Graph data={data} graphType={graphType} selectedKeyword={selectedKeyword} />)
                    }
                </div>
            </div>
        </div>
    );
}