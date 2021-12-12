import React from 'react';
import {Col} from 'react-bootstrap';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';

function FormGroup(props) {
    return (
        <React.Fragment>
            <Form.Group as={props.row !== undefined ? undefined : Col}>
                <Form.Label>{props.label}</Form.Label>
                <InputGroup>
                    {props.prepend !== undefined ?
                        <InputGroup.Prepend>
                            <InputGroup.Text>{props.prepend}</InputGroup.Text>
                        </InputGroup.Prepend> : null
                    }
                    {props.as === 'textarea' ?
                        <Form.Control as="textarea" rows={props.rows}
                                      style={props.disabled ? {backgroundColor: 'white'} : undefined}
                                      disabled={props.disabled}
                                      value={props.value ? props.value : undefined}
                                      onChange={props.func ? e => props.func(e.target.value) : null}
                        />
                        :
                        <Form.Control type={props.type}
                                      style={props.disabled ? {backgroundColor: 'white'} : undefined}
                                      disabled={props.disabled}
                                      placeholder={props.placeholder}
                                      value={props.value ? props.value : ''}
                                      onChange={props.func ? e => props.func(e.target.value) : null}
                        />
                    }
                </InputGroup>
            </Form.Group>
        </React.Fragment>
    );
}

export default FormGroup;