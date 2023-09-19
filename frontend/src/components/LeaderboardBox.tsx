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
            <p>{title}</p>
            {data && data.map((item, index) => (
                    <div key={index} style={{display: "flex", gap: "1rem"}}>
                         <p>{Object.values(item)[0]}</p>
                        <p>{Object.values(item)[1]}</p>
                    </div>
                ))

                }
        </div>
        
    )

}