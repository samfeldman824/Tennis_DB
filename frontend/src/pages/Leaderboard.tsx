import { useState, useEffect } from "react"
import LeaderboardBox from "../components/LeaderboardBox";
import '../styles.css'

export default function Leaderboard() {


    
        
    



    return (
        
        
        <div className="leaderboard"> 
            <h2 className="leaderboard-title">Leaderboard</h2>
            <div className="leaderboard-body">
                <LeaderboardBox title="Wins" apiUrl="players/stats/wins" />
                <LeaderboardBox title="Sets Won" apiUrl="players/stats/sets" />
                <LeaderboardBox title="1st Serve Points Won %" apiUrl="players/stats/fspw" />
            </div>
        </div>
    )
}