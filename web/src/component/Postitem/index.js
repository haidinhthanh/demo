import React,{Component} from "react";
import {css} from "aphrodite";
import {w, d, fled, h,  bc,  m, ff, fw, lets, clr, text,fs, linh, hov,texd, fle, jc, ai } from "../../styles/themes";
import {Link} from "react-router-dom";
import {images as img, images_v2 as img2} from "../../assets/images";
import EqualizerIcon from '@material-ui/icons/Equalizer';
class PostItem extends Component{
    
    extract15WordSentence = (content)=>{
        var sentences = content.split(" ")
        var new_content = ""
        for (let step = 0; step < 20; step++) {
            new_content = new_content.concat(sentences[step] + " ")
          }
        return new_content.concat(" ...")
    }

    render() {
        const {level} = this.props
        const {_id, no_view} = this.props.item
        const {processor_category_classify, title, published_date, content, images} = this.props.item._source
        
        const new_content = this.extract15WordSentence(content)
        return (
            <div className={css(d.flex, fled.c, m.lg, w.w_40, bc.white,)}>
                <img 
                    src={images && images.length? images[0]: ( level == 1 ? img.post_img: img2.post_img)} 
                    className={css(w.w_100,h.elg)} 
                    style={{objectFit:"fill"}}
                />
                <div class={css(d.flex, m.lg, fled.c)}>
                    <Link 
                        to={"/category/" + processor_category_classify}
                        className={css(ff.Roboto, fw.w500, lets._esm, clr.dodger_blue, text.u, fs.sm, m.mg_t_sm, texd.none, hov.dis_underline)}
                    >
                        {processor_category_classify}
                    </Link>
                    <Link 
                        to={"/view_post/" + _id}
                        className={css(ff.IBM, fs.emd, fw.w700, lets._esm, linh.h1_25, clr.black, hov.trans_color_lgray, m.mg_t_sm, texd.none)}
                    >
                        {title}
                    </Link>
                    <div className={css(d.flex, ai.c,)}>
                        <div className={css(ff.Roboto, fs.esm, fw.w400, linh.h1_5, clr.dim_gray,  m.mg_t_sm)}> 
                            {published_date.replace("T", " ")}
                        </div>
                        <div className={css(m.mg_l_md)}>
                            <EqualizerIcon style={{width: 36, height:36, color: "#696969"}}></EqualizerIcon>
                        </div>
                        <div className={css(ff.Roboto, fs.esm, fw.w400, linh.h1_5, clr.dim_gray,  m.mg_t_sm,)}> 
                            {no_view} views
                        </div>
                    </div>
                    <div className={css(ff.Roboto, fs.esm, fw.w400, linh.h1_5, clr.dim_gray,  m.mg_t_sm)}>
                        {new_content}
                    </div>
                    <div className={css( m.mg_t_sm,)}>
                        <Link 
                            className={css(d.flex, fled.r,ff.Roboto, fs.esm, fw.w600, lets.esm,clr.black,texd.none, hov.trans_color_blue, text.u,  m.mg_t_sm, m.mg_r_,)}
                            to={"/view_post/" + _id}
                        >
                            Read more
                            <div className={css(m.mg_l_sm, hov.trans_color_blue)}>
                                <i className="fa fa-long-arrow-right"></i>
                            </div>
                        </Link>
                    </div>
                </div>
            </div>
        )
    }
}

export default PostItem;