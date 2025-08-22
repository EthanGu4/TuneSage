import React, { useState } from 'react';
import SongList from './components/SongList';


export default function App(){
    const [genre, setGenre] = useState('');
    const [timePeriod, setTimePeriod] = useState('');
    const [songs, setSongs] = useState([]);
    const [loading, setLoading] = useState(false);


    async function fetchSongs(e){
        e && e.preventDefault();
        setLoading(true);
        const params = new URLSearchParams();
        if(genre) params.append('genre', genre);
        if(timePeriod) params.append('time_period', timePeriod);
        params.append('count', '10');


        const res = await fetch(`http://127.0.0.1:8000/songs?${params.toString()}`);
        const data = await res.json();
        setSongs(data.results || []);
        setLoading(false);
    }


    return (
        <div style={{padding:20,fontFamily:'sans-serif'}}>
            <h1>🎶 TuneSage 🎶</h1>
            <form onSubmit={fetchSongs} style={{marginBottom:12}}>
                <input placeholder="Genre (optional)" value={genre} onChange={e=>setGenre(e.target.value)} />
                <input placeholder="Time period (optional, e.g. 1990s or 2000-2010)" value={timePeriod} onChange={e=>setTimePeriod(e.target.value)} style={{marginLeft:8}}/>
                <button type="submit" style={{marginLeft:8}}>Get Songs</button>
                <button type="button" onClick={()=>{setGenre(''); setTimePeriod(''); fetchSongs();}} style={{marginLeft:8}}>Surprise Me</button>
            </form>


            {loading ? <p>Loading…</p> : <SongList songs={songs} />}
        </div>
    );
}