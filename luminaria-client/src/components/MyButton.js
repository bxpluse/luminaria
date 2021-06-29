import Button from "react-bootstrap/Button";
import React from "react";
import './Custom.css'

function MyButton(props) {
    return (
        <Button className={props.variant === undefined ? '' : 'link-btn'}
            onClick={(e) => {
                e.currentTarget.blur();
                click(props);
            }}
            variant={props.variant === undefined ? 'info' : props.variant}
            disabled={props.disabled}
        >
            {props.text}
        </Button>
    )
}

function click(props){
    if (props.hasOwnProperty('onClick')){
        props.onClick();
    }
}


export default MyButton;