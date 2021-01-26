import React from "react";
import Container from 'react-bootstrap/Container';
import Jumbotron from 'react-bootstrap/Jumbotron'
import Button from 'react-bootstrap/Button'
import {saveAs} from "file-saver";
import Request from "../../Requests";

function Backup() {

    window.scrollTo(0, 0)

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
                <h1>Copy DB (Disabled)</h1>
                <p>
                    Copy a copy of the current database to the backup folder.
                </p>
                <p>
                    <Button variant="primary" disabled="true" onClick={() => {copy()}}>Copy</Button>
                </p>
            </Jumbotron>
        </Container>
    );
}

function download(){
    Request.GET_JSON('/get/db-backup/file-name').then(data => {
        const filename = data['filename'];
        Request.GET_FILE('/blob/db-backup/download').then(blob => {
            saveAs(blob, filename);
        });
    });
}

function copy() {

}


export default Backup;