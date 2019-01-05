/**
 * Created by Saghar on 12/24/18.
 */
import { Form, Text } from 'react-form';
import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';

export default class InvitedPeople extends Component {

    constructor( props ) {
        super( props );
        this.state = {};
    }

    render() {
        return (
            <div>
                <Form
                    onSubmit={submittedValues => this.setState( { submittedValues } )}>
                    { formApi => (
                        <div>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={() => formApi.addValue('participants', '')}
                                type="button"
                                className="mb-4 mr-4 btn btn-success">Add Participant</Button>
                            <form onSubmit={formApi.submitForm} id="dynamic-form">
                                { formApi.values.participants && formApi.values.participants.map( ( participant, i ) => (
                                    <div key={`participant${i}`}>
                                        <label htmlFor={`participant-name-${i}`}></label>
                                        <TextField label="participant" field={['participant', i]} id={`participant-name-${i}`} />
                                        <IconButton aria-label="Delete"
                                                    onClick={() => formApi.removeValue('participants', i)}
                                                    type="button"
                                                    className="mb-4 btn btn-danger">
                                            <DeleteIcon fontSize="small" />
                                        </IconButton>
                                    </div>
                                ))}
                                <Button variant="contained" color="secondary" type="submit" className="mb-4 btn btn-primary">Confirm Participants</Button>
                            </form>
                        </div>
                    )}
                </Form>
            </div>
        );
    }
}