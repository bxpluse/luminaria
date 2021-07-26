import React from 'react';
import Badge from 'react-bootstrap/Badge'
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container'
import Masonry from 'react-masonry-css';
import {Link} from 'react-router-dom'
import './Home.css';


function Home(props) {

    const applications = [];
    for(let i = 0; i < props.apps.length; i++){
        const app = props.apps[i];
        applications.push(
            <AppCard key={app.id} app={app} order={app.order}/>
        )
    }

    return (
        <Container>
            <Masonry
                breakpointCols={4}
                className='masonry-grid'
                columnClassName='masonry-grid_column'>
                {applications}
            </Masonry>
        </Container>
    );
}

function AppCard(props) {
    let variant;
    switch(props.app.status) {
        case 'Running':
            variant = 'success';
            break;
        case 'Stopped':
            variant = 'warning'
            break;
        case 'Ready':
            variant = 'info'
            break;
        case 'Error':
            variant = 'danger'
            break;
        case 'Link':
            variant = 'dark'
            break;
        default:
            variant = 'secondary'
    }

    const is_link = props.app.url.includes('https');

    return (
        <Card className={'mt-5 shadow dashboard-card'}>
            {is_link ? (
                <a className={'app-link'} href={props.app['url']} target='_blank' rel='noopener noreferrer'>
                    <Card.Img variant="top" src={props.app.image} />
                    <Badge className={'app-badge badge-pill'} variant={variant}>{props.app.status}</Badge>
                </a>
            ) : (
                <Link className={'app-link'} to={props.app['url']}>
                    <Card.Img variant='top' src={props.app.image} />
                    <Badge className={'app-badge badge-pill'} variant={variant}>{props.app.status}</Badge>
                </Link>
            )}
            <Card.Body>
                <Link className={'appcard app-link'} to='/'>
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