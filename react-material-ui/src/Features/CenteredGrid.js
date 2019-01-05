import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import InvitedPoll from './InvitedPoll'
import CreatedPoll from './CreatedPoll'
const styles = theme => ({
    root: {
        flexGrow: 1,
    },
    paper: {
        padding: theme.spacing.unit * 2,
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
});


function CenteredGrid(props) {
    const { classes } = props;

    const createdPolls =[{
        name:"Nahar",
        description:"Berim Nahar Bokhorim"
    },{
        name:"Sham",
        description:"Berim Sham Bokhorim"
    }
    ]

    const invitedPolls =[{
        name:"Jalase1",
        description:"Berim Jalase1 o Bokhorim"
    },{
        name:"Jalase2",
        description:"Berim Jalase2 o Bokhorim"
    }
    ]

    return (
        <div className={classes.root}>
            <Grid container spacing={24}>
                <Grid item xs={6}>
                    <h1 align="center">Created Polls</h1>
                    {createdPolls.map(createdPoll => (
                        <CreatedPoll poll={createdPoll}/>
                    ))}
                </Grid>
                <Grid item xs={6}>
                    <h1 align="center">Invited Polls</h1>
                    {invitedPolls.map(invitedPoll => (
                        <InvitedPoll poll={invitedPoll}/>
                    ))}
                </Grid>
            </Grid>
        </div>
    );
}

CenteredGrid.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CenteredGrid);