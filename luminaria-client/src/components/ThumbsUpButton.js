import React from 'react';
import './Custom.css'


function ThumbsUpButton(props) {

    const handleClick = () => {
        props.onClick();
    }

    return (
        <span onClick={handleClick} className='emoji-btn'> 👍</span>
);
}


export default ThumbsUpButton;