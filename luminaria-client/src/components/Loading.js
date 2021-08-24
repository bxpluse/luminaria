import React, {useEffect, useState} from 'react';
import {Image} from 'react-bootstrap';
import Spinner from 'react-bootstrap/Spinner';
import Request from '../Requests';
import './Loading.css';


function Loading(props) {

    const [loadingImageUrl, setLoadingImageUrl] = useState(null);

    useEffect(() => {
        setLoadingImageUrl(localStorage.getItem('loadingImageUrl'));
    }, []);

    if (!(props.isLoading)) {
        return null;
    }

    if (!loadingImageUrl) {
        Request.POST_JSON('/exec/syscmd/fetch-url', {url: 'LOADING_SPINNER_URL'}).then(data => {
            setLoadingImageUrl(data.url);
            localStorage.setItem('loadingImageUrl', data.url);
        });
    }

    const className = props.width === undefined ? 'w-100' : 'w-' + props.width;

    return (
        <div className='loading-div'>
            <Image className={className} src={loadingImageUrl} rounded />
            {props.extraSpinner !== undefined ?
                <Spinner className='loading-spinner' animation='grow' variant='dark'/> : null
            }
        </div>
    );
}


export default Loading;