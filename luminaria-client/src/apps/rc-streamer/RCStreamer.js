import React, {useEffect, useState} from 'react';
import 'react-toastify/dist/ReactToastify.css';
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form'
import FormControl from 'react-bootstrap/FormControl'
import InputGroup from 'react-bootstrap/InputGroup'
import {STATUS} from '../../Enums'
import Request from "../../Requests";
import Jumbotron from "react-bootstrap/Jumbotron";

function RCStreamer() {

    const [ready, setReady] = useState(null);
    const [debugging, setDebugging] = useState(false);
    const [nextRun, setNextRun] = useState('');
    const [ram, setRam] = useState({});

    useEffect(() => {
        Request.STATUS('/rc-streamer').then(data => {
            if(data['status'] === STATUS.READY || data['status'] === STATUS.STOPPED){
                setReady(true);
            } else {
                setReady(false);
            }
            setDebugging(data['debugging']);
            setNextRun(data['next_run']);
            setRam(data['ram']);
        });
    }, []);

    if(ready === null){
        return (
            <Container/>
        );
    }

    let button;
    if(ready){
        button = <Button variant="primary" size="lg" onClick={() => {start(); setReady(false);}}>
            Start
        </Button>
    } else {
        button = <Button variant="primary" size="lg" disabled={true}>
            Running ...
        </Button>
    }

    return (
        <Container>
            <Jumbotron>
                <h1>RC Streamer</h1>
                <br/>
                {button}
                <br/><br/>
                <Button variant="primary" onClick={() => {dump()}}>
                    Dump to File
                </Button>
                <br/><br/>
                <Form>
                    <Form.Check type="checkbox" label="Debugging" checked={debugging} onChange={() => {
                        toggleDebug(!debugging);
                        setDebugging(!debugging);
                    }}/>
                    <br/><br/>
                    <InputGroup className="mb-3">
                        <InputGroup.Prepend>
                            <InputGroup.Text id="basic-addon1">Next Run Time</InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl value={nextRun} disabled={true}/>
                    </InputGroup>
                    <InputGroup className="mb-3">
                        <InputGroup.Prepend>
                            <InputGroup.Text id="basic-addon1">Data on RAM</InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl as="textarea" value={JSON.stringify(ram)} disabled={true}/>
                    </InputGroup>
                </Form>
            </Jumbotron>
        </Container>
    );
}

function start(){
    Request.EXEC('/rc-streamer/run', {}).then(() => {});
}

function dump(){
    Request.EXEC('/rc-streamer/dump-to-file', {}).then(() => {});
}

function toggleDebug(isDebug){
    Request.EXEC('/rc-streamer/debug', {isDebug: isDebug}).then(() => {});
}


export default RCStreamer;