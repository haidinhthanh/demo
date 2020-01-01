import React,{Component} from "react";
import { clr, d, h, w, fle, fled, bc, ai, jc, ff, fw, linh, fs, opa, pos, flew, zi, fil, pad } from "../../styles/themes";
import { css } from "aphrodite";
import {images_v2} from "../../assets/images";
import {connect} from "react-redux";
import {cities, nations, provinces} from "../../assets/location_data";
import SideContent from "../../component/SideContent";
import PaginationPost from "../../component/PaginationPost";
class Location extends Component{
    componentDidMount() {
    }

    render() {
        const {location} =this.props.match.params
        const {posts} = this.props
        let locPosts = []
        if( location == "Viet Nam"){
            locPosts = posts.filter((item, index)=>{
                if("Việt Nam" in item._source.processor_ner_loc.nations 
                    || item._source.processor_ner_loc.provinces.length>0
                    || item._source.processor_ner_loc.cities.length>0
                ){
                    return item;
                }
            })
        }
        else if( location == "World"){
            locPosts = posts.filter((item, index)=>{
                if( item._source.processor_ner_loc.nations.length> 2
                    || (item._source.processor_ner_loc.nations.length == 1 &&  item._source.processor_ner_loc.nations[0] != "Việt Nam")
                ){
                    return item;
                }
            })
        }
        return (
            <div className={css(d.flex,w.w_100, fled.c, flew.w, pos.relative,) } >
                <div className={css(d.flex,h.lg, w.w_100, h.elg, ai.c, jc.c)}>
                    <img src={images_v2.loc_bg} className={css(pos.absolute, w.w_100, h.elg, zi.zi1,)} style={{objectFit:"cover"}}></img>
                    <div className={css(d.flex, ff.IBM, fw.w700, linh.h1_25, clr.white, fs.lg,zi.zi3)}>
                        Location:{location}
                    </div>
                </div>
                <div className={css(d.flex, w.w_100, fled.r)}>
                    <div className={css(d.flex, fled.c, fle.flex_2,  pad.lg, bc.white_smoke)}>
                        <PaginationPost posts={locPosts} level={2}/>
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

export default connect(mapStateToProps, null)(Location);