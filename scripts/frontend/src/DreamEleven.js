
import React from 'react';
import "./DreamEleven.css";

function DreamEleven({ players }) {
    // extract array
    const { goalkeeper, defenders, midfielders, forwards } = players;

    return (
        <div className="dream-eleven-container">
            <h2>Dream Eleven</h2>
            <div className="pitch">
                {/* Goalkeeper */}
                <div className="goalkeeper">
                    {goalkeeper && (
                        <span>{goalkeeper[1].name} {goalkeeper[1].rating}</span>
                    )}
                </div>

                {/* Defenders */}
                <div className="defenders">
                    {defenders && defenders.map(([id, player], index) => (
                        <span key={index}>{player.name} {player.rating}</span>
                    ))}
                </div>

                {/* Midfielders */}
                <div className="midfielders">
                    {midfielders && midfielders.map(([id, player], index) => (
                        <span key={index}>{player.name} {player.rating}</span>
                    ))}
                </div>

                {/* Forwards */}
                <div className="forwards">
                    {forwards && forwards.map(([id, player], index) => (
                        <span key={index}>{player.name} {player.rating}</span>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default DreamEleven;