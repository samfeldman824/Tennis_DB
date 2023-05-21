import '../styles.css'
import { useState, useEffect } from 'react';
import { DropzoneBox } from '../components/Dropzone';
import DragDrop from '../components/DragDrop';


export default function Home() {
    const [addPlayerInputText, setAddPlayerInputText] = useState('');
    const [addPlayerMessage, setAddPlayerMessage] = useState('')
    const [deletePlayerInputText, setDeletePlayerInputText] = useState('');
    const [deletePlayerMessage, setDeletePlayerMessage] = useState('');
    
    
    const [formData, setFormData] = useState({name: 'name'});

    const handleAddPlayer = async () => {
        const url = 'http://localhost:8080/players/create_player/' + encodeURIComponent(addPlayerInputText)
        const options_post = { method: 'POST', headers: {'Content-Type': 'application/json'}}
        const data = await fetch(url, options_post);
        const json = await data.json();
        setAddPlayerMessage(json.message)
    }
    // const handleAddPlayer = async () => {
    //     const data1 = { key1: 'value1', key2: 'value2', key3: 'value3' };
    //     const blob = new Blob([JSON.stringify(data1)], { type: 'application/json' });
    //     // console.log(blob)
    //     const form = new FormData();
    //     // form.append('name', blob)
    //     form.append('test', '123')
    //     console.log(form)
        
    //     const url = 'http://localhost:8080/upload'
    //     const options_post = { method: 'POST', body: form}
    //     const data = await fetch(url, options_post);
    //     const json = await data.json()
    //     console.log(json.message.name)


    // }

    const handleDeletePlayer = async () => {
        const url = 'http://localhost:8080/players/delete/name/' + encodeURIComponent(deletePlayerInputText)
        const options_delete = { method: 'DELETE', headers: {'Content-Type': 'application/json'}}
        const data = await fetch(url, options_delete);
        const json = await data.json();
        setDeletePlayerMessage(json.message)
    }

    const handleKeyDownAdd = (event: { keyCode: number; }) => {
        if (event.keyCode === 13) { // return key
          handleAddPlayer();
        }
      };

      const handleKeyDownDelete = (event: { keyCode: number; }) => {
        if (event.keyCode === 13) { // return key
          handleDeletePlayer();
        }
      };

    const clearAddPlayerInput = () => {
        setAddPlayerInputText('');
        setAddPlayerMessage('');
    }

    const clearDeletePlayerInput = () => {
        setDeletePlayerInputText('');
        setDeletePlayerMessage('');
    }

    return (
        <div className='home'>
        <div className="home-title">
            <h1>Welcome to my Tennis Database</h1>
        </div>
        <div className='container'>
            <div>
                {/* <p>Add Match from CSV</p>
                <div>
                    <input 
                    id='csv-file'
                    type='file'
                    >

                    </input>
                </div> */}
                <DragDrop />
                {/* <DropzoneBox /> */}
            </div>
            <div>
                <p>Add Player</p>
                <input
                id='input-add-player'
                type='text'
                value={addPlayerInputText}
                onChange={(e) => setAddPlayerInputText(e.target.value)}
                onKeyDown={handleKeyDownAdd}
                ></input>
                <button
                onClick={handleAddPlayer}
                >Add</button>
                <button onClick={clearAddPlayerInput}>Clear</button>
                <p>{addPlayerMessage}</p>
            </div>
            <div>
                <p>Delete Player</p>
                <input
                id='input-delete-player'
                type='text'
                value={deletePlayerInputText}
                onChange={(e) => setDeletePlayerInputText(e.target.value)}
                onKeyDown={handleKeyDownDelete}></input>
                <button onClick={handleDeletePlayer}>Delete</button>
                <button onClick={clearDeletePlayerInput}>Clear</button>
                <p>{deletePlayerMessage}</p>

            </div>
            
        </div>
            
        </div>
        )
}