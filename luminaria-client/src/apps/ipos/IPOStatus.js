import React, {useEffect, useState} from 'react';
import Button from 'react-bootstrap/Button'
import Container from "react-bootstrap/Container";
import Form from 'react-bootstrap/Form'
import Jumbotron from "react-bootstrap/Jumbotron";
import Table from 'react-bootstrap/Table'
import {STATUS} from "../../Enums";
import Request from "../../Requests";

function IPOStatus() {

    const [ready, setReady] = useState(null);
    const [strings, setStrings] = useState([]);
    const [company, setCompany] = useState("");
    const [sites, setSites] = useState([]);

    useEffect(() => {
        Request.STATUS('/ipo-listener').then(data => {
            if(data['status'] === STATUS.READY || data['status'] === STATUS.STOPPED){
                setReady(true);
            } else {
                setReady(false);
            }
        });
        refresh();
    }, []);

    let button;
    if(ready === null) {
        return (
            <Container/>
        );
    }
    if(ready){
        button = <Button variant="primary" size="lg" onClick={() => {start(); setReady(false);}}>
            Start
        </Button>
    } else {
        button = <Button variant="primary" size="lg" disabled={true}>
            Running ...
        </Button>
    }

    let i = 1;
    let j = 1;
    const rowsAnnounced = [];
    const rowsWaiting = [];
    const links = [];

    strings.map((s) => {

        if(s['found'] === 1) {
            rowsAnnounced.push(
                <tr key={s.id}>
                    <td>{i++}</td>
                    <td>{s['string']}</td>
                    <td>{s['found_date'].substring(0, 16)}</td>
                    <td>
                        <Button variant="secondary" onClick={() => {
                            dismiss(s['string']);
                        }}>
                            X
                        </Button>
                    </td>
                </tr>
            )
        } else {
            rowsWaiting.push(
                <tr key={s.id}>
                    <td>{j++}</td>
                    <td>{s['string']}</td>
                    <td>
                        <Button variant="secondary" onClick={() => {
                            remove(s['string']);
                        }}>
                            X
                        </Button>
                    </td>
                </tr>
            )
        }
        return 1;
    });

    sites.map((site) => {
        const match = /[.](.*?)[.]/g.exec(site);
        links.push(
            <div key={site}>
                <a href={site} target='_blank' rel='noopener noreferrer'>Link to {match[1]} calendar</a>
                <br/>
            </div>
        )
        return 1;
    });

    const handleSubmit = (evt) => {
        const string = company.trim();
        if(string !== ''){
            Request.EXEC('/ipo-listener/add', {string: string}).then(() => {
                refresh();
            });
        }
        setCompany('');
        evt.preventDefault();
    }

    return (
        <Container>
            <Jumbotron>
                <h1>IPO Status</h1> {button}
                <br />

                <br />
                {links}
                <br />

                <Form inline onSubmit={handleSubmit}>
                    <Form.Control
                        className='mb-2 mr-sm-2'
                        placeholder='Company Name'
                        value={company}
                        onChange={e => setCompany(e.target.value)}
                    />
                    <Button type='submit' className='mb-2' variant='info'>Add String</Button>
                </Form>
            </Jumbotron>

            <Table striped bordered hover>
                <thead>
                    <tr>
                        <th colSpan='4'>IPO Date Set</th>
                    </tr>
                    <tr>
                        <th>#</th>
                        <th>String</th>
                        <th>Announced Date</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {rowsAnnounced}
                </tbody>
            </Table>
            <br/>
            <Table striped bordered hover>
                <thead>
                <tr>
                    <th colSpan='3'>Waiting for IPO Date</th>
                </tr>
                <tr>
                    <th>#</th>
                    <th>String</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {rowsWaiting}
                </tbody>
            </Table>
        </Container>
    );

    function refresh(){
        Request.EXEC('/ipo-listener/data', {}).then(data => {
            setStrings(data['res']);
            setSites(data['sites']);
        });
    }

    function remove(string){
        Request.EXEC('/ipo-listener/remove', {string: string}).then(() => {
            refresh();
        });
    }

    function dismiss(string){
        Request.EXEC('/ipo-listener/dismiss', {string: string}).then(() => {
            refresh();
        });
    }
}

function start(){
    Request.EXEC('/ipo-listener/run', {}).then(() => {});
}


export default IPOStatus;