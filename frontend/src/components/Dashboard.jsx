import "./Dashboard.css"
import NewsToggleSwitch from "./NewsToggleSwitch";

function Dashboard({
                       onKeywordSelect,
                       selectedKeyword,
                       graphType,
                       newsType,
                       handleSubjectToggle,
                       handleNewsToggle,
                       stockTopicData,
                       onTopicSelect
}) {
    const topicsToRender = stockTopicData;

    return (
        <div className="dashboard-container">
            <div className="dashboard-top-area">
                <NewsToggleSwitch newsType={newsType} onToggle={handleNewsToggle}/>
            </div>

            <div className="dashboard-middle-area">
                <div className="dashboard-list">
                {topicsToRender.map((topic) => (
                    <button
                        key={topic.topic}
                        onClick={() => {
                            onKeywordSelect(topic.representative_keyword);
                            onTopicSelect(topic.cluster_id);
                        }}
                        className={`dashboard-button ${
                            selectedKeyword === topic.topic ? "active" : ""
                        }`}
                    >
                        {topic.topic}
                    </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;