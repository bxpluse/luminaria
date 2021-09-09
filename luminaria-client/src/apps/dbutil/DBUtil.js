import {saveAs} from 'file-saver';
import React, {useEffect, useState} from 'react';
import {Tabs} from 'react-bootstrap';
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form'
import Jumbotron from 'react-bootstrap/Jumbotron'
import Tab from 'react-bootstrap/Tab';
import Table from 'react-bootstrap/Table';
import MyButton from '../../components/MyButton';
import Request from '../../Requests';
import StringUtil from '../../util/StringUtil';


function DBUtil() {

    window.scrollTo(0, 0)

    return (
        <Container>
            <Tabs>
                <Tab key={1} eventKey='download' title='Download'>
                    <DownloadJumbo dbName='config'/>
                    <DownloadJumbo dbName='dynamic'/>
                </Tab>
                <Tab key={2} eventKey='editor' title='KO Editor'>
                    <KOEditor/>
                </Tab>
            </Tabs>
        </Container>
    );
}

function KOEditor() {

    const [rows, setRows] = useState([]);

    useEffect(() => {
        Request.GET_JSON('/get/dbutil/fetch-all-ko-md').then(res => {
            setRows(res['metadatas']);
        });
    }, []);

    const tableRows = rows.map(row => {
        return (
            <KORow key={row['key']} row={row}/>
        )
    }) ?? [];

    return (
        <Table striped bordered hover>
            <colgroup>
                <col style={{width: '20%'}}/>
                <col style={{width: '75%'}}/>
                <col style={{width: '5%'}}/>
            </colgroup>
            <thead>
            <tr>
                <th>KO Key</th>
                <th>Metadata</th>
                <th>Action</th>
            </tr>
            </thead>
            <tbody>
            {tableRows}
            </tbody>
        </Table>
    );
}

function KORow(props) {

    const row = props.row;

    const [metadata, setMetadata] = useState(JSON.stringify(row['metadata']));
    const [readOnly, setReadOnly] = useState(true);

    function modify() {
        if (readOnly) {
            setReadOnly(false);
        } else {
            const body = {key: row['key'], value: metadata};
            Request.POST_JSON('/exec/dbutil/put-ko-md', body).then(res => {
                if (res.success) {
                    setReadOnly(true);
                }
            });
        }
    }

    return (
        <tr key={row['key']}>
            <td>{row['key']}</td>
            <td>
                <Form.Control type='text' value={metadata}
                              onChange={e => setMetadata(e.target.value)} readOnly={readOnly}
                />
            </td>
            <td>
                <MyButton text='+' onClick={() => modify()}/>
            </td>
        </tr>
    );
}


function DownloadJumbo(props) {

    return (
        <Jumbotron>
            <h1>Download {StringUtil.capitalize(props.dbName)} DB</h1>
            <p>
                Download a copy of the {props.dbName} database.
            </p>
            <p>
                <Button variant='primary' onClick={() => {
                    download(props.dbName)
                }}>Download</Button>
            </p>
        </Jumbotron>
    );
}

function download(dbName) {
    Request.POST_JSON('/exec/dbutil/file-name', {dbName: dbName}).then(data => {
        const filename = data['filename'];
        Request.GET_FILE('/blob/dbutil/download', {dbName: dbName}).then(blob => {
            saveAs(blob, filename);
        });
    });
}


export default DBUtil;