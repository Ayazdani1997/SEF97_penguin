/**
 * Created by Saghar on 12/24/18.
 */


import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import VoteDialog from "./VoteDialog";

const styles = {
    card: {
        margin : 10,
        minWidth: 275,
    },
    bullet: {
        display: 'inline-block',
        margin: '0 2px',
        transform: 'scale(0.8)',
    },
    title: {
        fontSize: 14,
    },
    pos: {
        marginBottom: 12,
    },
    vote:{
        width:1200,
    }
};

function InvitedPoll(props) {
    const { classes } = props;
    const bull = <span className={classes.bullet}>•</span>;

    return (
        <Card className={classes.card}>
            <CardContent>
                <Typography classname={classes.pos} variant="h5" component="h2">
                    {props.poll.name}
                </Typography>
                <Typography className={classes.pos} color="textSecondary">
                    {props.poll.description}
                </Typography>
            </CardContent>
            <CardActions>
                <VoteDialog style={{width:2000}}/>
            </CardActions>
        </Card>
    );
}

InvitedPoll.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(InvitedPoll);
