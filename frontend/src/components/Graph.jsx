import {ResponsiveContainer, Bar, XAxis, YAxis, Tooltip, Legend, BarChart, Cell, CartesianGrid} from 'recharts';

function Graph({ data, graphType, selectedKeyword }) {
    if(!data || data.length === 0) {
        return <p>No Data</p>;
    }

    let isStock = graphType === "stock";

    return (
        <div className="graph">
            <h2>{selectedKeyword}</h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} syncId="synced">
                    <CartesianGrid strokeDasharray="2 2"/>
                    <XAxis dataKey="date"/>
                    <YAxis domain={[
                        (dataMin) => dataMin * 0.95,
                        (dataMax) => dataMax * 1.05]}
                           tickFormatter={v => Number(v.toFixed(2))}
                    />

                   <Tooltip/>
                    <Legend/>
                    <Bar
                        dataKey={(data) => {
                            const range = [data.lwpr, data.hgpr]
                            return range
                        }}
                        name="주가"
                        barSize={20}
                        fill="#E64560"
                    >
                        {data.map((data) => (
                            <Cell fill={(data.sign > 3) ? "#006DEE" : "#E94560"}/>
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>

            <ResponsiveContainer width="100%" height={180}>
                <BarChart data={data} syncId="synced">
                    <CartesianGrid strokeDasharray="2 2"/>
                    <XAxis dataKey="date"/>
                    <YAxis />
                    <Tooltip/>
                    <Legend/>
                    <Bar
                        dataKey="value"
                        name="검색량"
                        barSize={20}
                        fill="#2563eb"/>
                </BarChart>
            </ResponsiveContainer>

            {isStock && (
                <ResponsiveContainer width="100%" height={180}>
                    <BarChart data={data} syncId="synced">
                        <CartesianGrid strokeDasharray="2 2"/>
                        <XAxis dataKey="date"/>
                        <YAxis tickFormatter={(value) => (value / 1000000).toFixed(0) + "M"}/>
                        <Tooltip/>
                        <Legend/>
                        <Bar
                            dataKey="vol"
                            name="거래량"
                            barSize={20}
                            fill="#2331de"/>
                    </BarChart>
                </ResponsiveContainer>
            )}
        </div>
    )
}

export default Graph;