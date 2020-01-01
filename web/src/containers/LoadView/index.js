import React,{Component} from "react";
import {css} from "aphrodite";
import { d, w, h, ai, jc } from "../../styles/themes";
import CircularProgress from "../../component/CircularProgress";
class LoadingView extends Component{
    render() {
        const {size} = this.props
        return (
            <div className={css(d.flex, w.w_100, h.h_100, ai.c, jc.c)}>
                <CircularProgress size={200}/>
            </div>
        )
    }
}

export default LoadingView; 