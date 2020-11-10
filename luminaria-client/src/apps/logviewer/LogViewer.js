import React, {useRef, useState} from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import './LogViewer.css'
import Request from "../../Requests";
import Jumbotron from "react-bootstrap/Jumbotron";


function LogViewer() {

    const [logs, setLogs] = useState('');
    const scrollRef = useRef(null);

    window.scrollTo(0, 0)

    function onClick() {
        getLogs().then(lines => {
            setLogs(lines);
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        });
    }

    return (
        <Container id='log-viewer'>
            <Jumbotron>
                <h1>Logviewer</h1>
                <br />
                <Button onClick={onClick} variant="info">Tail 100</Button>
                <br/> <br/> <br/>
                <Form className={'shadow-sm'}>
                    <Form.Group>
                        <Form.Label>Log.txt</Form.Label>
                        <Form.Control ref={scrollRef} as="textarea" rows="16" readOnly={true} value={logs}/>
                    </Form.Group>
                </Form>
                </Jumbotron>
        </Container>
    );
}

async function getLogs() {
    return await Request.POST_JSON('/log-viewer/tail', {numLines: 100}).then(data => {
        return data.lines;
    });
}


export default LogViewer;