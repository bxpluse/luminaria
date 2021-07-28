import React from 'react';
import {Link} from 'react-router-dom';


function GearLink(props) {

    const marginTop = props.marginTop === undefined ? '0px' : props.marginTop;
    const marginBottom = props.marginBottom === undefined ? '0px' : props.marginBottom;
    const marginLeft = props.marginLeft === undefined ? '0px' : props.marginLeft;
    const marginRight = props.marginRight === undefined ? '0px' : props.marginRight;

    return (
        <div style={{marginTop: marginTop, marginBottom: marginBottom,
            marginLeft: marginLeft, marginRight: marginRight}}>
            <Link to={'/' + props.link}>
                <span>⚙</span>
            </Link>
        </div>
    );
}


export default GearLink;