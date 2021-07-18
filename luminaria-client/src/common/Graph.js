import InnerHTML from 'dangerously-set-html-content'
import React, {useEffect, useState} from 'react';
import Request from '../Requests';
import AppUtil from '../util/AppUtil'

function Graph() {
    const [html, setHtml] = useState('');

    useEffect(() => {
        getGraph().then(html => {
            setHtml(html);
        });
    }, []);

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