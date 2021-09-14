import React, {useEffect, useState} from 'react';
import Card from 'react-bootstrap/Card'
import Container from 'react-bootstrap/Container';
import Masonry from 'react-masonry-css'
import '../../components/masonry.css';
import Request from '../../Requests';


function TopTen() {

    const [top, setTop] = useState({});

    useEffect(() => {
        Request.EXEC('/top-ten/absolute_top', {}).then(data => {
            setTop(data['absolute_top']);
        });
    }, []);

    let days = [];
    for (const [key, value] of Object.entries(top)) {
        days.push(<DayCard key={key} date={key} symbols={value['symbols']} isWeekend={value['is_weekend']}
                           mentions={value['mentions']} totalMentions={value['total_mentions']}
                           dayOfWeek={value['day_of_week']}
        />);
    }
    days.reverse();

    return (
        <Container>
            <Masonry
                breakpointCols={4}
                className="masonry-grid"
                columnClassName="masonry-grid_column">
                {days}
            </Masonry>
        </Container>
    );
}

function DayCard(props) {

    let top = [];
    for(let i = 0; i < props.symbols.length; i++){
        const symbol = props.symbols[i];
        const symbolMentions = props.mentions[i];
        const num = (symbolMentions / props.totalMentions) * 100;
        const percentage = Math.round((num + Number.EPSILON) * 100) / 100;

        top.push(
            <tr key={i}>
                <td>{i + 1 + '. ' + symbol}</td>
                <td>{percentage}%</td>
                <td>{symbolMentions}</td>
            </tr>);
    }

    // let dayType = props.isWeekend ? 'Weekend': 'Weekday';

    return (

        <Card>
            <Card.Body>
                <Card.Title className="card-title">{props.date}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">{props.dayOfWeek}</Card.Subtitle>
                <p>Total Comments: {props.totalMentions}</p>

                    <table style={{width: "100%"}}>
                        <thead>
                            <tr>
                                <td>Symbol</td>
                                <td>Percent</td>
                                <td>Mentions</td>
                            </tr>
                        </thead>
                        <tbody>
                            {top}
                        </tbody>
                    </table>

            </Card.Body>
        </Card>
    );
}


export default TopTen;