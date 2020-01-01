import React,{Component} from "react";
import {css} from "aphrodite";
import { pos, h, w, bc, zi, d, fled, jc, ff, fw, fs, text, lets, m, ai, clr, pad, b, lst, linh, texd, hov } from "../../styles/themes";
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import ArrowDropUpIcon from '@material-ui/icons/ArrowDropUp';
import {Link} from "react-router-dom";

class SideBarItem extends Component{
    render(){
        const {cateItem, id, onChangeStas} = this.props
        return(
            <li className={css(d.flex, fled.c,lst.none, w.w_100,fs.md, ff.IBM, fw.w700, lets._esm, linh.h1_5, )}
            >
                <div className={css(d.flex, jc.sb)}>
                    {cateItem.name} 
                <span onClick={()=>{
                    onChangeStas(id)
                }}>{cateItem.stas? <ArrowDropUpIcon/> : <ArrowDropDownIcon/>}</span>
                </div>
                    {   
                        cateItem.stas?
                        (Object.keys(cateItem.lstItem).map((item,index)=>{
                            if (cateItem.name == "Category"){
                                return(
                                    <ul className={css(d.flex, pad.p0, fled.c, lst.none, m.mg_t_sm)}>
                                        <li className={css(d.flex, fled.r, jc.sb, m.esm,)}>
                                            <Link
                                                to={"/category/" + item} 
                                                className={css(ff.IBM, fw.w500, fs.sm, clr.black, texd.none, hov.trans_color_lgray)}
                                            >
                                                {item}
                                            </Link>
                                            <span className={css(bc.light_gray, b.br50,pad.p_lr_esm, fs.sm, fw.w500)}> 
                                                {cateItem.lstItem[item]}
                                            </span>
                                        </li>
                                    </ul>
                                )
                            }
                            else if(cateItem.name == "Feature"){
                                return(
                                    <ul className={css(d.flex, pad.p0, fled.c, lst.none, m.mg_t_sm)}>
                                        <li className={css(d.flex, fled.r, jc.sb, ff.IBM, fw.w500, fs.sm, m.esm,)}>
                                            <Link
                                                to={"/feature/"+ item}
                                                className={css(ff.IBM, fw.w500, fs.sm, clr.black, texd.none, hov.trans_color_lgray)}
                                            >
                                                {item}
                                            </Link>
                                            <span className={css(bc.light_gray, b.br50, d.flex,pad.p_lr_esm)}> 
                                                {cateItem.lstItem[item]}
                                            </span>
                                        </li>
                                    </ul>
                                )
                            }
                            else{
                                return null;
                            }
                        })): null
                    }
            </li> 
        )
    }
}

export default SideBarItem;