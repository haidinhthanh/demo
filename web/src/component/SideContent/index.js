import React, {Component} from "react";
import { w, d, fled, h, zi, pad, bc, m, ff, fw, ai, jc, fs, linh, b, } from "../../styles/themes"
import {css, StyleSheet} from "aphrodite";
import RecentPost from "../../component/RecentPost";
class SideContent extends Component{
    render() {
        return (
            <div className={css(d.flex,fled.c, bc.white_smoke)}>
                <div className={css(d.flex, fled.c, bc.white, pad.md)}>
                    <div className={css(ff.IBM, fw.w700, linh.h1_25, fs.emd, m.md,)}>Social Link</div>
                    <div className={css(d.flex, fled.r,)}>
                        <a className={css(d.flex,bc.white_smoke, h.md, w.md, b.br50, ai.c, jc.c, m.sm)}><i className="fa fa-facebook-square" style={{fontSize:24}}/></a>
                        <a className={css(d.flex,bc.white_smoke, h.md, w.md, b.br50, ai.c, jc.c, m.sm)}><i className="fa fa-twitter" style={{fontSize:24}}/></a>
                    </div>
                </div>
                <div className={css(d.flex, fled.c, bc.white, pad.md, m.mg_t_lg)}>
                    <div className={css(ff.IBM, fw.w700, linh.h1_25, fs.emd, m.sm)}>Recent Posts</div>
                    <div className={css(d.flex, fled.c,)}>
                        <RecentPost  noPost={10} type="content"/>
                    </div>
                </div>
            </div>
        )
    }
}

export default SideContent;