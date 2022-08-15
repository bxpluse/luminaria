import React from 'react';
import './Custom.css'


function DismissButton(props) {

    const handleClick = () => {
        props.onClick();
    }

    return (
        <span onClick={handleClick} className='emoji-btn'> ⓧ</span>
    );
}


export default DismissButton;