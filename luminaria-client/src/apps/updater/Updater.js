import React, {useState} from 'react';
import Button from 'react-bootstrap/Button'
import CardColumns from "react-bootstrap/CardColumns";
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form'
import Jumbotron from 'react-bootstrap/Jumbotron';
import Loading from '../../components/Loading';
import {STATUS} from '../../Enums'
import '../../pages/Home.css';
import Request from '../../Requests';


function Updater() {
    return (
        <Container>
            <Jumbotron>
                <h1>Exchange Updater</h1>
                <br/>
                <CardColumns>
                    <UpdateCard exchange='All'/>
                </CardColumns>
            </Jumbotron>
        </Container>
    )
}

function UpdateCard(props) {

    const [status, setStatus] = useState(STATUS.READY);

    function updateExchange(exchange) {
        setStatus(STATUS.INPROGRESS);
        Request.EXEC('/updater/update', {exchange: exchange}).then(() => {
            setStatus(STATUS.READY);
        });
    }

    return (
        <Form className='card p-5 orange shadow-sm'>
            <Form.Group>
                <Form.Label>Update Exchange</Form.Label>
                <Form.Control type="text" value={props.exchange} disabled={true}/>
            </Form.Group>
            {status === STATUS.READY ?
                <Button onClick={() => updateExchange(props.exchange)} variant="info">Update</Button> : null
            }
            <Loading width={100} isLoading={status !== STATUS.READY}/>
        </Form>
    );
}


export default Updater;