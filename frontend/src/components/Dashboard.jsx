const keywordsList1 = ["딱다구리", "삼성전자", "LG전자", "네이버", "카카오", "현대차", "기아", "SK하이닉스", "셀트리온", "넷마블"];
const keywordsList2 = ["쏙독새", "참새", "왜가리", "참수리", "수리부엉이", "매", "비둘기", "오리", "방울새", "꿩"];
export let keywordsList = [];

function Dashboard({onKeywordSelect, selectedKeyword, graphType}) {
    if (graphType === "stock") keywordsList = keywordsList1;
    else keywordsList = keywordsList2;
    return (
        <div style = {{ display: "flex", gap: "20px"}}>
            <div style={{ display: "flex", flexDirection: "column", gap: "8px"}}>
            {keywordsList.map((word) => (
                <button
                    key={word}
                    onClick={() => onKeywordSelect(word)}
                    style={{
                        padding: "8px 12px",
                        borderRadius: "4px",
                        border: selectedKeyword === word ? "2px solid blue" : "1px solid gray",
                        background: selectedKeyword === word ? "#d0e7ff" : "#fff",
                        cursor: "pointer",
                    }}
                >
                    {word}
                </button>
                ))}
            </div>
        </div>
    );
}

export default Dashboard;