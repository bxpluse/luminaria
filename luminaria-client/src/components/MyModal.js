import React from "react";
import Modal from 'react-bootstrap/Modal'
import './Custom.css'

function MyModal(props) {
    return (
        <Modal show={props.show} onHide={props.onHide} centered>
            <Modal.Header closeButton>
                <Modal.Title>{props.title}</Modal.Title>
            </Modal.Header>
            <Modal.Body>{props.body}</Modal.Body>
        </Modal>
    );
}

export default MyModal;