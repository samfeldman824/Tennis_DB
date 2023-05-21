import '../styles.css'
import PlayersBox from '../components/Playersbox'
import { useState, useEffect } from 'react';

interface Match {
    _id: string;
    Winner: string;
    Loser: string;
    'Number of Sets': number;
    'Set Scores': number[];
  }

  function Match({ match }: { match: Match }) {
    return (
      <div>
        <h2>Match Info</h2>
        <p>Winner: {match.Winner}</p>
        <p>Loser: {match.Loser}</p>
        <p>Number of Sets: {match['Number of Sets']}</p>
        <p>Set Scores: {match['Set Scores'].join(', ')}</p>
      </div>
    );
  }

    



export default function Players() {
    const [searchText, setSearchText] = useState('')
    const [playerMatches, setPlayerMatches] = useState<Match[]>([])

    const handleSearch = async () => {
        const url = 'http://localhost:8080/players/matches/' + encodeURIComponent(searchText)
        const data = await fetch(url);
        const json = await data.json();
        setPlayerMatches(json.matches)
    }

    const clearStates = () => {
        setSearchText("");
        setPlayerMatches([]);
    }

    const handleKeyDown = (event: { keyCode: number; }) => {
        if (event.keyCode === 13) { // return key
          handleSearch();
        }
      };


    return (
        <div className="players">


            <h2>Players</h2>


            <p>Search Players</p>

            <input
            id='text'
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            onKeyDown={handleKeyDown}
            ></input>

            <button
            onClick={handleSearch}
            >Search</button>

            <button
            onClick={clearStates}>Clear Matches</button>


            <div className='scrollable-div'>
            {playerMatches ? (<div>
          {playerMatches.map((match) => (
            <Match key={match._id} match={match} />
          ))}
        </div>) : <p></p>}
            </div>
            

            <div className='playersbox'>
                
                <PlayersBox />
                </div>
            
        </div>
    
    )
}

