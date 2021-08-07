import React, {useEffect, useState} from 'react';
import {Tooltip} from 'react-bootstrap';
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Masonry from "react-masonry-css";
import DismissButton from '../../components/DismissButton';
import InfoSymbol from '../../components/InfoSymbol';
import MyButton from '../../components/MyButton';
import Request from '../../Requests';
import DateUtil from '../../util/DateUtil';
import StringUtil from '../../util/StringUtil';
import './Feed.css';


function Feeds() {

    const [entries, setEntries] = useState([]);
    const [pageLoaded, setPageLoaded] = useState(false);

    useEffect(() => {
        Request.GET_JSON('/get/feeds/entries').then(data => {
            setEntries(data['entries']);
        });
        setTimeout(() => {
            setPageLoaded(true);
        }, 300)
    }, []);

    function updateFeeds() {
        Request.GET_JSON('/get/feeds/force-fetch-feed').then(() => {
            Request.GET_JSON('/get/feeds/entries').then(data => {
                setEntries(data['entries']);
            })
        });
    }

    let entryCard = [];

    function dismiss(key){
        Request.POST_JSON('/exec/feeds/dismiss', {id: key}).then(data => {
            setEntries(data['entries']);
        });
    }

    const renderTooltip = (entry) => (
        <Tooltip id={entry.link} className='mytooltip'>
            Site: {entry.site} <br/>
            {entry.author !== null ? <span>Author: {entry.author} <br/></span> : null}
            {entry.tags.length > 0 ? <span>Tags: {StringUtil.listToString(entry.tags, ', ')} <br/></span> : null}
        </Tooltip>
    );

    for (const entry of entries){
        if (entry.show) {
            entryCard.push(
                <Card key={entry.link}>
                    <Card.Body>
                        <Card.Title>
                            <a href={entry.link}>{StringUtil.stripPeriod(entry.title)}</a>
                            <DismissButton onClick={() => dismiss(entry.id)}/>
                        </Card.Title>
                        <Card.Subtitle className='mb-2 text-muted'>
                            {DateUtil.parse(entry['published_datetime'])} &nbsp;
                            <InfoSymbol onHover={renderTooltip(entry)}/>
                        </Card.Subtitle>
                        <Card.Text>{entry.summary}</Card.Text>
                    </Card.Body>
                </Card>
            );
        }
    }

    return (
        <Container>
            <Masonry
                breakpointCols={1}
                className='masonry-grid masonry-grid-extra-margin'
                columnClassName='masonry-grid_column'>
                <MyButton text='Update Feeds' onClick={() => updateFeeds()}/>
                <br/><br/>
                {entryCard.length === 0 && pageLoaded ? <h2>No Unread Feeds</h2> : entryCard}
            </Masonry>
        </Container>
    );
}


export default Feeds;