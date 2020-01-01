import React,{Component} from "react";
import {css} from "aphrodite";
import { pos, h, w, bc, zi, d, fled, jc, ff, fw, fs, text, lets, m, ai, clr, pad, b, lst, linh, ovfl } from "../../styles/themes";
import Close from "@material-ui/icons/Close";
import {connect} from "react-redux";
import SideBarItem from "../SideBarItem";
import { ocSideBar } from "../../store/actions/sidebar";
import {loadPost} from "../../store/actions/post";
import {server, api} from "../../assets/constant";
import axios from "axios";
class SideBar extends Component{
    constructor(props){
        super(props)
        this.state = {
            cate:[
                {
                    name: "Category",
                    stas: 0,
                    lstItem: {}
                },
                // {
                //     name: "Location",
                //     stas: 0,
                //     lstItem: null
                // },
                {
                    name: "Feature",
                    stas: 0,
                    lstItem: {}
                },
                {
                    name: "Location",
                    stas: 0,
                    lstItem: {}
                },
            ]
        }
    }
    componentDidMount(){
        this.getAllPost()
    }
    
    onChangeStas = (key) => {
        var newState = this.state.cate.slice()
        newState[key].stas = !newState[key].stas
        this.setState({cate : newState})
    }

    getCateogoryObject = ()=>{
        let cateObject = {}
        console.log("cate", this.props.posts)
        this.props.posts.map((item,index)=>{
            const src = item._source;
            if(src.processor_category_classify in cateObject){
                cateObject[src.processor_category_classify] += 1
            }
            else{
                cateObject[src.processor_category_classify] = 1
            }
        })
        return cateObject
    }
    getPolicyObject = ()=>{
        let policyObject = {
            "Regime":0,
            "Salary": 0,
            "Environment": 0,
        }
        console.log("policy", this.props.posts)
        this.props.posts.map((item,index)=>{
            const src = item._source;
            let keys = Object.keys(src.process_talent_info)
            for (let i in keys){
                if(src.process_talent_info[keys[i]].length){
                    policyObject[keys[i]] += 1
                }
            }
        })
        return policyObject
    } 

    getAllPost=()=>{
        const {loadPost} = this.props
        var url = server.url + api.getAllPost
        axios.get(url)
        .then(res => {
            const posts = res.data.data;
            loadPost({
                posts: posts
            })
        })
        .then(res=>{
            var newState = this.state.cate.slice()
            newState[0].lstItem = this.getCateogoryObject()
            newState[1].lstItem = this.getPolicyObject()
            this.setState({cate : newState})
            console.log("get post", this.props.posts)
        })
        .catch(error => console.log(error));
    } 
    render(){
        const {cate} = this.state
        const {stas, onClose, posts} = this.props
        // this.getAllPost()
        if(stas){
            return(
                <div className={css(pos.absolute, pos.t0,)}>
                <div className={css(d.flex,pos.fixed, zi.zi3, h.h_100, w.w_25, d.flex, fled.c, bc.white, ovfl.y_auto )}>
                    <div className={css(d.flex, fled.r, jc.sb, ai.c, h.md, pad.p_lr_md, pad.p_tb_esm, b.b_b_l)}>
                        <div className={css(ff.IBM, fw.w700, fs.md, lets.esm)}> Nhân tài</div>
                        <Close 
                            style={{fontSize:20, color: "#808080"}} 
                            onClick={()=>{
                                onClose({isOpen: false})
                            }}
                        />
                    </div>
                    <div className={css( d.flex, h.h_100, m.mg_l_lg, m.mg_r_lg)}>
                        <ul className={css(d.flex, fled.c,lst.none, w.w_100, pad.p0)}>
                        {
                            cate.map((item, index)=>{
                                return(<SideBarItem cateItem={item} key={index} onChangeStas={this.onChangeStas} id={index}/>)
                            })
                        }
                        </ul>
                    </div>
                </div>
                </div>
            )
        }
        else{
            return (<div/>)
        }
    }
}


const mapStateToProps = state =>({
    posts: state.loadPost.posts,
    stas: state.sideBar.isOpen,
})

const mapDispatchToProps = (dispatch) => {
    return {
      onClose: (payload) => {
        dispatch(ocSideBar(payload))
      },
      loadPost: (payload)=>{
        dispatch(loadPost(payload))
    }
    }
}

export default connect(mapStateToProps,mapDispatchToProps)(SideBar);