import React from 'react';


export default function SongList({songs}){
    if(!songs || songs.length===0) return <p>No songs yet — click Get Songs.</p>
    return (
        <ol>
            {songs.map((s,i)=> (
                <li key={s.id || i} style={{marginBottom:8}}>
                    <a href={s.spotify_url} target="_blank" rel="noreferrer">{s.name}</a>
                    <div style={{fontSize:12,color:'#555'}}>{(s.artists||[]).join(', ')} • popularity: {s.popularity}</div>
                </li>
            ))}
        </ol>
    )
}