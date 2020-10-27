import React from "react";
import Container from 'react-bootstrap/Container';
import Jumbotron from 'react-bootstrap/Jumbotron'
import Button from 'react-bootstrap/Button'
import {saveAs} from "file-saver";
import Request from "../../Requests";

function Backup() {

    return (
        <Container>
            <Jumbotron>
                <h1>Download DB</h1>
                <p>
                    Download a copy of the current database.
                </p>
                <p>
                    <Button variant="primary" onClick={() => {download()}}>Download</Button>
                </p>
            </Jumbotron>

            <Jumbotron>
                <h1>Copy DB</h1>
                <p>
                    Copy a copy of the current database to the backup folder.
                </p>
                <p>
                    <Button variant="primary" onClick={() => {copy()}}>Copy</Button>
                </p>
            </Jumbotron>
        </Container>
    );
}

function download(){
    Request.GET_JSON('/download_db').then(data => {
        const filename = data['filename'];
        Request.GET_FILE('/download_db').then(blob => {
            saveAs(blob, filename);
        });
    });
}

function copy() {
    Request.POST_JSON('/updater/exchanges', {}).then(() => {

    });
}


export default Backup;