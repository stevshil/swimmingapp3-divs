import React, { Component } from "react";
import logo from '../images/tps.png';
import './Layout.css';

class Header extends Component {
    render() {
        return (
            <header>
            <div className="home-container01">
                <img
                    alt="Company Logo"
                    src={logo}
                    className="home-logo"
                />
                <span className="Heading">
                    Swimming Info Folkestone
                </span>
            </div>
        </header>
        )
    }
}

export default Header;