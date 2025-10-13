import {LineChart, XAxis, YAxis, Tooltip, Line, ResponsiveContainer, CartesianGrid, Legend} from 'recharts';

function Graph({ data }) {
    if(!data || data.length == 0) {
        return <p>No Data</p>;
    }

    console.log(data);

    return (
        <div className="graph">
            <h2>Graph</h2>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3"/>
                    <XAxis dataKey="date"/>
                    <YAxis/>
                    <Tooltip/>
                    <Legend/>
                    <Line
                        type="monotone"
                        dataKey="value"
                        stroke="#2563eb"
                        strokeWidth={2}
                        activeDot={{ r: 6}}
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}

export default Graph;