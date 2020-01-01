import React,{Component} from "react";
import {css} from "aphrodite";
import { d, pos, w, h, zi, bc } from "../../styles/themes";
class SearchView extends Component{
    render() {
        return (
            <div className={css(d.flex, pos.fixed,w.w_100, h.h_100, zi.zi3, bc.red)}>

            </div>
        )
    }
}

export default SearchView;