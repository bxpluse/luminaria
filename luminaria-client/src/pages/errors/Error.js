import React, {useEffect, useState} from 'react';
import {Image} from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import {Link} from "react-router-dom";
import Request from '../../Requests';
import ObjUtil from '../../util/ObjUtil';
import './Error.css';


function Error(props) {

    const IMAGE_KEY = 'ERROR_IMAGE_URL';
    const [imageUrl, setImageUrl] = useState(localStorage.getItem(IMAGE_KEY));

    useEffect(() => {
        const element = document.getElementById("error-container");
        element.scrollIntoView();

        if (ObjUtil.isFalsy(imageUrl)) {
            Request.QUERY('/syscmd/fetch-url', {url: IMAGE_KEY}).then(data => {
                setImageUrl(data.url);
                localStorage.setItem(IMAGE_KEY, data.url);
            });
        }
    }, [imageUrl]);

    return (
        <Container id='error-container'>
            <div className='error-center'>
                {props.errorCode.code === 401 ?
                    <Link to='/login'>
                        <h2>{props.errorCode.code} - {props.errorCode.message}</h2>
                    </Link> :
                    <h2>{props.errorCode.code} - {props.errorCode.message}</h2>
                }
            </div>
            <br/>
            <div className='error-center'>
                <Image className='w-50' src={imageUrl} roundedCircle/>
            </div>
        </Container>
    );
}


export default Error;