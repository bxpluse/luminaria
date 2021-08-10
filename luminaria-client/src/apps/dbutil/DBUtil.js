import {saveAs} from 'file-saver';
import React from 'react';
import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container';
import Jumbotron from 'react-bootstrap/Jumbotron'
import Request from '../../Requests';
import StringUtil from '../../util/StringUtil';


function DBUtil() {

    window.scrollTo(0, 0)

    return (
        <Container>
            <DownloadJumbo dbName='config'/>
            <DownloadJumbo dbName='dynamic'/>
        </Container>
    );
}


function DownloadJumbo(props) {

    return (
        <Container>
            <Jumbotron>
                <h1>Download {StringUtil.capitalize(props.dbName)} DB</h1>
                <p>
                    Download a copy of the {props.dbName} database.
                </p>
                <p>
                    <Button variant="primary" onClick={() => {download(props.dbName)}}>Download</Button>
                </p>
            </Jumbotron>
        </Container>
    );
}

function download(dbName){
    Request.POST_JSON('/exec/dbutil/file-name', {dbName: dbName}).then(data => {
        const filename = data['filename'];
        Request.GET_FILE('/blob/dbutil/download',{dbName: dbName}).then(blob => {
            saveAs(blob, filename);
        });
    });
}


export default DBUtil;