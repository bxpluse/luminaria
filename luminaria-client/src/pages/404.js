import React, {useEffect, useState} from 'react';
import {Image} from 'react-bootstrap';
import Container from 'react-bootstrap/Container';
import Request from '../Requests';
import './404.css';


function NotFound404() {

    const [imageUrl, setImageUrl] = useState(null);
    const IMAGE_KEY = '404_IMAGE_URL';

    useEffect(() => {
        setImageUrl(localStorage.getItem(IMAGE_KEY));
        const element = document.getElementById("404-container");
        element.scrollIntoView();
    }, []);

    if (!imageUrl) {
        Request.POST_JSON('/exec/syscmd/fetch-url', {url: IMAGE_KEY}).then(data => {
            setImageUrl(data.url);
            localStorage.setItem(IMAGE_KEY, data.url);
        });
    }

    return (
        <Container id='404-container'>
            <div className='container-404'>
                <h2>404 - Page not found</h2>
            </div>
            <br/>
            <div className='container-404'>
                <Image className='w-50' src={imageUrl} roundedCircle/>
            </div>
        </Container>
    );
}


export default NotFound404;