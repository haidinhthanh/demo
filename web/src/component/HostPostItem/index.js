import React,{ Component } from "react";
import {css} from "aphrodite";
import {d,fled,w,h,m,fle,ff,fw,fs,clr,lets,linh,text,hov,pad, texd} from "../../styles/themes";
import {Link} from "react-router-dom";
import {images as img, images_v2 as img2} from "../../assets/images";
class HostPostItem extends Component{
    render(){
        const {item , level} = this.props
        const {_id} = item
        const {images,title, published_date } = item._source
        const date = published_date.replace("T", " ")
        return(
            <div className={css(d.flex, fled.r, w.w_100, h.lg,pad.esm, m.mg_b_lg)}>
                <img src={images && images.length? images[0]: ( level == 1 ? img.post_img: img2.post_img)} className={css(w.lg, fle.flex_1)} style={{objectFit:"cover"}}></img>
                <div className={css(d.flex,fled.c,w.w_100,m.mg_l_sm, fle.flex_2)}>
                    <Link 
                        to={"/view_post/" + _id}
                        className={css(ff.IBM, fw.w500, fs.esm, clr.white, linh.h1_25,text.n, hov.trans_color_dgray,m.mg_b_sm, texd.none)}
                    >
                        {title}
                    </Link>
                <div className={css(ff.Roboto,fw.w500,lets._esm,clr.white,text.u,fs.esm)}>{date}</div>
                </div>
            </div>
        )
    }
}
export default  HostPostItem;