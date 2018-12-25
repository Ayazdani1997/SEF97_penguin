import { Form, Text } from 'react-form';
import React, { Component } from 'react';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';
import IconButton from '@material-ui/core/IconButton';
import TextField from '@material-ui/core/TextField';


export default class Options extends Component {

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
                                onClick={() => formApi.addValue('options', '')}
                                type="button"
                                className="mb-4 mr-4 btn btn-success">Add Option</Button>
                            <form onSubmit={formApi.submitForm} id="dynamic-form">
                                { formApi.values.options && formApi.values.options.map( ( option, i ) => (
                                    <div key={`option${i}`}>
                                        <label htmlFor={`option-name-${i}`}></label>
                                        <TextField label="option" field={['options', i]} id={`option-name-${i}`} />
                                        <IconButton aria-label="Delete"
                                                    onClick={() => formApi.removeValue('options', i)}
                                                    type="button"
                                                    className="mb-4 btn btn-danger">
                                            <DeleteIcon fontSize="small" />
                                        </IconButton>
                                    </div>
                                ))}
                                <Button  variant="contained" color="secondary" type="submit" className="mb-4 btn btn-primary">Confirm Options</Button>
                            </form>
                        </div>
                    )}
                </Form>
            </div>
        );
    }
}