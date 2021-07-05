import React, {useEffect, useState} from 'react';
import Card from "react-bootstrap/Card";
import Container from "react-bootstrap/Container";
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
    const rule = props.rule;
    const jobs = [];

    for (let i = 0; i < rule['jobs'].length; i++) {
        const job = rule['jobs'][i];
        jobs.push(<Card.Text>
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

    return (
        <Card style={{ width: '24rem' }}>
            <Card.Body>
                <Card.Title>{rule['name']}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">Running: {rule['is_running']}</Card.Subtitle>
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


export default Signal;