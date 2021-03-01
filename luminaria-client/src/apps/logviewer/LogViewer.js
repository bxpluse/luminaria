import React, {useEffect, useRef, useState} from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import './LogViewer.css'
import Request from "../../Requests";
import Jumbotron from "react-bootstrap/Jumbotron";
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

function LogViewer(props) {

    const [logs, setLogs] = useState('');
    const [checkedApps, setCheckedApps] = useState({});
    const [selectedLogLevel, setSelectedLogLevel] = useState(2);
    const scrollRef = useRef(null);

    useEffect(() => {
        window.scrollTo(0, 0)
    }, []);

    function onClick() {
        // Find logs for wanted apps
        const appsToSearch = [];
        for (const [, app] of Object.entries(props.apps)) {
            const is_link = app['link_to'] !== null;
            if(!is_link){
                if(!(app.id in checkedApps) || (checkedApps[app.id] === true)){
                    appsToSearch.push(app.id);
                }
            }
        }
        if(!('FLASK' in checkedApps) || (checkedApps['FLASK'] === true)){
            appsToSearch.push('Flask');
        }

        getLogs(appsToSearch, selectedLogLevel).then(lines => {
            setLogs(lines);
            scrollRef.current.scrollIntoView({ behavior: 'smooth' });
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        });
    }

    const handleChange = (event) => {
        setCheckedApps({...checkedApps, [event.target.name] : event.target.checked });
    }

    const handleLogLevelChange = (event) => {
        setSelectedLogLevel(parseInt(event.target.value));
    }

    const checkboxes = [];
    checkboxes.push(
        <Form.Check key="FLASK" className="ml-3" type="checkbox" defaultChecked={true} name="FLASK"
                    label="FLASK" onChange={handleChange}/>
    )
    for(let i = 0; i < props.apps.length; i++){
        const app = props.apps[i];
        const is_link = app['link_to'] !== null;
        if(!is_link){
            checkboxes.push(
                <Form.Check key={app.id} className="ml-3" type="checkbox" name={app.id} defaultChecked={true}
                            label={app.name} onChange={handleChange}/>
            )
        }
    }

    return (
        <Container id='log-viewer'>
            <Jumbotron>
                <h1>Logviewer</h1>
                <br />

                <Container>
                    <Row>
                        {checkboxes}
                    </Row>
                    <br />
                    <Form.Group  as={Row}>
                        <Form.Label column>
                            Log Level >=
                        </Form.Label>
                        <Col>
                            <Form.Control as="select" defaultValue={2} onChange={handleLogLevelChange}>
                                <option value={5}>5 (FATAL)</option>
                                <option value={4}>4 (ERROR)</option>
                                <option value={3}>3 (WARN)</option>
                                <option value={2}>2 (INFO)</option>
                                <option value={1}>1 (DEBUG)</option>
                            </Form.Control>
                        </Col>
                    </Form.Group>
                </Container>

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

async function getLogs(appsToSearch, selectedLogLevel) {
    const levels = [];
    for(let i = selectedLogLevel; i <= 5; i++){
        levels.push(i);
    }
    const body = {numLines: 100, apps: appsToSearch, levels: levels};
    return await Request.POST_JSON('/exec/log-viewer/tail', body).then(data => {
        return data.lines;
    });
}


export default LogViewer;