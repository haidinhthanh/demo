import React,{Component} from "react";
import { flo, m, clr, texd, hov, d, pos, pad, bef, bc, lst, h, w, ai, jc, fw, b, zi, cus, fled, ff, fs} 
    from "../../styles/themes";
import { css } from "aphrodite";
import {Link} from "react-router-dom";

const style_ul_ul_li = css(
    d.flex,
    m.mg_l_lg,
    pos.relative,
    clr.white,
)
const style_li_link = css(
    d.flex,
    clr.white,
    texd.none,
    h.sm,
    pad.sm,
    w.elg,
    ai.c,
    ff.Roboto,
    fw.w700,
    hov.trans_color_dgray
)
const style_cav= css(
    cus.arrow_up,
    bc.trans,
    pos.absolute,
    pos.b0,
)

class DropDownItem extends Component{
    constructor(props){
        super(props)
    }

    render(){
        const {cate, stas, itemLst, onChangeStas, id} = this.props
        return(
            <li 
                className={css(d.flex,ai.fs,fled.c,w.header_width,m.mg_l_sm,m.mg_r_sm,)}         
            >   
                {
                    (cate != "Analystic")?(
                    <div 
                        className={css(d.flex,clr.black,texd.none,hov.trans_color_blue,fs.sm,fw.w700,h.h_100,w.w_100,jc.c,ai.c, )}
                        onMouseEnter={()=>{
                            onChangeStas(id, true)}}
                        onMouseLeave={()=>{
                            onChangeStas(id, false)}}
                    >
                        {cate}
                        <div className={itemLst.length && stas? style_cav: css(d.none)}/> 
                    </div>):
                    (
                    <Link 
                        to="/chart"
                        className={css(d.flex,clr.black,texd.none,hov.trans_color_blue,fs.sm,fw.w700,h.h_100,w.w_100,jc.c,ai.c, )}
                        onMouseEnter={()=>{
                            onChangeStas(id, true)}}
                        onMouseLeave={()=>{
                            onChangeStas(id, false)}}
                    >
                        {cate}
                        <div className={itemLst.length && stas? style_cav: css(d.none)}/> 
                    </Link>)

                }   
                <ul className={stas? css(d.flex, fled.c, pos.absolute, pos.t_100, pad.p0, bc.black, lst.none, zi.zi2,): 
                                    css(d.none)}
                    onMouseEnter={()=>{
                        onChangeStas(id,true)}}
                    onMouseLeave={()=>{
                        onChangeStas(id,false)}} 
                >
                    {itemLst.map((item,index)=>{
                        return (
                            <li className={style_ul_ul_li} key={index}>
                                <Link 
                                    className={style_li_link}
                                    to={"/"+cate.toLowerCase()+"/"+ item.title}
                                >
                                    {item.title}
                                </Link>
                            </li>
                        )
                    })}
                </ul>
            </li>
        )
    }
}

export default DropDownItem