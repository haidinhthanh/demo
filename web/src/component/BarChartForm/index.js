import React,{Component} from "react";
import { css } from "aphrodite";
import { d, fled, w, fle, h, ff, fw, fs, m, bc, jc, ai, b, pad } from "../../styles/themes";
import Selector from "../Selector";
import MultiSelector from "../MultiSelector";
import {connect} from "react-redux"; 
import {changeChartStas} from "../../store/actions/chart";
import DatePicker from "../../component/DatePicker";
const typeAspect = ["Content Type", "Feature"]
const contentType = ["Công nghệ", "Giáo dục", "Giải trí", "Khoa học", "Kinh tế", "Pháp luật", "Thế giới", "Thể Thao", "Văn hóa", "Xã hội", "Y tế"]
const feature = ["Regime", "Salary", "Environment"]
class BarChartForm extends Component{
    constructor(props){
        super(props)
    }
    rendMultiSelect = (aspect,changeChartStas)=>{
        if(aspect== "Content Type"){
            return <MultiSelector sets={contentType} onChangeStas={(lstSelected)=>{
                changeChartStas({
                    lstBarValue: lstSelected
                })
            }}/>
        }
        else if( aspect == "Feature"){
            return <MultiSelector sets={feature} onChangeStas={(lstSelected)=>{
                changeChartStas({
                    lstBarValue: lstSelected
                })
            }}/>
        }
        else{
            return null
        }
    }

    render() {
        const {changeChartStas, aspect, } = this.props
        const rendMultiSelect = this.rendMultiSelect(aspect, changeChartStas)
        return (
            <div className={css(d.flex, fled.c, w.w_100,)}>
                <div className={css(d.flex, jc.sa,)}>
                    <div className={css(d.flex, ff.IBM, fw.w700, fs.emd, ai.c, jc.fs, fle.flex_1)}>
                        Type of aspect:
                    </div>
                    <div className={css(d.flex, ai.c, fle.flex_1)}>
                        <Selector name={"Aspect"} items={typeAspect} 
                            onChangeStas={(aspect)=>{
                                changeChartStas({
                                    aspect: aspect,
                                    startRend: false,
                                    newstas: []
                                })
                            }}
                        />
                    </div>
                </div>
                {
                    aspect !== "" ?( 
                    <div className={css(d.flex, jc.sa, m.mg_t_md)}>
                        <div className={css(d.flex, ff.IBM, fw.w700, fs.emd, ai.c, jc.fs, fle.flex_1)}>
                            Value:
                        </div>
                        <div className={css(d.flex, ai.c, fle.flex_1)}>
                            {rendMultiSelect}
                        </div>
                    </div>):null
                }   
                <div className={css(d.flex, jc.sa, m.mg_t_md)}>
                    <div className={css(d.flex, ff.IBM, fw.w700, fs.emd, ai.c, jc.fs, fle.flex_1)}>
                        Start Date:
                    </div>
                    <div className={css(d.flex, ai.c, fle.flex_1)}>
                        <DatePicker
                            time={"2019-01-01T21:11:54"}
                            onChangeStas={(time)=>{
                                changeChartStas({
                                    startTime: time,
                                })
                            }}
                        />
                    </div>
                </div>
                <div className={css(d.flex, jc.sa, m.mg_t_md)}>
                    <div className={css(d.flex, ff.IBM, fw.w700, fs.emd, ai.c, jc.fs, fle.flex_1)}>
                        End Date:
                    </div>
                    <div className={css(d.flex, ai.c, fle.flex_1)}>
                        <DatePicker
                            time={"2019-12-01T21:11:54"}
                            onChangeStas={(time)=>{
                                changeChartStas({
                                    endTime: time
                                })
                            }}
                        />
                    </div>
                </div>
            </div>
        )
    }
}


const mapStateToProps = state =>({
    aspect: state.chartStas.aspect,
    lstBarValue: state.chartStas.lstBarValue,
})
const mapDispatchToProps = (dispatch) => {
    return {
        changeChartStas: (payload)=>{
            dispatch(changeChartStas(payload))
        }
    }
}
export default connect(mapStateToProps,mapDispatchToProps)(BarChartForm);
