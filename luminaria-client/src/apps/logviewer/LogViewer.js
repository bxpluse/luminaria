import React, {useEffect, useRef, useState} from 'react';
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Jumbotron from "react-bootstrap/Jumbotron";
import Row from 'react-bootstrap/Row'
import Tab from 'react-bootstrap/Tab'
import Table from 'react-bootstrap/Table'
import Tabs from 'react-bootstrap/Tabs'
import MyButton from "../../components/MyButton";
import Request from "../../Requests";
import './LogViewer.css'

function LogViewer(props) {
    return (
            <Container id='log-viewer'>
                <Tabs defaultActiveKey="Logs">
                    <Tab eventKey="Logs" title="Logs">
                        <LogTab apps={props.apps}/>
                    </Tab>
                    <Tab eventKey="Jobs" title="Jobs">
                        <JobTab apps={props.apps}/>
                    </Tab>
                </Tabs>
            </Container>
    );
}


function LogTab(props) {

    const MAX_APPS = 50;
    const [nextToggle, setNextToggle] = useState(false);
    const [logs, setLogs] = useState('');
    const [checkedState, setCheckedState] = useState(
        new Array(MAX_APPS).fill(true)
    );
    const apps = ['Flask'];
    const links = new Set();

    const [selectedLogLevel, setSelectedLogLevel] = useState(2);
    const scrollRef = useRef(null);

    useEffect(() => {
        window.scrollTo(0, 0)
    }, []);

    function onClick() {
        // Find logs for wanted apps
        const appsToSearch = new Set();
        for (let i = 0; i < checkedState.length; i++) {
            if (checkedState[i] && !links.has(i) && checkedState[i] !== undefined) {
                appsToSearch.add(apps[i]);
            }
        }
        if (appsToSearch.size === 0) {
            setLogs('');
        } else {
            getLogs(Array.from(appsToSearch), selectedLogLevel).then(lines => {
                setLogs(lines);
                scrollRef.current.scrollIntoView({ behavior: 'smooth' });
                scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
            });
        }
    }

    function onToggle() {
        setCheckedState(new Array(MAX_APPS).fill(nextToggle));
        setNextToggle(!nextToggle);
    }

    const handleOnChange = (position) => {
        const updatedCheckedState = checkedState.map((item, index) =>
            index === position ? !item : item
        );
        setCheckedState(updatedCheckedState);
    };

    const handleLogLevelChange = (event) => {
        setSelectedLogLevel(parseInt(event.target.value));
    }

    const checkboxes = [];
    checkboxes.push(
        <Form.Check key="FLASK" className="ml-3" type="checkbox" name="FLASK"
                    label="FLASK" checked={checkedState[0]} onChange={() => handleOnChange(0)}/>
    )
    for(let i = 0; i < props.apps.length; i++){
        const app = props.apps[i];
        const is_link = app.url.includes('https');
        const stateIdx = i + 1;
        apps.push(app.id);
        if(!is_link){
            checkboxes.push(
                <Form.Check key={app.id} className="ml-3" type="checkbox" name={app.id}
                            label={app.name} checked={checkedState[stateIdx]} onChange={() => handleOnChange(stateIdx)}/>
            )
        } else {
            links.add(stateIdx);
        }
    }

    return (
        <Jumbotron>
            <h3>Logviewer</h3>
            <br />
            <Container>
                <MyButton text='Toggle' variant='secondary' onClick={() => onToggle()}/>
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
    );
}

function JobTab() {

    const [executedJobs, setExecutedJobs] = useState([]);

    function onClick() {
        getJobs().then(lines => {
            setExecutedJobs(lines);
        })
    }

    const rows = [];

    for (let i = 0; i < executedJobs.length; i++) {
        const executedJob = executedJobs[i];
        rows.push(
            <tr>
                <td>{executedJob['name']}</td>
                <td>{executedJob['app_id']}</td>
                <td>{executedJob['func']}</td>
                <td>{executedJob['triggers']}</td>
                <td>{executedJob['response']}</td>
                <td>{executedJob['datetime_created']}</td>
            </tr>
        )
    }

    return (
        <Jumbotron>
            <h3>Jobs</h3>
            <br />
            <Button onClick={onClick} variant="info">Tail 100</Button>
            <br/> <br/> <br/>

            {executedJobs.length !== 0 ?
                <Table striped bordered hover>
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Id</th>
                        <th>Func</th>
                        <th>Triggers</th>
                        <th>Response</th>
                        <th>Datetime</th>
                    </tr>
                    </thead>
                    <tbody>
                    {rows}
                    </tbody>
                </Table> : <></>
            }
        </Jumbotron>
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

async function getJobs() {
    return await Request.POST_JSON('/exec/log-viewer/tailJob', {}).then(data => {
        return data.lines;
    });
}


export default LogViewer;