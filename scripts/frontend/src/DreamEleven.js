
import React from 'react';
import "./DreamEleven.css";

function DreamEleven({ players }) {
    // extract array
    const { goalkeeper, defenders, midfielders, forwards } = players;

    return (
        <div className="pitch">
            <h2>Dream Eleven</h2>

            {/* Goalkeeper */}
            <div className="goalkeeper">
                {goalkeeper && (
                    <span>{players.goalkeeper[0]} {players.goalkeeper[1]}</span>
                )}
            </div>

            {/* Defenders */}
            <div className="defenders">
                {defenders && players.defenders.map(([name, rating], index) => (
                    <span key={index}>{name} {rating}</span>
                ))}
            </div>

            {/* Midfielders */}
            <div className="midfielders">
                {midfielders && midfielders.map(([name, rating], index) => (
                    <span key={index}>{name} {rating}</span>
                ))}
            </div>

            {/* Forwards */}
            <div className="forwards">
                {forwards && forwards.map(([name, rating], index) => (
                    <span key={index}>{name} {rating}</span>
                ))}
            </div>
        </div>
    );
}

export default DreamEleven;