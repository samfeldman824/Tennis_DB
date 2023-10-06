import { useState, useEffect } from "react";



interface LeaderboardData {
    Name: string;
    Wins: number;
}

interface LeaderboardBoxProps {
    title: string;
    apiUrl: string
}




export default function LeaderboardBox({title, apiUrl}: LeaderboardBoxProps) {
    
    const [data, setData] = useState<LeaderboardData[]>([])


    useEffect(() => {

        const getData = async () => {
        const url = 'http://localhost:8080/' + apiUrl
        const data = await fetch(url)
        const json = await data.json()
        console.log(json.data)
        setData(json.data)
        
        };

        getData();
    }, [])

    
    
    return (
        <div className="leaderboard-box">
            <div>
                <p>{title}</p>
            </div>
    
            <table>
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Name</th>
                        <th>{title}</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index}>
                            <td>{index + 1}</td>
                            <td>{Object.values(item)[0]}</td>
                            <td>{Object.values(item)[1]}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )

}