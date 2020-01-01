import React,{Component} from "react";
import Header from "../Header";
import Routes from "../../routes";
import SideBar from "../../component/SideBar";
import Footer from "../../containers/Footer";
import {BrowserRouter} from "react-router-dom";
import { Provider } from "react-redux";
import store from "../../store";
import {css} from "aphrodite";
import { d, fled, w, ovfl } from "../../styles/themes";
class App extends Component{
    render(){
        return(
            <Provider store={store} >
                <BrowserRouter>
                    <div className={css(d.flex, fled.c, w.w_100,)}
                    >
                        <Header/>
                        <Routes/>
                        <Footer/>
                        <SideBar/>
                    </div>
                </BrowserRouter>
            </Provider>
        )
    }
}

export default App