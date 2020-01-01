import React,{ Component} from "react";
import {connect} from "react-redux";
import { w, d, fled, h, m, fle, ff, fw, clr, jc, fs, linh, hov, texd, bc,} from "../../styles/themes"
import {css, StyleSheet} from "aphrodite";
import {Link} from "react-router-dom";
import {images} from "../../assets/images"
import df from "./post_img.jpg"
import axios from "axios";
import {server, api} from "../../assets/constant";
import {loadRecentPost,} from "../../store/actions/post";
class RecentPost extends Component{
    componentDidMount(){
        const {loadRecentPost} = this.props
        var url = server.url + api.getRecentPost
        axios.get(url)
        .then(res => {
            const recentPosts = res.data.data;
            loadRecentPost({
                recentPosts: recentPosts
            })
        })
        .catch(error => console.log(error));
    }

    render() {
        const {recentPosts, noPost, type} = this.props
        return (
            <div className={css(d.flex, fled.c,)}>
                {
                    recentPosts.slice(0,noPost).map((item,index)=>{
                    const src = item._source;
                    if (type == "content"){
                        return (
                            <div className={css(d.flex, m.sm)} key={index}>
                                <img src={src.images && src.images.length?src.images[0]: df} className={css(w.lg,h.lg, m.sm, fle.flex_1)} style={{objectFit:"fill"}}></img>
                                <div className={css(d.flex, fled.c, m.sm, jc.sb, fle.flex_2)}>
                                    <Link 
                                        to={"/view_post/" + item._id}
                                        className={css(ff.IBM, fw.w700, fs.esm, linh.h1_25, hov.trans_color_dgray, clr.black, texd.none)}
                                    >
                                        {src.title}
                                    </Link>
                                    <div className={css(ff.IBM, fs.esm, linh.h1_25, clr.dim_gray)}>
                                        {src.published_date.replace("T", " ")}
                                    </div>
                                </div>
                            </div>
                        )
                    }
                    else if( type == "footer"){
                        return (
                            <div className={css(d.flex, m.sm)} key={index}>
                                <img src={src.images && src.images.length?src.images[0]: df} className={css(w.lg,h.lg, m.sm, fle.flex_1)} style={{objectFit:"fill"}}></img>
                                <div className={css(d.flex, fled.c, m.sm, jc.sb, fle.flex_2)}>
                                    <Link 
                                        to={"/view_post/" + item._id}
                                        className={css(ff.IBM, fw.w700, fs.esm, linh.h1_25, clr.white, texd.none, hov.trans_color_)}
                                    >
                                        {src.title}
                                    </Link>
                                    <div className={css(ff.IBM, fs.esm, linh.h1_25, clr.dim_gray)}>
                                        {src.published_date.replace("T", " ")}
                                    </div>
                                </div>
                            </div>
                        )
                    }
                    else{
                        return (
                            <div className={css(d.flex, m.sm)}>
                                <img src={src.images && src.images.length?src.images[0]:images.post_img} className={css(w.lg,h.lg, m.sm)} style={{objectFit:"fill"}}></img>
                                <div className={css(d.flex, fled.c, m.sm, jc.sb)}>
                                    <div className={css(ff.IBM, fw.w700, fs.esm, linh.h1_25)}>
                                        {src.title}
                                    </div>
                                    <div className={css(ff.IBM, fs.esm, linh.h1_25, clr.dim_gray)}>
                                        {src.published_date.replace("T", " ")}
                                    </div>
                                </div>
                            </div>
                        )
                    }
                     
                })
                }
            </div>
        )
    }
}

const mapStateToProps = state =>({
    recentPosts : state.recentPost.recentPosts,
})

const mapDispatchToProps = (dispatch) => {
    return {
        loadRecentPost: (payload)=>{
            dispatch(loadRecentPost(payload))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RecentPost)