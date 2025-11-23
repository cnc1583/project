import "./Dashboard.css"
import SubjectToggleSwitch from "./SubjectToggleSwitch";
import NewsToggleSwitch from "./NewsToggleSwitch";

const keywordsList1 = ["딱다구리", "삼성전자", "LG전자", "네이버", "카카오", "현대차", "기아", "SK하이닉스", "셀트리온", "넷마블"];
const keywordsList2 = ["쏙독새", "참새", "왜가리", "참수리", "수리부엉이", "매", "비둘기", "오리", "방울새", "꿩"];
export let keywordsList = [];

function Dashboard({
                       onKeywordSelect,
                       selectedKeyword,
                       graphType,
                       newsType,
                       handleSubjectToggle,
                       handleNewsToggle
}) {
    if (graphType === "stock") keywordsList = keywordsList1;
    else keywordsList = keywordsList2;
    return (
        <div className="dashboard-container">
            <div className="dashboard-top-area">
                <SubjectToggleSwitch graphType={graphType} onToggle={handleSubjectToggle}/>
                <NewsToggleSwitch newsType={newsType} onToggle={handleNewsToggle}/>
            </div>

            <div className="dashboard-middle-area">
                <div className="dashboard-list">
                {keywordsList.map((word) => (
                    <button
                        key={word}
                        onClick={() => onKeywordSelect(word)}
                        className={`dashboard-button ${
                            selectedKeyword === word ? "active" : ""
                        }`}
                    >
                        {word}
                    </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;