import React,{Component} from "react";
import {css} from "aphrodite";
import {connect} from "react-redux";
import RecentPost from "../../component/RecentPost";
import { d, bc, pos, w, h, fle, fled, ff, fw, fs, clr, text, pad, m, linh, jc, flew, b } from "../../styles/themes";

class Footer extends Component{
    render(){
        return (
            <div className={css(d.flex, bc.dim_black, pos.relative, w.w_100, fled.c, pos.relative)}
            >
                <div className={css(d.flex,m.elg )}>
                    <div className={css(d.flex, fle.flex_1, fled.c, m.md)}>
                        <div className={css( ff.Roboto, fw.w700, fs.emd, clr.white, text.u, linh.h1_5)}>
                            Nhantai.org
                        </div>
                        <div className={css( ff.Roboto, fs.sm, clr.white_smoke, m.mg_t_md, linh.h1_25)}>
                            Trang thông tin tin tức về chính sách thu hút, đào tạo, đãi ngộ nhân tài.
                        </div>
                        <div className={css(d.flex,m.mg_t_md)}>
                            <div className={css(clr.white, m.mg_r_md,)}>
                                <i className="fa fa-facebook-square" style={{fontSize:24,}}/>
                            </div>
                            <div className={css(clr.white, m.mg_r_md)}>
                                <i className="fa fa-twitter" style={{fontSize:24}}></i>
                            </div>
                        </div>
                    </div>
                    <div className={css(d.flex, fle.flex_1, m.md, fled.c)}>
                        <div className={css( ff.Roboto, fw.w700, fs.esm, clr.white, text.u, linh.h1_5, m.mg_l_md)}>
                            Recent Posts
                        </div>
                        <RecentPost noPost={2} type="footer"/>
                    </div>
                    <div className={css(d.flex, fle.flex_1, m.md, fled.c)}>
                        <div className={css( ff.Roboto, fw.w700, fs.esm, clr.white, text.u, linh.h1_5, m.mg_l_md)}>
                            Tags
                        </div>
                        <div className={css(d.flex, flew.w, fled.r, m.mg_t_sm)}>
                            <div className={css(b.br_45, bc.light_gray, linh.h1_5, pad.sm, m.sm)}> 
                                Việt Nam
                            </div>
                            <div className={css(b.br_45, bc.light_gray, linh.h1_5, pad.sm, m.sm)}> 
                                Hà Nội
                            </div>
                            <div className={css(b.br_45, bc.light_gray, linh.h1_5, pad.sm, m.sm)}> 
                                Chính sách
                            </div>
                            <div className={css(b.br_45, bc.light_gray, linh.h1_5, pad.sm, m.sm)}> 
                                Lương
                            </div>
                            <div className={css(b.br_45, bc.light_gray, linh.h1_5, pad.sm, m.sm)}> 
                                Thành phố Hồ Chí Minh
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

const mapStateToProps = state =>({
    posts: state.loadPost.posts
})

export default connect(mapStateToProps,null)(Footer);