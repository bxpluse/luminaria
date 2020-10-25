import React from 'react';
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Config from "../../config"
import './LogViewer.css'

class LogViewer extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            logs: ''
        }
        this.textLog = React.createRef();
        this.getLogs = this.getLogs.bind(this);
    }


    getLogs() {

        fetch(Config.HOST + '/log-viewer/tail', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                numLines: 100
            })
        }).then(response => {
            return response.json();
        }).then(data => {
            this.setState({
                logs: data.lines
            });
        })
    }

    componentDidMount() {
        window.scrollTo(0, 0)
    }

    render() {
        return (
            <Container id='log-viewer'>
                <Button onClick={this.getLogs} variant="info">Tail 100</Button>
                <br/> <br/> <br/>
                <Form className={'shadow-sm'}>
                    <Form.Group>
                        <Form.Label>Log.txt</Form.Label>
                        <Form.Control as="textarea" rows="16" ref={this.textLog} readOnly={true} value={this.state.logs}/>
                    </Form.Group>
                </Form>
            </Container>
        );
    }
}


export default LogViewer;