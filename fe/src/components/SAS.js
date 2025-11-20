import React, {Component} from 'react';
import './Layout.css';

class SAS extends Component {
    render() {
        return (
            <>
                <div align='center' id="sas">
                    <button className="threeD-button" onClick={() => window.open("https://www.sas.org.uk/water-quality/sewage-pollution-alerts/")}>Surfers Agains Sewage</button>
                </div>
            </>
        );
    };
};

export default SAS;