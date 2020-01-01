import React,{Component} from "react";
import {connect} from "react-redux";
import {loadPost} from "../../store/actions/post";
import {css} from "aphrodite";
import { d, fle, fled, w, bc, h, pad, m, ai, jc, lst, mih, b, ff, fw, fs } from "../../styles/themes";
import ChartControl from "../../component/ChartControl";
import PieChart from "../../component/PieChart";
import BarChart from "../../component/BarChart";
import {server, api} from "../../assets/constant";
import axios from "axios";
class ChartDashBoard extends Component{
    constructor(props){
        super(props)
    }
    componentDidMount(){
        const {loadPost} = this.props
        var url = server.url + api.getAllPost
        axios.get(url)
        .then(res => {
            const posts = res.data.data;
            loadPost({
                posts: posts
            })
        })
        .catch(error => console.log(error));
    }
    renderChart = (chartType, aspect, dataOb)=>{
        if(chartType == "Pie Chart"){
            if(aspect == "Content Type"){
                console.log("test", dataOb)
                return (
                    <div className={css(w.w_70,bc.white, pad.sm,)}>
                        <PieChart
                            items={dataOb}
                        />
                    </div>
                )
            }
            else if(aspect == "Feature"){
                return (
                    <div className={css(w.w_70,bc.white, pad.sm)}>
                        <PieChart
                            items={dataOb}
                        />
                    </div>
                )
            }
            else {
                return null;
            }
        }
        else if(chartType == "Bar Chart"){
            if(aspect == "Content Type"){
                return (
                    <div className={css(w.w_70,bc.white, pad.sm,)}>
                        <BarChart items={dataOb}/>
                    </div>
                )
            }
            else if(aspect == "Feature"){
                return (
                    <div className={css(w.w_70,bc.white, pad.sm, )}>
                        <BarChart items={dataOb}/>
                    </div>
                )
            }
            else {
                return null;
            }
        }
    }

    render() {
        const {chartType, aspect, endTime, startTime, startRend, lstBarValue} = this.props
        var rendChart = null
        if(startRend){
            const dataobject = this.getdataChart(chartType, aspect, startTime, endTime, lstBarValue)
            rendChart = this.renderChart(chartType, aspect, dataobject)
        }
        return (
            <div className={css(d.flex, fled.c,bc.white_smoke, pad.lg, mih.mih500)}>
                <div className={css(ff.IBM, fw.w700, fs.lg, d.flex, ai.c, jc.c)}>
                    Statistical Post
                </div>

                <div className={css(d.flex, bc.white, b.br_45, b.b_l)}>
                    <div className={css(d.flex,fle.flex_2,ai.c, jc.c,)}>
                        {   
                            startRend && rendChart
                        }
                    </div>
                    <div className={css(fle.flex_1, b.br_tr_45, b.br_br_45)}>
                        <ChartControl/>
                    </div>
                </div>
            </div>
        )
    }

    getDateRange = (startDate, endDate) => {
        var start      = startDate.split('-');
        var end        = endDate.split('-');
        var startYear  = parseInt(start[0]);
        var endYear    = parseInt(end[0]);
        var dates      = [];
      
        for(var i = startYear; i <= endYear; i++) {
          var endMonth = i != endYear ? 11 : parseInt(end[1]) - 1;
          var startMon = i === startYear ? parseInt(start[1])-1 : 0;
          for(var j = startMon; j <= endMonth; j = j > 12 ? j % 12 || 11 : j+1) {
            var month = j+1;
            var displayMonth = month < 10 ? '0'+month : month;
            dates.push([i, displayMonth, '01'].join('-'));
          }
        }
        return dates;
    }
    getdataChart =(chartType, aspect, startTime, endTime, lstSelect)=>{
        if(chartType=="Pie Chart"){
            if(aspect == "Content Type"){
                return this.getCategoryObject("all", null, null, null)
            }
            else if(aspect == "Feature"){
                return this.getPolicyObject("all", null, null, null)
            }
            else{
                return null
            }
        }
        else if(chartType="Bar Chart"){
            if(aspect == "Content Type"){
                return this.getCategoryObject("time", startTime, endTime, lstSelect)
            }
            else if(aspect == "Feature"){
                return this.getPolicyObject("time", startTime, endTime, lstSelect)
            }
            else{
                return null
            }
        }
    }

