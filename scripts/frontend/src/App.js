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
  const sorted_gk = Object.entries(gk).sort(([, playerA], [, playerB]) => playerB.rating - playerA.rating);
  const sorted_def = Object.entries(def).sort(([, playerA], [, playerB]) => playerB.rating - playerA.rating);
  const sorted_mid = Object.entries(mid).sort(([, playerA], [, playerB]) => playerB.rating - playerA.rating);
  const sorted_fwd = Object.entries(fwd).sort(([, playerA], [, playerB]) => playerB.rating - playerA.rating);  

  // the top players from each position given
  // gk = 1, def = 3, mid = 4, fwd = 3
  const goalkeeper = sorted_gk[0];
  const defenders = sorted_def.slice(0,3);
  const midfielders = sorted_mid.slice(0,4);
  const forwards = sorted_fwd.slice(0,3);
  const all_players = {goalkeeper: goalkeeper, defenders: defenders, midfielders: midfielders, forwards: forwards}
  
  const disableScrolling = () => {
    document.body.style.overflow = 'hidden'; 
  };

  const enableScrolling = () => {
    document.body.style.overflow = '';
  };

  document.querySelectorAll('.table').forEach((table) => {
    table.classList.add('wiggle');
    setTimeout(() => {
      table.classList.remove('wiggle');
      is_wiggling = false;
    }, 500);

    let is_wiggling = false

    table.addEventListener('scroll', () => {
      if (table.scrollTop === 0 || table.scrollTop + table.offsetHeight >= table.scrollHeight) {
        if(!is_wiggling) {
          is_wiggling = true;
          table.classList.add('wiggle');
          setTimeout(() => {
            table.classList.remove('wiggle');
            is_wiggling = false;
          }, 200);
        }
      }
    });
  });

  // a function for rendering each position's own table
  const render_table = (players, title) => {
    return (
      <div className="table-container fade-in">
        <h2>{title}</h2>
        <div className="table" onMouseEnter={disableScrolling} onMouseLeave={enableScrolling}>
          <table border="2">
            <thead>
              <tr>
                <th>Player</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {players.map(([id, player], index) => (
                <tr key={index}>
                  <td>{player.name}</td>
                  <td>{player.rating}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };  

  return (
    <div className="App">
      {/* top bar */}
      <div class="bar">
        <header className="top-bar">
          <div className="top-bar-content">
            <img src={logo} alt="Logo" className="logo"/>
            <h1 className="header">FPL Player Scores</h1>
          </div>
        </header>
        </div>

        {/* main content */}
        <main className="main-content">
          <div className="background-top">
            <div className="top-section">
              <div className="sliding-menu-container">
                <Sliding_menu />
              </div>
              <div className="dream-eleven-container">
                <DreamEleven players={all_players}/>
              </div>
            </div>
          </div>
          <div className="background-table">
            {/* rendering each table */}
            <div className="table-wrapper">
                {render_table(sorted_gk, "Goalkeepers")}
                {render_table(sorted_def, "Defenders")}
                {render_table(sorted_mid, "Midfielders")}
                {render_table(sorted_fwd, "Forwards")}
            </div>
          </div>
        </main>
    </div>
  );
}

export default App;