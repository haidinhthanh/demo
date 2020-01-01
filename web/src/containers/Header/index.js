import React,{Component} from "react";
import {css, StyleSheet} from "aphrodite";
import {d, w, bc, vi, tsi, tsf, fled, pos} 
from "../../styles/themes";
import NavBar from "../../component/NavBar";
import HeaderMenu from "../../component/HeaderMenu";


class Header extends Component{
    constructor(props){
        super(props)
        this.state={
            show: true,
            scrollPos: 0,
        }
    }
    render(){
        return(
                <div className={css(d.flex,w.w_100, fled.c,)}>
                        <NavBar/>
                        <HeaderMenu/>
                </div>
        )
    }
}
export default Header;