import Button from "react-bootstrap/Button";
import React from "react";

function MyButton(props) {
    return (
        <Button
            onClick={(e) => {
                e.currentTarget.blur();
                click(props);
            }}
            variant="info">
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