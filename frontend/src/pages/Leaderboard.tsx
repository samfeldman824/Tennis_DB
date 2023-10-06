import { useState, useEffect } from "react"
import LeaderboardBox from "../components/LeaderboardBox";
import '../styles.css'

export default function Leaderboard() {


    
        
    



    return (
        
        
        <div id="leaderboard"> 
            <h2>Leaderboard</h2>
            <div className="leaderboard-container">
                <LeaderboardBox title="Wins" apiUrl="players/stats/wins" />
                <LeaderboardBox title="Sets Won" apiUrl="players/stats/sets" />
                <LeaderboardBox title="1st Serve Points Won %" apiUrl="players/stats/fspw" />
            </div>
        </div>
    )
}