import React,{Component} from "react";
import { clr, d, h, w, fle, fled, bc, ai, jc, ff, fw, linh, fs, opa, pos, flew, zi, fil, pad } from "../../styles/themes";
import { css } from "aphrodite";
import {images_v2} from "../../assets/images";
import {connect} from "react-redux";
import SideContent from "../../component/SideContent";
import PaginationPost from "../../component/PaginationPost";
class Feature extends Component{
    componentDidMount() {
    }

    render() {
        const {feature} =this.props.match.params
        const {posts} = this.props
        let featurePosts = posts.filter((item,index)=>{
            if (item._source.process_talent_info[feature].length>0){
                return item;
            }
        })
        console.log(featurePosts)
        return (
            <div className={css(d.flex,w.w_100, fled.c, flew.w, pos.relative,) } >
                <div className={css(d.flex,h.lg, w.w_100, h.elg, ai.c, jc.c)}>
                    <img src={images_v2.loc_bg} className={css(pos.absolute, w.w_100, h.elg, zi.zi1,)} style={{objectFit:"cover"}}></img>
                    <div className={css(d.flex, ff.IBM, fw.w700, linh.h1_25, clr.white, fs.lg,zi.zi3)}>
                            Feature:{feature}
                    </div>
                </div>
                <div className={css(d.flex, w.w_100, fled.r)}>
                    <div className={css(d.flex, fled.c, fle.flex_2,  pad.lg, bc.white_smoke)}>
                        <PaginationPost posts={featurePosts} level={2}/>
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

export default connect(mapStateToProps, null)(Feature);