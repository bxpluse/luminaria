import React, {useEffect, useState} from 'react';
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Masonry from 'react-masonry-css';
import ExternalLink from '../../components/ExternalLink';
import Request from '../../Requests';


function Finder() {

    const [schedules, setSchedules] = useState([]);

    useEffect(() => {
        Request.GET_JSON('/get/finder/fetch-schedules').then(data => {
            setSchedules(data['schedules']);
        });
    }, []);


    let schedulesCard = [];
    for (const schedule of schedules){
        if (schedule === undefined || schedule['schedules'] === undefined) {
            continue;
        }

        let maxKey = '0';
        let maxUrl = '';

        for (const [key, value] of Object.entries(schedule['schedules'])) {
            if (key > maxKey) {
                maxKey = key;
                maxUrl = value['media_urls'][0];
            }
        }

        schedulesCard.push(
            <Card key={schedule.name}>
                <Card.Body>
                    <Card.Title>
                        <div>
                            {schedule.name} <ExternalLink symbol='🔗' link={'https://twitter.com/i/status/' + maxKey}/>
                        </div>
                    </Card.Title>
                    <Card.Img variant='bottom' src={maxUrl}/>
                </Card.Body>
            </Card>
        );
    }

    return (
        <Container>
            <Masonry
                breakpointCols={1}
                className='masonry-grid masonry-grid-extra-margin'
                columnClassName='masonry-grid_column'>
                {schedulesCard}
            </Masonry>
        </Container>
    );
}


export default Finder;