import React, {useEffect, useState} from 'react';
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Request from "../../Requests";

function HealthCheck() {

    const [date, setDate] = useState('');
    const [uptime, setUptime] = useState('');
    const [temperature, setTemperature] = useState('');
    const [ram, setRam] = useState('');
    const [space, setSpace] = useState('');


    useEffect(() => {
        checkHealth().then(res => {
            setDate(res.date);
            setUptime(res.uptime);
            setTemperature(res.temperature);
            setRam(res.ram);
            setSpace(res.space);
        })

    }, []);

    return (
        <Container>
                <HealthCard title='Date' body={date}/>
                <HealthCard title='Uptime' body={uptime}/>
                <HealthCard title='Temperature' body={temperature}/>
                <HealthCard title='Ram' body={ram}/>
                <HealthCard title='Space' body={space}/>
        </Container>
    );
}


function HealthCard(props) {
    return (
        <Card style={{ width: '18rem' }}>
            <Card.Body>
                <Card.Title>{props.title}</Card.Title>
                <Card.Text>
                    {props.body}
                </Card.Text>
            </Card.Body>
        </Card>
    );
}


async function checkHealth() {
    return await Request.POST_JSON('/exec/health-check/checkup', {}).then(data => {
        return data;
    });
}


export default HealthCheck;