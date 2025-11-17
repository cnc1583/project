import Date from "../components/Date.jsx";
import Graph from "../components/Graph.jsx";
import Dashboard, {keywordsList} from "../components/Dashboard";
import NEWS_DATA from "../components/News";
import SubjectToggleSwitch from "../components/SubjectToggleSwitch";
import NewsToggleSwitch from "../components/NewsToggleSwitch";

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
    handleNewsToggle
}) {

    return (
        <div>
            <h1>데이터 시각화</h1>

            <Date onDateChange={handle_dates_change} />

            <SubjectToggleSwitch graphType={graphType} onToggle={handleSubjectToggle}/>

            <NewsToggleSwitch newsType={newsType} onToggle={handleNewsToggle}/>

            {newsType === "news" ?
            (
            <div>
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

            <Dashboard
                selectedKeyword={selectedKeyword}
                onKeywordSelect={setSelectedKeyword}
                graphType={graphType}
            />

        </div>
    );
}