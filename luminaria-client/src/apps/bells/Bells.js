import React, {useEffect, useState} from 'react';
import {Col} from 'react-bootstrap';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Jumbotron from 'react-bootstrap/Jumbotron';
import DismissButton from '../../components/DismissButton';
import FormGroup from '../../components/FormGroup';
import MyButton from '../../components/MyButton';
import Request from '../../Requests';
import Validator from '../../util/Validator';


function Bells() {

    const [rule, setRule] = useState();

    useEffect(() => {
        getAlerts(0);
    }, []);

    function getAlerts(timeout) {
        setTimeout(function () {
                Request.EXEC('/bells/get-alerts', {}).then(res => {
                    setRule(res['rule']);
                });
            }, timeout
        );
    }

    function dismiss(subruleName) {
        Request.EXEC('/bells/remove-alert', {subruleName: subruleName}).then(() => getAlerts(100));
    }

    function saveAlert(symbol, below, above, daysToCancel) {
        save(symbol, below, above, daysToCancel).then(() => getAlerts(100))
    }

    return (
        <Container>
            <h2>Divine Bells</h2>
            <CreateAlertForm saveAlert={saveAlert}/>
            <Alerts rule={rule} dismiss={dismiss}/>
        </Container>
    );
}


function CreateAlertForm(props) {
    const [symbol, setSymbol] = useState('');
    const [below, setBelow] = useState('0');
    const [above, setAbove] = useState('1000000');
    const [daysToCancel, setDaysToCancel] = useState(7);

    return (
        <Jumbotron>
            <h4>Create Alert</h4>
            <Form.Row>
                <Form.Group as={Col}>
                    <Form.Label>Action</Form.Label>
                    <Form.Control value={daysToCancel} as='select'
                                  onChange={e => setDaysToCancel(e.target.value)}
                    >
                        <option value={1}>1 Day</option>
                        <option value={2}>2 Day</option>
                        <option value={3}>3 Day</option>
                        <option value={4}>4 Day</option>
                        <option value={5}>5 Day</option>
                        <option value={7}>7 Day</option>
                        <option value={10}>10 Day</option>
                    </Form.Control>
                </Form.Group>
                <FormGroup label='Symbol' value={symbol} func={setSymbol}/>
                <FormGroup label='Below' value={below} func={setBelow} prepend={'$'}/>
                <FormGroup label='Above' value={above} func={setAbove} prepend={'$'}/>
            </Form.Row>
            <MyButton text='Save' onClick={() => props.saveAlert(symbol, below, above, daysToCancel)}/>
        </Jumbotron>
    )
}

function Alerts(props) {
    const rule = props.rule;
    if (!rule) {
        return null;
    }

    const subrules = rule['jobs'].map((subrule, idx) => {
        return (
            <div key={idx}>
                <Alert subrule={subrule} dismiss={props.dismiss}/>
                <br/>
            </div>
        )
    }) ?? [];

    return (
        <Jumbotron>
            <h4>Alerts</h4>
            <p>Description: {rule['description']}</p>
            <p>Alarmable: {rule['alarmable'].toString()}</p>
            <p>Suppressed: {rule['suppressed'].toString()}</p>
            {subrules}
        </Jumbotron>
    );
}

function Alert(props) {
    const subrule = props.subrule;
    const subruleName = subrule['name'];
    return (
        <Card key={subruleName} className={subrule['expired'] && 'expired'}>
            <Card.Body>
                <Card.Title>
                    <span>Symbol: {subruleName}</span>
                    <DismissButton onClick={() => props.dismiss(subruleName)}/>
                </Card.Title>
                <Card.Text>Above: {subrule['metadata']['above']}</Card.Text>
                <Card.Text>Below: {subrule['metadata']['below']}</Card.Text>
            </Card.Body>
        </Card>
    )
}

async function save(symbol, below, above, daysToCancel) {
    Validator.validateNonEmptyString(symbol);
    Validator.validatePositiveFloat(below);
    Validator.validatePositiveFloat(above);
    Validator.validatePositiveInt(daysToCancel);
    const body = {symbol: symbol, below: below, above: above, daysToCancel: daysToCancel};
    Request.EXEC('/bells/create-alert', body).then();
}


export default Bells;