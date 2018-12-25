/**
 * Created by Saghar on 12/24/18.
 */
import React from 'react';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import AddIcon from '@material-ui/icons/Add';
import Options from './Options'
import InvitedPeople from './InvitedPeople'

export default class FormDialog extends React.Component {
    state = {
        open: false,
    };

    handleClickOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    render($) {
        return (
            <div>
                <Button variant="contained" color="secondary" onClick={this.handleClickOpen}>
                    <AddIcon />
                    Create New Poll
                </Button>
                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="form-dialog-title"
                >
                    <DialogTitle id="form-dialog-title">Create New Poll</DialogTitle>
                    <DialogContent>
                        <TextField
                            autoFocus
                            margin="dense"
                            id="name"
                            label="Poll Name"
                            type="string"
                            fullWidth
                        />
                        <TextField
                            autoFocus
                            margin="dense"
                            id="name"
                            label="Poll Description"
                            type="string"
                            fullWidth
                        />
                        <Options/>
                        <InvitedPeople/>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Cancel
                        </Button>
                        <Button onClick={this.handleClose} color="primary">
                            Create Poll
                        </Button>
                    </DialogActions>

                </Dialog>
            </div>
        );
    }
}