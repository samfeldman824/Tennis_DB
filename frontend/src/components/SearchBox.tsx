import React from 'react';
import { useState, useEffect } from 'react';


interface Match {
  _id: string;
  Winner: string;
  Loser: string;
  'Number of Sets': number;
  'Set Scores': number[];
}

interface Player {
    Name: string;
    Wins: number;
    Losses: number;
}

function Player({ player}: { player: Player}) {
    return (
        <div>
            <h4>Name: {player.Name}</h4>
            <p>Wins: {player.Wins}</p>
            <p>Losses: {player.Losses}</p>
        </div>
    )
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

export default function SearchBox() {

  const [InputText, setInputText] = useState('');
  const [matches, setMatches] = useState<Match[]>([]);
  const [players, setPlayers] = useState<Player[]>([])
  const [selectedOption, setSelectedOption] = useState('');
  const [selectedOptionLabel, setSelectedOptionLabel] = useState('');
  const [outMessage, setOutMessage] = useState('');
  // const [formData, setFormData] = useState(null);

  useEffect(() => {
    console.log('test')
  });

  async function postData() {
    const postData = {
      Name: "Joe"
    };
}
  

  const options = [
    { value: 'http://localhost:8080/players', label: 'View All Players'}, // works
    { value: 'http://localhost:8080/players/matches/', label: 'Search Player Matches' }, // works
    { value: 'http://localhost:8080/players/create_player/', label: 'Add Player' }, // works
    { value: 'http://localhost:8080/matches/add_csv/', label: 'Add Match from CSV'},
    { value: 'http://localhost:8080/players/update/name/', label: 'Update Name'},
    { value: 'http://localhost:8080/players/delete/name/', label: 'Delete Player (Name)'}, // works
    
  ];
    
  const handleClick = async () => {
    const url = selectedOption + encodeURIComponent(InputText)
    const options_post = { method: 'POST',
    headers: {
      'Content-Type': 'application/json'}}
    console.log({url});
    const options_delete = { method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'}}
      const options_patch = { method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'}}

    if (selectedOptionLabel === "View All Players") {
        const data = await fetch(selectedOption);
        const json = await data.json();
        setOutMessage(json.message)
        setPlayers(json.players)
        console.log(json.players)
    }

    if (selectedOptionLabel === "Add Player") {
        const data = await fetch(url, options_post);
        const json = await data.json();
        setOutMessage(json.message)
        console.log(json)
    }

    if (selectedOptionLabel === "Search Player Matches") {
        const data = await fetch(url);   
        const json = await data.json();
        console.log(json)
        setOutMessage(json.message)
        try {
            setMatches(json.matches)
        } catch (error) {
            setMatches([])
        }
        
    }

    if (selectedOptionLabel === "Add Match from CSV") {
        console.log('CSV match should be added')
    }

    if (selectedOptionLabel === "Update Name") {
        const data = await fetch(url, {method: 'POST', headers: {
            'Content-Type': 'application/json',
          }, body: JSON.stringify(postData)})
        const json = await data.json()
        console.log(json.message)
    }

    if (selectedOptionLabel === "Delete Player (Name)") {
        const data = await fetch(url, options_delete);
        const json = await data.json();
        setOutMessage(json.message)
    }



  };

  const handleKeyDown = (event: { keyCode: number; }) => {
    if (event.keyCode === 13) { // return key
      handleClick();
    }
  };

  const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedOption(event.target.value);
    setSelectedOptionLabel(event.target.options[event.target.selectedIndex].label)
  };

  return (
    <div>
    <label> Type something</label>
    <input
        id='input-box'
        type='text'
        value={InputText}
        onChange={(e) => setInputText(e.target.value)}
        onKeyDown={handleKeyDown}>

    </input>
    <select 
    id="select-box"
    value={selectedOption}
    onChange={handleSelectChange}
    >
    {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
    

    </select>
    <button onClick={handleClick} onKeyDown={handleKeyDown}>
      Enter
    </button>
    <button onClick={() => {setMatches([]); setOutMessage(''); setPlayers([])}}>Clear</button>
    {outMessage ? (<p>{outMessage}</p>) : <p></p>}
    {matches ? (<div>
          {matches.map((match) => (
            <Match key={match._id} match={match} />
          ))}
        </div>) : <p></p>}
    {players ? (<div>
          {players.map((player) => (
            <Player key={player.Name} player={player} />
          ))}
        </div>) : <p>WORKING</p>}
    
    
    </div>
  );
}
