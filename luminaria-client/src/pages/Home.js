import React, {useEffect, useState} from 'react';
import Card from 'react-bootstrap/Card';
import CardColumns from 'react-bootstrap/CardColumns'
import Container from 'react-bootstrap/Container'
import Badge from 'react-bootstrap/Badge'
import {Link} from 'react-router-dom'
import './Home.css';
import Request from "../Requests";

function Home() {

    const [apps, setApps] = useState({});

    useEffect(() => {
        Request.POST_JSON('/get-all-apps', {}).then(data => {
            const applications = [];
            for (const [, app] of Object.entries(data)) {
                applications.push(app);
            }
            applications.sort(function(a, b){
                return a.order - b.order;
            });
            setApps(applications);
        });
    }, []);

    const applications = [];
    for(let i = 0; i < apps.length; i++){
        const app = apps[i];
        applications.push(
            <AppCard key={app.id} app={app} order={app.order}/>
        )
    }

    return (
        <Container>
            <CardColumns>
                {applications}
            </CardColumns>
        </Container>
    );
}

function AppCard(props) {
    let variant;
    if (props.app.status === "Running") {
        variant = 'success';
    } else if (props.app.status === "Stopped") {
        variant = 'danger'
    } else if (props.app.status === "Ready") {
        variant = 'info'
    } else if (props.app.status === "Error") {
        variant = 'danger'
    } else if (props.app.status === "Link") {
        variant = 'dark'
    } else {
        variant = 'warning'
    }

    const is_link = props.app['link_to'] !== null;

    return (
        <Card className={'mt-5 shadow dashboard-card'}>
            {is_link ? (
                <a className={'app-link'} href={props.app['link_to']} target='_blank' rel='noopener noreferrer'>
                    <Card.Img variant="top" src={props.app.image} />
                    <Badge className={'element2 badge-pill'} variant={variant}>{props.app.status}</Badge>
                </a>
            ) : (
                <Link className={'app-link'} to={props.app['url']}>
                    <Card.Img variant="top" src={props.app.image} />
                    <Badge className={'element2 badge-pill'} variant={variant}>{props.app.status}</Badge>
                </Link>
            )}
            <Card.Body>
                <Link className={'element1 app-link'} to="/">
                    <Card.Title>{props.app.name}</Card.Title>
                </Link>
                <Card.Text>
                    {props.app.description}
                </Card.Text>
            </Card.Body>
        </Card>
    );
}


export default Home;