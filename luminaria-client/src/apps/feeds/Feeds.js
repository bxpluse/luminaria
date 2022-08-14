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
        Request.GET('/feeds/entries').then(data => {
            setEntries(data['entries']);
        });
        setTimeout(() => {
            setPageLoaded(true);
        }, 300)
    }, []);

    function updateFeeds() {
        Request.GET('/feeds/force-fetch-feed').then(() => {
            Request.GET('/feeds/entries').then(data => {
                setEntries(data['entries']);
            })
        });
    }


    function dismiss(key) {
        Request.EXEC('/feeds/dismiss', {id: key}).then(data => {
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

    const entryCards = entries.map(entry => {
        const metadata = JSON.parse(entry.metadata);
        let extra;
        extra = 'Comments: ' + metadata['num_comments']
            + ' | Score: ' + metadata['score']
            + ' | Ratio: ' + metadata['upvote_ratio'];
        return (
            <Card key={entry.link}>
                <Card.Body>
                    <Card.Title>
                        <span>
                            [{StringUtil.capitalize(entry.site)}] &nbsp;
                            <a href={entry.link}>{StringUtil.stripPeriod(entry.title)}</a>
                        </span>
                        <DismissButton onClick={() => dismiss(entry.id)}/>
                    </Card.Title>
                    <Card.Subtitle className='mb-2 text-muted'>
                        {DateUtil.parse(entry['published_datetime'])} &nbsp;
                        <InfoSymbol onHover={renderTooltip(entry)}/>
                    </Card.Subtitle>
                    {Object.keys(metadata).length > 0 ?
                        <Card.Subtitle className='mt-2 mb-2 text-muted'>
                            {extra}
                        </Card.Subtitle> : null
                    }
                    <Card.Text>{entry.summary}</Card.Text>
                </Card.Body>
            </Card>
        )
    }) ?? [];

    return (
        <Container>
            <Masonry
                breakpointCols={1}
                className='masonry-grid masonry-grid-extra-margin'
                columnClassName='masonry-grid_column'>
                <MyButton text='Update Feeds' onClick={() => updateFeeds()}/>
                <br/><br/>
                {entryCards.length === 0 && pageLoaded ? <h2>No Unread Feeds</h2> : entryCards}
            </Masonry>
        </Container>
    );
}


export default Feeds;