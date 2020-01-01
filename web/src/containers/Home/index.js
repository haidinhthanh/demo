import React,{Component} from 'react'
import { w, d, fled, h, zi, pad, bc, pos , bgu, m, fle, ff, fw, lets, clr, text, ai, jc, fs, linh, hov, opa, bg, b, flew, texd, lst, fil} from "../../styles/themes"
import {css, StyleSheet} from "aphrodite";
import {images as img, images_v2 as img2} from "../../assets/images";
import HostPostItem from "../../component/HostPostItem";
import SideContent from "../../component/SideContent";
import PaginationPost from "../../component/PaginationPost";
import { connect } from "react-redux";
import {loadPagePost, changeWebStas} from "../../store/actions/post";
import { Link} from "react-router-dom";
import axios from "axios";
import {server, api } from "../../assets/constant";
import LoadView from "../LoadView";

class Home extends Component{
    componentDidMount(){
        const {loadPagePosts} = this.props
        var url = server.url + api.getPopularPosts(10,0)
        axios.get(url)
        .then(res => {
            const pagePosts = res.data.data;
            loadPagePosts({
                pagePosts: pagePosts
            })
        })
        .catch(error => console.log(error));
        changeWebStas({
            isFirstOpen: true
        })
    }
    render(){
        const {popularPosts} = this.props;
        
        console.log("dinh thanh hai 2",this.props.isFirstOpen)
        var isRend = false
        if(popularPosts.length>0){
            isRend = true
        }
        if (isRend){
        var src = popularPosts[0]._source
        return(
            <div className={css(d.flex, w.w_100, fled.c,)}>
                <div className={css(d.flex,w.w_100, h.bg_img,)}
                >
                    <div className={css(d.flex, fled.r, w.w_100)}>
                        <div class={css(d.flex, fle.flex_2,)}>
                            <div className={ css(d.flex, fled.c, fle.flex_1, ai.fs, jc.fe, zi.zi1,)}>   
                                <img src={img.cate_bg} className={css(pos.absolute, w.w_100, h.bg_img, zi.zi_1, fil.b50)} style={{objectFit:"cover"}}></img>
                                <div className={css(d.flex, fled.c, w.w_100, h.h_100, m.lg, jc.fe)}>
                                    <Link to={"/category/" + src.processor_category_classify} 
                                        className={css(ff.Roboto, fw.w500, fs.sm, clr.white, lets.sm, text.u, texd.none, hov.dis_underline)
                                    }>
                                        {src.processor_category_classify}
                                    </Link>
                                    <Link 
                                        to={"/view_post/" + popularPosts[0]._id}
                                        className={css(ff.IBM, fw.w700, fs.elg, clr.white, lets._esm, linh.h1_25, text.n, hov.trans_color_dgray,texd.none, m.mg_t_md)}
                                    >
                                        {src.title}
                                    </Link>
                                    <div className={css(ff.Roboto, fw.w500, lets._esm, clr.white_smoke, text.u, fs.esm, m.mg_t_lg)}>
                                        {src.published_date.replace("T", " ")}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class={css(d.flex,m.lg, fle.flex_1,)}>
                            <div className={css(fle.flex_1,bg.black_op07,zi.zi2,pad.lg,)}>
                                <div className={css(zi.zi3, d.flex, fled.c,w.w_100,bc.trans,)}>
                                    <div className={css(ff.Roboto, fs.lg, fw.w700, lets._sm,zi.zi3,clr.white , m.mg_b_md)}>What's Hot</div>
                                    {
                                        popularPosts.slice(0,3).map((item,index)=>{
                                            const src = item._source;
                                            return(
                                                <HostPostItem
                                                    imageUrl={src.images && src.images.length?src.images[0]:img.post_img} title={src.title} datePublished={src.published_date} key={index} item={item} level={1}
                                                />
                                            )
                                        })
                                    }
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className={css(d.flex, w.w_100, fled.r)}>
                    <div className={css(d.flex, fled.c, w.w_70,  pad.lg, bc.white_smoke)}>
                        <div className={css(d.flex, fled.c, ai.c)}>
                            <div className={css(ff.IBM, fw.w700, fs.lg, linh.h1_5)}>
                                Popular Posts
                            </div>
                            <div className={css(ff.IBM, fw.w400, fs.sm, linh.h1_5, clr.gray)}> 
                                Don't miss to check out our most popular posts
                            </div>
                        </div>
                        <PaginationPost level={1}/>
                    </div>
                    <div className={css(d.flex, fled.c, w.w_30, bc.white_smoke, pad.lg)}>
                        <SideContent/>
                    </div>
                </div>
            </div>
        );   
    }
    else{
        return (
            <div className={css(d.flex, w.w_100,h.h_100, pad.elg, pos.absolute, zi.zi3, bc.white)}>
                <LoadView size={200}></LoadView>
            </div>
            )
    }
    }
}

const mapStateToProps = state =>({
    posts: state.loadPost.posts,
    popularPosts: state.pagePost.pagePosts,
    isFirstOpen: state.web.isFirstOpen,
})

const mapDispatchToProps = (dispatch) => {
    return {
        loadPagePosts: (payload)=>{
            dispatch(loadPagePost(payload))
        },
        changeWebStas: (payload)=>{
            dispatch(changeWebStas(payload))
        }
    }
}
export default connect(mapStateToProps,mapDispatchToProps)(Home);