    getCategoryObject = (type, startTime, endTime, lstSelect)=>{
        const {posts} = this.props
        var cateObject = {}
        if(type=="all"){
            posts.map((item,index)=>{
                const src = item._source;
                if(src.processor_category_classify in cateObject){
                    cateObject[src.processor_category_classify] += 1
                }
                else{
                    cateObject[src.processor_category_classify] = 1
                }
            })
        }
        else{
            let dateRange = this.getDateRange(this.getDayMonthYear(startTime), this.getDayMonthYear(endTime))
            cateObject["date_range"] = dateRange 
            lstSelect.forEach( element=>{
                cateObject[element] = {}
                dateRange.forEach( date =>{
                    cateObject[element][date] = 0
                })
            })
            posts.map((item,index)=>{   
                const src = item._source;
                let currentTime = new Date(src.published_date)
                if(currentTime >= startTime && currentTime <= endTime){
                    let field = this.getDayMonthYear(currentTime).substring(0,7) + "-01"
                    if(lstSelect.includes(src.processor_category_classify)){
                        cateObject[src.processor_category_classify][field] +=1
                    }
                }
            })
        }
        console.log("1111111111", cateObject)
        return cateObject;
    }
    getPolicyObject = (type, startTime, endTime, lstSelect)=>{
        var policyObject = {}
        const {posts} = this.props
        if(type == "all"){
            policyObject = {
                "Regime":0,
                "Salary": 0,
                "Environment": 0,
            }
            posts.map((item,index)=>{
                const src = item._source;
                let keys = Object.keys(src.process_talent_info)
                for (let i in keys){
                    if(src.process_talent_info[keys[i]].length){
                        policyObject[keys[i]] += 1
                    }
                }
            })
        }
        else{
            let dateRange = this.getDateRange(this.getDayMonthYear(startTime), this.getDayMonthYear(endTime))
            policyObject["date_range"] = dateRange 
            lstSelect.forEach( element=>{
                policyObject[element] = {}
                dateRange.forEach( date =>{
                    policyObject[element][date] = 0
                })
            })
            posts.map((item,index)=>{   
                const src = item._source;
                let currentTime = new Date(src.published_date)
                if(currentTime >= startTime && currentTime <= endTime){
                    let field = this.getDayMonthYear(currentTime).substring(0,7) + "-01"
                    let keys = Object.keys(src.process_talent_info)
                    lstSelect.forEach( element=>{
                        if(src.process_talent_info[element].length > 0){
                            policyObject[element][field] += 1
                        } 
                    })
                }
            })
            console.log("1112222333", policyObject)
        }
        
        return policyObject;
    } 

    getDayMonthYear= (dateObj)=>{
        var month = dateObj.getUTCMonth() + 1; //months from 1-12
        var day = dateObj.getUTCDate();
        var year = dateObj.getUTCFullYear();
        var displayMonth = month < 10 ? '0'+month : month;
        return year + "-" + displayMonth + "-" + day;
    }
}

const mapStateToProps = state =>({
    posts: state.loadPost.posts,
    chartType: state.chartStas.chartType,
    aspect: state.chartStas.aspect,
    startTime: state.chartStas.startTime,
    endTime: state.chartStas.endTime,
    startRend: state.chartStas.startRend,
    lstBarValue: state.chartStas.lstBarValue,
})

const mapDispatchToProps = (dispatch) => {
    return {
        loadPost: (payload)=>{
            dispatch(loadPost(payload))
        }
    }
}

export default connect(mapStateToProps,mapDispatchToProps)(ChartDashBoard)