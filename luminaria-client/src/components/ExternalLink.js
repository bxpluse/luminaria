import React from 'react';
import './Custom.css'


function ExternalLink(props) {

    const marginTop = props.marginTop === undefined ? '0px' : props.marginTop;
    const marginBottom = props.marginBottom === undefined ? '0px' : props.marginBottom;
    const marginLeft = props.marginLeft === undefined ? '0px' : props.marginLeft;
    const marginRight = props.marginRight === undefined ? '0px' : props.marginRight;

    return (
        <div className='external-link' style={{marginTop: marginTop, marginBottom: marginBottom,
            marginLeft: marginLeft, marginRight: marginRight}}>
            <a className='no-deco' target='_blank' rel='noreferrer' href={props.link}>{props.symbol}</a>
        </div>
    );
}


export default ExternalLink;