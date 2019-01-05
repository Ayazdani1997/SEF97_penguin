/**
 * Created by Saghar on 12/24/18.
 */
/**
 * Created by Saghar on 12/24/18.
 */
/**
 * Created by Saghar on 4/7/18.
 */
import React, { Component } from 'react';
import ButtonAppBar from "../Features/ButtonAppBar"
import UserPolls from "../Features/CenteredGrid"
import withStyles from '@material-ui/core/styles/withStyles';
import styled from 'styled-components';
import img from '../bg.png';



const request = require('superagent');
const styles = theme => ({
    main: {
    }
});



class Polls extends Component {

    constructor(props) {
        super(props);
        this.state={user:{
            name:"Saghar Talebipour",
            email:"saghar.talebipoor@gmail.com"}
        };
        this.getLoggedInUser();
    }

    getLoggedInUser(){
        var user = {
            name:"Saghar Talebipour",
            email:"saghar.talebipoor@gmail.com"
        }

        this.setState({
            user:user
        });
    }

    render(){
        return (
            <div>
                <ButtonAppBar user={this.state.user}/>
                <UserPolls user={this.state.user}/>
            </div>
        );
    }
}

export default  withStyles(styles)(Polls);
