import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css'; 
import logo from "./favicon.ico"
import Sliding_menu from "./sliding_menu";
import DreamEleven from "./DreamEleven";

function App() {
  // constant for each position
  const [gk, set_gk] = useState([]);
  const [def, set_def] = useState([]);
  const [mid, set_mid] = useState([]);
  const [fwd, set_fwd] = useState([]);

  // fetch data for each position
  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/players/goalkeepers")
      .then(response => set_gk(response.data))
      .catch(error => console.error("Error while fetching goalkeepers: ", error))
    axios.get("http://127.0.0.1:5000/api/players/defenders")
      .then(response => set_def(response.data))
      .catch(error => console.error("Error while fetching defenders: ", error))
    axios.get("http://127.0.0.1:5000/api/players/midfielders")
      .then(response => set_mid(response.data))
      .catch(error => console.error("Error while fetching midfielders: ", error))
    axios.get("http://127.0.0.1:5000/api/players/forwards")
      .then(response => set_fwd(response.data))
      .catch(error => console.error("Error while fetching forwards: ", error))
  }, []);

  // sorting each position for its key value pair
  const sorted_gk = Object.entries(gk).sort(([, ratingA], [, ratingB]) => ratingB - ratingA);
  const sorted_def = Object.entries(def).sort(([, ratingA], [, ratingB]) => ratingB - ratingA);
  const sorted_mid = Object.entries(mid).sort(([, ratingA], [, ratingB]) => ratingB - ratingA);
  const sorted_fwd = Object.entries(fwd).sort(([, ratingA], [, ratingB]) => ratingB - ratingA);

  // the top players from each position given
  // gk = 1, def = 3, mid = 4, fwd = 3
  const goalkeeper = sorted_gk[0];
  const defenders = sorted_def.slice(0,3);
  const midfielders = sorted_mid.slice(0,4);
  const forwards = sorted_fwd.slice(0,3);
  const all_players = {goalkeeper: goalkeeper, defenders: defenders, midfielders: midfielders, forwards: forwards}
  
  // a function for rendering each position's own table
  const render_table = (players, title) => {
    return (
      <div className="table">
        <h2>{title}</h2>
        <table border="3">
        <thead>
            <tr>
              <th>Player</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {players.map(([name, rating], index) => (
              <tr key={index}>
                <td>{name}</td>
                <td>{rating}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="App">
      {/* top bar */}
      <header className="top-bar">
        <img src={logo} alt="Logo" className="logo"/>
        <h1 className="header">FPL Player Scores</h1>
      </header>

      <Sliding_menu />

      {/* rendering each table */}
      <div className="table-wrapper">
        <div className="table-container">
          <div className="table-modifier">
            <div className="table table-goalkeepers">
              {render_table(sorted_gk, "Goalkeepers")}
            </div>
            <div className="table table-defenders">
              {render_table(sorted_def, "Defenders")}
            </div>
            <div className="table table-midfielders">
              {render_table(sorted_mid, "Midfielders")}
            </div>
            <div className="table table-forwards">
              {render_table(sorted_fwd, "Forwards")}
            </div>
          </div>
        </div>
      </div>
      <DreamEleven players={all_players}/>
    </div>
  );
}

export default App;