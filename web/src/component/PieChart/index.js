import React from 'react';
import {Pie} from 'react-chartjs-2';
import {css} from "aphrodite"
import { d, fled, w, hov } from '../../styles/themes';

const backgroundColor = ['#ff0000', '#ff4000', '#ff8000', '#ffbf00', '#ffff00', '#bfff00', '#80ff00', '#40ff00', '#00ff00', '#00ff40', '#00ff80', '#00ffbf', '#00ffff', '#00bfff', '#0080ff', '#0040ff', '#0000ff', '#4000ff', '#8000ff', '#bf00ff', '#ff00ff', '#ff00bf', '#ff0080', '#ff0040', '#ff0000']

const hovBackgroundColor =['#ff0000', '#ff4000', '#ff8000', '#ffbf00', '#ffff00', '#bfff00', '#80ff00', '#40ff00', '#00ff00', '#00ff40', '#00ff80', '#00ffbf', '#00ffff', '#00bfff', '#0080ff', '#0040ff', '#0000ff', '#4000ff', '#8000ff', '#bf00ff', '#ff00ff', '#ff00bf', '#ff0080', '#ff0040', '#ff0000']



class PieChart extends React.Component{
    render() {
        const {items} = this.props
        let keys = Object.keys((items))
        const reducer = (accumulator, currentValue) => accumulator + currentValue;

        let keys_value = keys.map((key, index)=>{
            return items[key]
        })
        const total = keys_value.reduce(reducer)
        let perCentArr = keys_value.map((item, index)=>{
            return Number(Number(item*100/total).toFixed(2))
        })
        let length = keys_value.length
        let bc = backgroundColor.slice(0,length)
        let hovBC = hovBackgroundColor.slice(0, length)
        
        const data = {
                labels: keys,
                datasets: [{
                    data: perCentArr,
                    backgroundColor: bc,
                    hoverBackgroundColor: hovBC
                }]
            }
        return (
            <Pie 
                data={data}
                width={500}
                height={500}
                options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    
                  }}
                  onElementsClick={elems => {
                    // if required to build the URL, you can 
                    // get datasetIndex and value index from an `elem`:
                    console.log("11111111111111",elems[0]._datasetIndex );
                    // and then redirect to the target page:
                    // window.location = "https://example.com";
                }}
            />
        );
      }
}

export default PieChart;
