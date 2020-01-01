import React,{Component} from "react";
import { clr, d, h, w, fle, fled, bc, ai, jc, ff, fw, linh, fs, opa, pos, flew, zi, fil, pad } from "../../styles/themes";
import { css } from "aphrodite";
import {images_v2} from "../../assets/images";
import {connect} from "react-redux";
import SideContent from "../../component/SideContent";
import PaginationPost from "../../component/PaginationPost";
class Category extends Component{
    componentDidMount() {
    }
    render() {
        const {category} =this.props.match.params
        const {posts} = this.props
        const catePosts = posts.filter((item, index)=>{
            const src = item._source;
            if (src.processor_category_classify == category)
                return item;
            else {
                return
            }
        })
        return (
            <div className={css(d.flex,w.w_100, fled.c, flew.w, pos.relative,) } >
                <div className={css(d.flex,h.lg, w.w_100, h.elg, ai.c, jc.c)}>
                    <img src={images_v2.cate_bg} className={css(pos.absolute, w.w_100, h.elg, zi.zi1, fil.b50)} style={{objectFit:"cover"}}></img>
                    <div className={css(d.flex, ff.IBM, fw.w700, linh.h1_25, clr.white, fs.lg,zi.zi3)}>
                        Category:{category}
                    </div>
                </div>
                <div className={css(d.flex, w.w_100, fled.r)}>
                    <div className={css(d.flex, fled.c, fle.flex_2,  pad.lg, bc.white_smoke)}>
                        <PaginationPost posts={catePosts} level={2}/>
                    </div>
                    <div className={css(d.flex, fled.c, fle.flex_1, bc.white_smoke, pad.lg)}>
                        <SideContent/>
                    </div>
                </div>
            </div>
        )
    }
}
const mapStateToProps = state =>({
    posts: state.loadPost.posts,
})

export default connect(mapStateToProps, null)(Category);