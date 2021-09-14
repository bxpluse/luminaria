import React, {useEffect, useState} from 'react';
import {OverlayTrigger, Tooltip} from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Masonry from "react-masonry-css";
import Switch from 'react-switch';
import InfoSymbol from '../../components/InfoSymbol';
import MyModal from '../../components/MyModal';
import Request from "../../Requests";
import JobUtil from "../logviewer/JobUtil";
import './Signal.css'


function Signal() {

    const [rules, setRules] = useState({});

    useEffect(() => {
        fetchRules().then(rules => {
            setRules(rules);
        })
    }, []);

    const ruleCards = [];
    for (let i = 0; i < rules.length; i++) {
        const rule = rules[i];
        ruleCards.push(
            <RuleCard key={rule['id']} rule={rule}/>
        )
    }

    return (
        <Container>
            <Masonry
                breakpointCols={3}
                className='masonry-grid'
                columnClassName='masonry-grid_column masonry-grid-extra-margin'>
                {ruleCards}
            </Masonry>
        </Container>
    );
}

function RuleCard(props) {

    const rule = props.rule;
    const [isAlarmRunning, setIsAlarmRunning] = useState(true);
    const [modalJobs, setModalJobs] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const handleCloseModal = () => setShowModal(false);

    function handleShowModal(name) {
        tailJobsByName(name).then(lines => setModalJobs(lines));
        setShowModal(true);
    }

    const renderTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props}>
            {props['day_of_week'] !== undefined ? <><br/>Day of Week: {props['day_of_week']}</> : null}
            {props['hour'] !== undefined ? <><br/>Hour: {props['hour']}</> : null}
            {props['minute'] !== undefined ? <><br/>Minute: {props['minute']}</> : null}
            {props['second'] !== undefined ? <><br/>Second: {props['second']}</> : null}
        </Tooltip>
    );

    const jobs = [];
    for (let i = 0; i < rule['jobs'].length; i++) {
        const job = rule['jobs'][i];
        jobs.push(<Card.Text key={i}>
            Job {i}:
            <span onClick={() => handleShowModal(job['name'])}>
                <br/>&nbsp;&nbsp;&nbsp;&nbsp; Subrule Name: {job['name']} <InfoSymbol/>
            </span>
            <br/>&nbsp;&nbsp;&nbsp;&nbsp; Func: {job['func']}
            {job['args'] !== null ? <><br/>&nbsp;&nbsp;&nbsp;&nbsp; Args: {job['args']} </> : null}
            <br/>
            <span> &nbsp;&nbsp;
                <OverlayTrigger
                    placement="right"
                    delay={{ show: 250, hide: 400 }}
                    overlay={renderTooltip(job['triggers'])}
                >
                    <Button className='trigger-button' variant='link'>Triggers <InfoSymbol/> </Button>
                </OverlayTrigger>
            </span>
        </Card.Text>)
    }

    useEffect(() => {
        setIsAlarmRunning(!rule['suppressed']);
    }, [rule]);

    function handleChange(checked) {
        setIsAlarmRunning(checked);
        updateRunStatus(rule['id'], checked).then();
    }

    return (
        <Card style={{ width: '24rem' }}>
            <MyModal wide show={showModal} onHide={handleCloseModal} title='Job History'
                     component={JobUtil.convertJobRowsToTable(modalJobs)}
            />
            <Card.Body>
                <Card.Title>{rule['name']}</Card.Title>
                {rule['alarmable'] === true ? <Card.Subtitle className="mb-2 text-muted">
                    <span>{isAlarmRunning ? 'Alarm Running' : 'Alarm Suppressed'} </span>
                    <Switch onChange={handleChange} checked={isAlarmRunning}
                            onColor="#86d3ff"
                            onHandleColor="#2693e6"
                            handleDiameter={30}
                            uncheckedIcon={false}
                            checkedIcon={false}
                            boxShadow="0px 1px 5px rgba(0, 0, 0, 0.6)"
                            activeBoxShadow="0px 0px 1px 10px rgba(0, 0, 0, 0.2)"
                            height={20}
                            width={48}
                            className="react-switch"
                            id="material-switch"
                    />
                </Card.Subtitle> : null}

                <Card.Text>
                    {rule['description']}
                </Card.Text>
                {jobs}
            </Card.Body>
        </Card>
    );
}

async function fetchRules() {
    return await Request.EXEC('/signal/fetch-all-rules', {}).then(data => {
        return data.rules;
    });
}

async function updateRunStatus(id, isAlarmRunning) {
    const suppressed = !isAlarmRunning;
    return await Request.EXEC('/signal/update-rule-suppressed',
        {'id': id, 'suppressed': suppressed}
    )
}

async function tailJobsByName(name) {
    return await Request.EXEC('/log-viewer/tail-jobs', {'name': name})
        .then(data => {
            return data.lines;
        });
}


export default Signal;