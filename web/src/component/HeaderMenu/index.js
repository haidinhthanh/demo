import React, {Component} from "react"
import {css, StyleSheet} from "aphrodite";
import {aft ,d, w, h, m, pad, bc, pos, flew, ai, fs, fw, ff, lets, clr, jc, texa, flo, lst, hov, texd, fled, bef, cus, fle, b, bs, ol, vi, tsi, tsf} 
from "../../styles/themes";
import DropDownItem from "../DropDownItem";
import {connect} from "react-redux";
import {ocSideBar} from "../../store/actions/sidebar";
import {Link} from "react-router-dom";

const style_menu_header = css(
    d.flex,
    h.h_100,
    fled.r,
    ai.c,
    jc.sb
    )
// 
const style_brand =css(d.flex,h.h_100,fs.md, ff.IBM,lets._sm,fw.w700,pad.p_lr_md,ai.c,)
// 
const style_menu_nav = css(
    d.flex,
    fle.flex_2,
    h.h_100,
    texa.c,
)
const style_ul = css(
    d.flex,
    fled.r,
    m.m0,
    pad.p0,
    pos.relative,
    lst.none,
    h.h_100,
)

const style_bt= css(
    bc.trans,
    b.bn,
    bs.n,
    ol.n,
    hov.trans_color_blue,
    m.mg_r_md,
    m.mg_l_md,
)

class HeaderMenu extends Component{
    constructor(props){
        super(props)
        this.state= {
            menu:[
                {   
                    cate: "Location",
                    stas: false,
                    itemLst: [
                        {
                            title: "Viet Nam",
                            link: "#"
                        },
                        {
                            title: "World",
                            link: "#"
                        },
                    ]
                },
                {   
                    cate: "Feature",
                    stas: false,
                    itemLst: [
                        {
                            title: "Salary",
                            link: "#"
                        },
                        {
                            title: "Environment",
                            link: "#"
                        },
                        {
                            title: "Regime",
                            link: "#"
                        },
                    ],
                },
                {   
                    cate: "Analystic",
                    stas: false,
                    itemLst: [
                    ],
                },
            ],
        }
    }

    onChangeStas = (key, isOpen) => {
        const newMenu = this.state.menu.slice()
        newMenu[key].stas = isOpen
        this.setState({menu: newMenu})
    }
    
    render() {
        console.log("1234", "rend headermenu")
        const {menu} = this.state
        const {onOpen, stas} = this.props
        return (
            <div className={css(d.ib, w.w_100, h.lg, bc.white_smoke, b.b_b_l)}>
                <div className={style_menu_header}>
                    <Link className={css(d.flex,h.h_100,fs.md, ff.IBM,lets._sm,fw.w700,pad.p_lr_md,ai.c, clr.black,texd.none)}
                        to="/"
                    >
                        Talent
                    </Link>
                    <nav className={style_menu_nav}>
                            <ul className={style_ul}
                            >
                                {menu.map((item,index)=>(
                                    <DropDownItem id={index} key={index} cate={item.cate} stas={item.stas} itemLst={item.itemLst} onChangeStas={this.onChangeStas}/>
                                ))}
                            </ul>
                    </nav>   
                    <div className={css(d.flex, h.h_100)}>
                        <button className={style_bt}>
                            <i className="fa fa-search" style={{fontSize: 20}}></i>
                        </button>
                        <button className={style_bt} onClick={()=>{onOpen({isOpen: !stas})}}>
                            <i className="fa fa-bars" style={{fontSize: 20}}></i>
                        </button>
                    </div>
                </div>    
            </div>
        )
    }
}

const mapStateToProps = state =>({
    stas: state.sideBar.isOpen,
})
const mapDispatchToProps = (dispatch) => {
    return {
      onOpen: (payload) => {
        dispatch(ocSideBar(payload))
      },
    }
  }

export default connect(mapStateToProps, mapDispatchToProps)(HeaderMenu);