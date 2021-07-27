import React from "react";
import Modal from 'react-bootstrap/Modal'
import './Custom.css'


function MyModal(props) {
    let modalClass = '';
    if (props.wide) {
        modalClass = 'modal-75w';
    }
    return (
        <Modal dialogClassName={modalClass} show={props.show} onHide={props.onHide} centered>
            <Modal.Header closeButton>
                <Modal.Title>{props.title}</Modal.Title>
            </Modal.Header>
            {props.body !== undefined ? <Modal.Body>{props.body}</Modal.Body> : null}
            {props.component !== undefined ? <>{props.component}</> : null}
        </Modal>
    );
}


export default MyModal;