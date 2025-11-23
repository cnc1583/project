import {ResponsiveContainer, Bar, XAxis, YAxis, Tooltip, Legend, BarChart, Cell, CartesianGrid, Line} from 'recharts';

function Graph({ data, graphType }) {
    if(!data || data.length === 0) {
        return <p>No Data</p>;
    }

    console.log(data);

    let isStock = graphType === "stock";

    return (
        <div className="graph">
            <h2>Graph</h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} syncId="synced">
                    <CartesianGrid strokeDasharray="2 2"/>
                    <XAxis dataKey="date"/>

                    {isStock ? (
                         <YAxis domain={[
                        (dataMin) => dataMin * 0.95,
                        (dataMax) => dataMax * 1.05]}/>
                    ) : (
                        <YAxis domain={[
                            'dataMin', 'dataMax'
                        ]}/>
                    )}

                   <Tooltip/>
                    <Legend/>

                    {isStock ? (
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
                    ) : (
                        <Line dataKey="price" name="평당 가격" barSize={20} fill="#E64560"/>
                    )}
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