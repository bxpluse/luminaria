import React from 'react';
import './Header.css';
import {Link} from "react-router-dom";


class Header extends React.Component {

    componentDidMount() {
        import('../components/Fireworks').then(Fireworks => {
            Fireworks.loop();
        });
    }

    render() {
        return (
            <React.Fragment>
                <header id='header' className="App-header">
                    <canvas id="canvas"/>
                    <Link className={'element1 app-link'} to="/">
                        <p id='title'>𝓛𝓾𝓶𝓲𝓷𝓪𝓻𝓲𝓪</p>
                    </Link>
                </header>
            </React.Fragment>
        );
    }
}


export default Header;