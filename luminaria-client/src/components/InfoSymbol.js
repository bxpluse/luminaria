import React from "react";
import {OverlayTrigger} from 'react-bootstrap';
import './Custom.css'


function InfoSymbol(props) {
    const symbol = props.symbol !== undefined ? props.symbol : 'ⓘ';
    if (props.onHover !== undefined) {
        return (
            <OverlayTrigger
                placement='right'
                delay={{ show: props.delayShow !== undefined ? props.delayShow : 400,
                    hide: props.delayHide !== undefined ? props.delayHide : 400 }}
                overlay={props.onHover}
            >
                <span className='info-symbol'>{symbol}</span>
            </OverlayTrigger>
        );
    }

    return (
        <span className='info-symbol'>{symbol}</span>
    );
}


export default InfoSymbol;