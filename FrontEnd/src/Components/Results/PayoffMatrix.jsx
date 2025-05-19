import './PayoffMatrix.css';

export default function PayoffMatrix({ payoffs }) {
    if (!Array.isArray(payoffs) || payoffs.length === 0) return null;

    return (
        <div className="payoffmatrix-container">
            <h3 className="payoffmatrix-title">Payoff Matrix</h3>
            <div className="payoffmatrix-table-container">
                <table className="payoffmatrix-table">
                    <thead>
                        <tr>
                            <th></th>
                            {payoffs.map((_, j) => (
                                <th key={j}>C{j + 1}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {payoffs.map((row, i) => (
                            <tr key={i}>
                                <th>R{i + 1}</th>
                                {row.map((cell, j) => (
                                    <td
                                        key={j}
                                        className={`payoffmatrix-cell ${cell > 0 ? 'positive' : cell < 0 ? 'negative' : ''}`}
                                    >
                                        {cell}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}