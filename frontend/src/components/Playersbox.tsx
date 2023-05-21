import { useState, useEffect } from "react";
import '../styles.css'

interface PlayersData {
    Name: string;
}

export default function PlayersBox() {
    const [data, setData] = useState<PlayersData[]>([])

    useEffect(() => {

        const getData = async () => {
        const url = 'http://localhost:8080/players'
        const data = await fetch(url)
        const json = await data.json()
        // console.log(json.players)
        setData(json.players)
        
        };

        getData();
    }, [])

    // console.log(data)
    return (

        <div className="scrollable-div">
            {data && data.map((item, index) => (
                    <div key={index}>
                        <div>{item.Name}</div>
                    </div>
                ))

                }
        </div>
    )
}