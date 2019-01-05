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
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import FolderIcon from '@material-ui/icons/Folder';
import DeleteIcon from '@material-ui/icons/Delete';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';


const styles = theme => ({
    root: {
        flexGrow: 1,
        maxWidth: 752,
    },
    demo: {
        backgroundColor: theme.palette.background.paper,
    },
    title: {
        margin: `${theme.spacing.unit * 4}px 0 ${theme.spacing.unit * 2}px`,
    },
});

const options=[{
    id:"1234567",
    text:"Thursday afternoon at 18"
},{
    id:"7654321",
    text:"Friday morning at 9"
}
]


export default class VoteDialog extends React.Component {
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
                    vote
                </Button>
                <Dialog
                    open={this.state.open}
                    onClose={this.handleClose}
                    aria-labelledby="form-dialog-title"
                    style={{width:2000}}
                    fullWidth
                >
                    <DialogTitle id="form-dialog-title">vote</DialogTitle>
                    <DialogContent>
                        <List>
                            {options.map(opt => (
                                <ListItem>
                                    <ListItemText
                                        primary={opt.text}
                                    />
                                    <ListItemSecondaryAction>
                                        <Button variant="contained" color="primary" onClick={this.handleClickOpen}>
                                            Yes
                                        </Button>
                                        <Button variant="contained" color="secondary" onClick={this.handleClickOpen}>
                                            No
                                        </Button>
                                    </ListItemSecondaryAction>
                                </ListItem>
                            ))}


                        </List>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Submit Vote
                        </Button>
                    </DialogActions>

                </Dialog>
            </div>
        );
    }
}