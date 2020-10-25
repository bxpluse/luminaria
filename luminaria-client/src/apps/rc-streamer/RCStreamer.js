import React, { useState, useEffect } from 'react';
import 'react-toastify/dist/ReactToastify.css';
import Button from 'react-bootstrap/Button'
import Container from "react-bootstrap/Container";
import Config from "../../config";
import { STATUS } from '../../Enums'

function RCStreamer() {

    const [ready, setReady] = useState(false);

    useEffect(() => {
        fetch(Config.HOST + '/status/rc-streamer', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
        }).then(response => {
            return response.json();
        }).then(data => {
            if(data.status === STATUS.READY){
                setReady(true);
            }
            console.log(data.status)
        })
    }, []);

    if(ready){
        return (
            <Container>
                <Button variant="primary" size="lg" onClick={() => {start(); setReady(false);}}>
                    Start
                </Button>
            </Container>
        );
    } else {
        return (
            <Container>
                <Button variant="primary" size="lg" disabled={true}>
                    Running ...
                </Button>
            </Container>
        );
    }
}

function start(){
    fetch(Config.HOST + '/exec/rc-streamer/run', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({

        })
    }).then(response => {
        return response.json();
    });
}


export default RCStreamer;