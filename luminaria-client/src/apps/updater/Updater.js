import React, {useEffect, useState} from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import CardColumns from "react-bootstrap/CardColumns";
import Spinner from 'react-bootstrap/Spinner'
import '../../pages/Home.css';
import {STATUS} from '../../Enums'
import Request from "../../Requests";
import Jumbotron from "react-bootstrap/Jumbotron";

function Updater() {

    const [exchanges, setExchanges] = useState([]);

    useEffect(() => {
        Request.POST_JSON('/updater/exchanges', {}).then(data => {
            setExchanges(data['exchanges']);
        });
    });

    const exchangesComponents = [];
    for (const exchange of exchanges){
        exchangesComponents.push(
            <UpdateCard key={exchange} exchange={exchange}/>);
    }

    return (
        <Container>
            <Jumbotron>
                <h1>Exchange Updater</h1>
                <br />
                <CardColumns>
                    {exchangesComponents}
                </CardColumns>
            </Jumbotron>
        </Container>
    )

}

function UpdateCard(props) {

    const [status, setStatus] = useState(STATUS.READY);

    function updateExchange(exchange) {
        setStatus(STATUS.INPROGRESS);
        Request.POST_JSON('/updater/exchanges/' + exchange, {}).then(() => {
            setStatus(STATUS.READY);
        });
    }

    let button;
    if(status === STATUS.READY){
        button = <Button onClick={() => updateExchange(props.exchange)} variant="info">Update</Button>;
    } else{
        button = <React.Fragment>
            <Spinner animation="border" variant="primary"/>
            <span className={'px-3'}>Updating...</span>
        </React.Fragment>
    }

    return (
        <Form className='card p-5 orange shadow-sm'>
            <Form.Group>
                <Form.Label>Update Exchange</Form.Label>
                <Form.Control type="text" value={props.exchange} disabled={true}/>
            </Form.Group>
            {button}
        </Form>
    );

}


/*

class UpdateCard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            status: STATUS.READY
        }
        this.updateExchange = this.updateExchange.bind(this);
    }

    componentWillUnmount() {
        this.setState = (state,callback)=>{};
    }

    updateExchange(exchange) {
        this.setState({
            status: STATUS.INPROGRESS
        })

        Request.POST_JSON('/updater/exchanges/', {}).then(data => {
            this.setState({
                status: STATUS.READY
            })
        });
    }

    render() {
        let button;
        if(this.state.status === STATUS.READY){
            button = <Button onClick={() => this.updateExchange(this.props.exchange)} variant="info">Update</Button>;
        } else{
            button = <React.Fragment>
                <Spinner animation="border" variant="primary"/>
                <span className={'px-3'}>Updating...</span>
            </React.Fragment>
        }

        return (
            <Form className='card p-5 orange shadow-sm'>
                <Form.Group controlId="exampleForm.ControlSelect1">
                    <Form.Label>Update Exchange</Form.Label>
                    <Form.Control type="text" value={this.props.exchange} disabled={true}/>
                </Form.Group>
                {button}
            </Form>
        );
    }
}

 */

export default Updater;