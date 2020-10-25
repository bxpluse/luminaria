import React from 'react';
import Card from 'react-bootstrap/Card';
import CardColumns from 'react-bootstrap/CardColumns'
import Container from 'react-bootstrap/Container'
import Badge from 'react-bootstrap/Badge'
import { Link } from 'react-router-dom'
import Config from "../config"
import './Home.css';

class Home extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            apps: {}
        }
    }

    componentDidMount() {
        fetch(Config.HOST + '/get-all-apps', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            const applications = [];
            for (const [, app] of Object.entries(data)) {
                applications.push(app);
            }
            applications.sort(function(a, b){
                return a.order - b.order;
            });
            this.setState({
                apps: applications
            });
        })
    }

    render() {
        const applications = [];
        for(let i = 0; i < this.state.apps.length; i++){
            const app = this.state.apps[i];
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
}

class AppCard extends React.Component {

    render() {
        let variant = "";
        if(this.props.app.status === "Running"){
            variant = 'success';
        } else if(this.props.app.status === "Stopped"){
            variant = 'danger'
        } else if(this.props.app.status === "Ready"){
            variant = 'info'
        } else {
            variant = 'warning'
        }

        return (
            <Card className={'mt-5 shadow dashboard-card'}>
                <Link className={'app-link'} to={'/' + this.props.app.url}>
                    <Card.Img variant="top" src={this.props.app.image} />
                    <Badge className={'element2 badge-pill'} variant={variant}>{this.props.app.status}</Badge>
                </Link>

                <Card.Body>
                    <Link className={'element1 app-link'} to="/">
                        <Card.Title>{this.props.app.name}</Card.Title>
                    </Link>
                    <Card.Text>
                        {this.props.app.description}
                    </Card.Text>
                </Card.Body>
            </Card>
        );
    }
}


export default Home;