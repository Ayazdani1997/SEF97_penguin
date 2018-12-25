/**
 * Created by Saghar on 12/24/18.
 */
/**
 * Created by Saghar on 4/7/18.
 */
import React, { Component } from 'react';
import SignIn from "../Features/SignIn"
import withStyles from '@material-ui/core/styles/withStyles';
import styled from 'styled-components';
import img from '../bg.png';



const request = require('superagent');
const styles = theme => ({
    main: {
    }
});

class LoginPage extends Component {
    render(){
        return (
            <div className="main">
                <SignIn/>
            </div>
        );
    }
}

export default  withStyles(styles)(LoginPage);
