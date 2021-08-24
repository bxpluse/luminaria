import InnerHTML from 'dangerously-set-html-content'
import React, {useEffect, useState} from 'react';
import Container from 'react-bootstrap/Container';
import Request from '../Requests';
import AppUtil from '../util/AppUtil'
import Loading from './Loading';


function Graph() {
    const [html, setHtml] = useState('');
    const [showLoading, setShowLoading] = useState(false)

    useEffect(() => {
        setTimeout(() => {
            setShowLoading(true)
        }, 200)
        getGraph().then(html => {
            setHtml(html);
        });
    }, []);

    if (html === '' && showLoading) {
        return (
            <Container>
                <p>Loading Graph ...</p>
                <Loading width={25} isLoading={showLoading}/>
            </Container>
        );
    }

    return (
        <InnerHTML html={html} />
    );
}


async function getGraph() {
    const params = AppUtil.getUrlParams();
    const api = params['api'];
    const height = isNaN(window.innerHeight) ? window.clientHeight : window.innerHeight - 100;
    params['config'] = {'height': height}
    return await Request.POST_JSON('/exec/graphy/' + api, params).then(data => {
        return data.html;
    });
}


export default Graph;