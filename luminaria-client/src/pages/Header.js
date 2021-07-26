import React, {useEffect} from 'react';
import {Link} from 'react-router-dom';
import './Header.css';


function Header() {

    useEffect(() => {
        import('../components/Fireworks').then(Fireworks => {
            Fireworks.loop();
        });
    }, []);

    return (
        <header id='header' className='App-header'>
            <canvas id="canvas"/>
            <Link className={'element1 app-link'} to='/'>
                <p id='title'>𝓛𝓾𝓶𝓲𝓷𝓪𝓻𝓲𝓪</p>
            </Link>
        </header>
    )
}


export default Header;