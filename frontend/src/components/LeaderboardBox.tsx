import { useState, useEffect } from "react";



interface LeaderboardData {
    Name: string;
    Wins: number;
}





export default function LeaderboardBox() {
    
    const [data, setData] = useState<LeaderboardData[]>([])


    useEffect(() => {

        const getData = async () => {
        const url = 'http://localhost:8080/players/stats/wins'
        const data = await fetch(url)
        const json = await data.json()
        console.log(json.data)
        setData(json.data)
        
        };

        getData();
    }, [])

    
    
    return (
        <div>
            <p>Wins</p>
            {data && data.map((item, index) => (
                    <div key={index} style={{display: "flex", gap: "1rem"}}>
                        <div>{item.Name}</div>
                        <div>{item.Wins}</div>
                    </div>
                ))

                }
        </div>
        
    )

}