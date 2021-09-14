import React, {useEffect, useState} from 'react';
import {Image} from 'react-bootstrap';
import Spinner from 'react-bootstrap/Spinner';
import Request from '../Requests';
import './Loading.css';


function Loading(props) {

    const LOADING_SPINNER_URL = 'LOADING_SPINNER_URL';
    const [loadingImageUrl, setLoadingImageUrl] = useState(null);

    useEffect(() => {
        setLoadingImageUrl(localStorage.getItem(LOADING_SPINNER_URL));
    }, []);

    if (!(props.isLoading)) {
        return null;
    }

    if (!loadingImageUrl) {
        Request.QUERY('/syscmd/fetch-url', {url: LOADING_SPINNER_URL}).then(data => {
            setLoadingImageUrl(data.url);
            localStorage.setItem(LOADING_SPINNER_URL, data.url);
        });
    }

    const className = props.width === undefined ? 'w-100' : 'w-' + props.width;

    return (
        <div className='loading-div'>
            <Image className={className} src={loadingImageUrl} rounded/>
            {props.extraSpinner &&
            <Spinner className='loading-spinner' animation='grow' variant='dark'/>
            }
        </div>
    );
}


export default Loading;