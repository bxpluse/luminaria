import React, {useEffect, useState} from 'react';
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
import Switch from "react-switch";
import Request from "../../Requests";

function Signal() {

    const [rules, setRules] = useState([]);

    useEffect(() => {
        post().then(rules => {
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
            {ruleCards}
        </Container>
    );
}

function RuleCard(props) {

    const [isRunning, setIsRunning] = useState(true);
    const rule = props.rule;
    const jobs = [];

    for (let i = 0; i < rule['jobs'].length; i++) {
        const job = rule['jobs'][i];
        jobs.push(<Card.Text key={i}>
            Job {i}:
            <br/>&nbsp;&nbsp;&nbsp;&nbsp; Name: {job['name']}
            <br/>&nbsp;&nbsp;&nbsp;&nbsp; Func: {job['func']}
            <br/>&nbsp;&nbsp;&nbsp;&nbsp; Triggers:
            <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Day of Week: {job['triggers']['day_of_week']}
            <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Hour: {job['triggers']['hour']}
            <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Minute: {job['triggers']['minute']}
            <br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Second: {job['triggers']['second']}
        </Card.Text>)
    }

    useEffect(() => {
        setIsRunning(rule['is_running']);
    }, [rule]);

    function handleChange(checked) {
        setIsRunning(checked);
        updateRunStatus(rule['id'], checked);
    }

    return (
        <Card style={{ width: '24rem' }}>
            <Card.Body>
                <Card.Title>{rule['name']}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">
                <span>{isRunning ? 'Running' : 'Suppressed'}</span>
                <Switch onChange={handleChange} checked={isRunning}
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
                </Card.Subtitle>
                <Card.Text>
                    {rule['description']}
                </Card.Text>
                <Card.Text>
                    Sub-rules: {rule['rule_names']}
                </Card.Text>
                {jobs}
            </Card.Body>
        </Card>
    );
}

async function post() {
    return await Request.POST_JSON('/exec/signal/getAllRules', {}).then(data => {
        return data.rules;
    });
}

async function updateRunStatus(id, isRunning) {
    return await Request.POST_JSON('/exec/signal/updateRuleRunning', {'id': id, 'isRunning': isRunning})
}


export default Signal;