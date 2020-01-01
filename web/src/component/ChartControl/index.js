import React,{Component} from "react";
import { css } from "aphrodite";
import { d, fled, w, fle, h, ff, fw, fs, m, bc, jc, ai, b, pad } from "../../styles/themes";
import Selector from "../Selector";
import {connect} from "react-redux";  
import PieChartForm from "../PieChartForm";
import BarChartForm from "../BarChartForm";
import {changeChartStas} from "../../store/actions/chart";
import Button from '@material-ui/core/Button';
const typeChart = ["Pie Chart", "Bar Chart"]

class ChartControl extends Component{
    constructor(props) {
        super(props);
    }

    rendChartForm =(chartType)=>{
        if(chartType == "Pie Chart"){
            return (
                <div className={css(pad.md, bc.white ,)}> 
                    <PieChartForm/>
                </div>
            )
        }
        else if(chartType == "Bar Chart"){
            return (
                <div className={css(pad.md, bc.white)}> 
                    <BarChartForm/>
                </div>
            )
        }
        else {
            return null
        }
    }
    render() {
        const { chartType, changeChartStas, startRend} = this.props
        const rendForm = this.rendChartForm(chartType)
        return (
            <div className={css(d.flex, fled.c, w.w_100, b.br_br_45, b.br_tr_45, b.b_l_l, b.b_r_l)}>
                <div className={css(d.flex, jc.sa, pad.md, b.b_b_l,)}>
                    <div className={css(d.flex, ff.IBM, fw.w700,fs.emd, ai.c, jc.fs, fle.flex_1,)}>
                        Type of chart:
                    </div>
                    <div className={css(d.flex, ai.c, fle.flex_1,)}>
                        <Selector name={"Type"} items={typeChart} onChangeStas={(chart)=>{
                            changeChartStas({
                                chartType: chart,
                                startRend: false,
                                aspect: ""
                            })
                        }}/>
                    </div>
                </div>
                {rendForm}
                <div className={css(d.flex, jc.sa,pad.md, b.b_t_l )}>
                    <Button 
                        variant="contained" 
                        color="primary" 
                        onClick={()=>{
                            changeChartStas({
                                startRend: true
                            })
                        }}>
                        Create Chart
                    </Button>
                    <Button 
                        variant="contained" 
                        color="primary" 
                        onClick={()=>{
                            changeChartStas({
                                startRend: false
                            })
                        }}>
                        Remove chart
                    </Button>
                </div>
            </div>
        )
    }
}

const mapStateToProps = state =>({
    chartType: state.chartStas.chartType,
    startRend: state.chartStas.startRend,
})

const mapDispatchToProps = (dispatch) => {
    return {
        changeChartStas: (payload)=>{
            dispatch(changeChartStas(payload))
        }
    }
}

export default connect(mapStateToProps,mapDispatchToProps)(ChartControl);
