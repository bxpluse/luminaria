import React from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Config from "../../config"
import CardColumns from "react-bootstrap/CardColumns";
import Spinner from 'react-bootstrap/Spinner'
import '../../pages/Home.css';
import { STATUS } from '../../Enums'

class Updater extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            exchanges: []
        }
    }

    componentDidMount() {
        window.scrollTo(0, 0)

        fetch(Config.HOST + '/updater/exchanges', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            this.setState({
                exchanges: data.exchanges
            });
        })
    }



    render() {
        const exchanges = [];
        for (const exchange of this.state.exchanges){
            exchanges.push(
                <UpdateCard key={exchange} exchange={exchange}/>
            );
        }

        return (
            <Container>
                <div>
                    <CardColumns>
                        {exchanges}
                    </CardColumns>
                </div>
            </Container>
        );
    }
}

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
        fetch(Config.HOST + '/updater/exchanges/' + exchange, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        }).then(response => {
            this.setState({
                status: STATUS.READY
            })
        })
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


export default Updater;