import React, {useEffect} from 'react';
import {Link} from 'react-router-dom';
import AppUtil from "../util/AppUtil";
import './Header.css';

function Header() {

    useEffect(() => {
        import('../components/Fireworks').then(Fireworks => {
            Fireworks.loop();
        });
    }, []);

    let bg = 'bg-prod';
    let envSuffix = '';
    if (AppUtil.isDevEnv()) {
        bg = 'bg-dev';
        envSuffix = 'DEV';
    }

    return (
        <header id='header' className={'app-header ' + bg}>
            <canvas id="canvas"/>
            <Link className={'element1 app-link'} to='/'>
                <p id='title'>𝓛𝓾𝓶𝓲𝓷𝓪𝓻𝓲𝓪 {envSuffix}</p>
            </Link>
        </header>
    )
}


export default Header;