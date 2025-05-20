import './Probabilities.css';
import React from 'react';
import { useState, useEffect } from 'react';

export default function Probabilities({ Probabilities1, Probabilities2, source }) {
    console.log('Probabilities 1:', Probabilities1);
    console.log('Probabilities 2:', Probabilities2);
    const [showProbabilities1, setShowProbabilities1] = useState(false);
    const [showProbabilities2, setShowProbabilities2] = useState(false);

    useEffect(() => {
        // Check if it's a non-empty array (either 1D or 2D)
        const isProb1Valid = Array.isArray(Probabilities1) && Probabilities1.length > 0;
        const isProb2Valid = Array.isArray(Probabilities2) && Probabilities2.length > 0;

        setShowProbabilities1(isProb1Valid);
        setShowProbabilities2(isProb2Valid);
    }, [Probabilities1, Probabilities2]);

    // Early return if no probabilities to show
    if (!showProbabilities1 && !showProbabilities2) return null;

    const renderProbabilityTable = (data, title) => {
        if (!Array.isArray(data) || data.length === 0) return null;

        // Convert 1D array to 2D array if needed (each number becomes a single-cell row)
        const tableData = data[0] instanceof Array ? data : data.map(item => [item]);

        return (
            <div className="probability-table-container">
                <h3>{title}</h3>
                <table>
                    <tbody>
                        {tableData.map((row, i) => (
                            <tr key={i}>
                                <th>P{i + 1}</th>
                                {row.map((cell, j) => (
                                    <td
                                        key={j}
                                        className={`payoffmatrix-cell ${cell > 0 ? 'positive' : cell < 0 ? 'negative' : ''
                                            }`}
                                    >
                                        {typeof cell === 'number' ? (cell === 0 ? 0.0 : cell.toFixed(6)) : cell}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="probabilities-container">
            {renderProbabilityTable(
                Probabilities1,
                source === 'simulation' ? 'Hider Probabilities (Simulation)' : 'Computer Probabilities'
            )}
            {source === 'simulation' && renderProbabilityTable(
                Probabilities2,
                'Seeker Probabilities (Simulation)'
            )}
        </div>
    );
}