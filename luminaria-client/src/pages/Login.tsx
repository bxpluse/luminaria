import * as React from 'react';
import {useState} from 'react';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import MyButton from '../components/MyButton';
import AppUtil from '../util/AppUtil';


function Login() {

    const [sessionId, setSessionId] = useState(localStorage.getItem('sessionId') || '');

    function setSession(sessionId: string) {
        setSessionId(sessionId);
        localStorage.setItem('sessionId', sessionId);
    }

    return (
        <Container>
            <Form>
                <Form.Group>
                    <Form.Label>Session ID</Form.Label>
                    <Form.Control type='text' value={sessionId} onChange={e => setSession(e.target.value)}/>
                </Form.Group>
                <br/>
                <MyButton text='Return' onClick={() => AppUtil.goTo('/')}/>
            </Form>
        </Container>
    )
}


export default Login;