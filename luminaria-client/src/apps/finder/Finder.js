import React, {useEffect, useState} from 'react';
import {Tabs} from 'react-bootstrap';
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Tab from 'react-bootstrap/Tab';
import Masonry from 'react-masonry-css';
import ExternalLink from '../../components/ExternalLink';
import Request from '../../Requests';
import DictUtil from '../../util/DictUtil';

function Finder() {

    const [schedules, setSchedules] = useState([]);

    useEffect(() => {
        Request.GET('/finder/fetch-schedules').then(data => {
            setSchedules(data['schedules']);
        });
    }, []);

    const scheduleTabs = {};
    for (const schedule of schedules) {
        if (schedule === undefined || schedule['latest'] === undefined) {
            continue;
        }

        const latest = schedule['latest'];
        const metadata = schedule['<!METADATA>'];
        const tweetId = latest['tweet_id'];
        const url = latest['media_urls'][0];

        const tab = metadata['tab'] || 'Unknown';
        if (!(tab in scheduleTabs)) {
            scheduleTabs[tab] = [];
        }

        scheduleTabs[tab].push(
            <Card key={schedule.name}>
                <Card.Body>
                    <Card.Title>
                        <span>
                            <ExternalLink symbol={schedule.name} link={metadata['slink']}/>
                            <ExternalLink symbol='🔗' link={'https://twitter.com/i/status/' + tweetId}/>
                        </span>
                    </Card.Title>
                    <Card.Img variant='bottom' src={url}/>
                </Card.Body>
            </Card>
        );
    }

    const tabs = [];
    Object.entries(DictUtil.sort(scheduleTabs)).forEach(([key, value]) => {
        tabs.push(
            <Tab key={key} eventKey={key} title={key}>
                {value}
            </Tab>
        );
    })

    return (
        <Container>
            <Masonry
                breakpointCols={1}
                className='masonry-grid masonry-grid-extra-margin'
                columnClassName='masonry-grid_column'>
                <Tabs>
                    {tabs}
                </Tabs>
            </Masonry>
        </Container>
    );
}


export default Finder;