import React from 'react';
import {Bar} from 'react-chartjs-2';
import { hov } from '../../styles/themes';
import { el } from 'date-fns/esm/locale';

const backgroundColor = ['#ff0000', '#ff4000', '#ff8000', '#ffbf00', '#ffff00', '#bfff00', '#80ff00', '#40ff00', '#00ff00', '#00ff40', '#00ff80', '#00ffbf', '#00ffff', '#00bfff', '#0080ff', '#0040ff', '#0000ff', '#4000ff', '#8000ff', '#bf00ff', '#ff00ff', '#ff00bf', '#ff0080', '#ff0040', '#ff0000']

const hovBackgroundColor =['#ff0000', '#ff4000', '#ff8000', '#ffbf00', '#ffff00', '#bfff00', '#80ff00', '#40ff00', '#00ff00', '#00ff40', '#00ff80', '#00ffbf', '#00ffff', '#00bfff', '#0080ff', '#0040ff', '#0000ff', '#4000ff', '#8000ff', '#bf00ff', '#ff00ff', '#ff00bf', '#ff0080', '#ff0040', '#ff0000']


class BarChart extends React.Component{
    render() {
      const {items} = this.props
      var new_data ={
        labels: items["date_range"],
        datasets: [
           
        ],
      }
      Object.keys(items).map((item, index)=>{
        if( item !== "date_range"){
          let dataset = {
            label: item,
            backgroundColor: backgroundColor[index],
            borderColor: backgroundColor[index],
            borderWidth: 1,
            hoverBackgroundColor: hovBackgroundColor[index],
            hoverBorderColor: hovBackgroundColor[index],
            data: []
          }
          dataset.data = Object.keys(items[item]).map((value, index)=>{
            return items[item][value]
          })
          new_data.datasets.push(dataset)
        }
      })
        return (
            <Bar
                data={new_data}
                width={200}
                height={600}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                }}
                onElementsClick={elems => {
                  // if required to build the URL, you can 
                  // get datasetIndex and value index from an `elem`:
                  console.log("11111111111111",elems );
                  // and then redirect to the target page:
                  // window.location = "https://example.com";
                }}
                getElementAtEvent={el=>{
                  console.log("122222222111",el );
                }}

            />
        )
    }
}

export default BarChart;