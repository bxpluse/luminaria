import React, {useEffect, useState} from "react";
import Container from 'react-bootstrap/Container';
import Request from "../../Requests";

function News() {

    const [articles, setArticles] = useState([]);

    useEffect(() => {
        Request.POST_JSON('/exec/news/fetch-news', {}).then(data => {
            setArticles(data['articles']);
        });
    }, []);

    let links = [];

    for (const article of articles){
        links.push(
            <span><a href={article.url}>{article.title}</a>
            <br/></span>
        );
    }

    return (
        <Container>
            {links}
        </Container>
    );
}


export default News;