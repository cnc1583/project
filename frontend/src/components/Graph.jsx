import {ResponsiveContainer, Bar, XAxis, YAxis, Tooltip, Legend, ComposedChart, Line} from 'recharts';

function Graph({ data, graphType: graphType }) {
    if(!data || data.length === 0) {
        return <p>No Data</p>;
    }

    console.log(data);

    let yAxisLabel = (graphType === "stock") ? "주가" : "평당 가격";

    return (
        <div className="graph" style={{ margin: '100px'}}>
            <h2>Graph</h2>
            <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={data}>
                    <XAxis dataKey="date"/>
                    <YAxis
                        yAxisId="left"
                        label={{value: "검색량", angle:-90, position:"insideLeft"}}
                    />

                    <YAxis
                        yAxisId="right"
                        orientation="right"
                        label={{value: yAxisLabel, angle:90, position:"insideRight"}}
                    />
                    <Tooltip/>
                    <Legend/>
                    <Bar
                        yAsisId="left"
                        dataKey="value"
                        name="검색량"
                        fill="#2563eb"
                        barSize={20}
                    />

                    <Line
                        yAxisId="right"
                        type="monotone"
                        dataKey="price"
                        name={yAxisLabel}
                        stroke="#dc2626"
                        strokeWidth={2}
                        dot={false}
                    />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
    )
}

export default Graph;