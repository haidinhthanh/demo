import React from 'react'
import {Route, Switch} from 'react-router-dom'
import Home from "../containers/Home"
import About from "../containers/About"
import Contact from "../containers/Contact"
import Category from "../containers/Category";
import PostView from "../containers/PostView";
import Location from "../containers/Location";
import Feature from "../containers/Feature";
import ChartDashBoard from "../containers/ChartDashBoard";
const Routes = () => {
    
    return(
        <Switch>
            <Route exact path="/" component={Home}/>
            <Route path="/about" component={About}/>
            <Route path="/contact" component={Contact}/>
            <Route path="/category/:category" component={Category}/>
            <Route path="/view_post/:id" component={PostView}/>
            <Route path="/location/:location" component={Location}/>
            <Route path="/feature/:feature" component={Feature}/>
            <Route path="/chart" component={ChartDashBoard}/>
        </Switch>
        )
    }

export default Routes;