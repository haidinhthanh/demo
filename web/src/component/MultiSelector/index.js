import React from 'react';
import clsx from 'clsx';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import ListItemText from '@material-ui/core/ListItemText';
import Select from '@material-ui/core/Select';
import Checkbox from '@material-ui/core/Checkbox';
import Chip from '@material-ui/core/Chip';

import {connect} from "react-redux"; 
import {changeChartStas} from "../../store/actions/chart";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};


class MultipleSelect extends React.Component {
  constructor(props){
    super(props)
    // this.state={values : []}
  }
  render() {
    const {sets, onChangeStas, changeChartStas, newstas } = this.props
    // const {values} = this.state
    const handleChange = event => {
      // this.setState({
      //   values : event.target.value
      // })
      changeChartStas({
        newstas: event.target.value,
      })
      onChangeStas(event.target.value)
    };
    return (
        <FormControl style={{
          margin: 8,
          minWidth: 120,
          maxWidth: 300,
        }}>
          <InputLabel id="demo-mutiple-chip-label">Chip</InputLabel>
          <Select
            labelId="demo-mutiple-chip-label"
            id="demo-mutiple-chip"
            multiple
            value={newstas}
            onChange={handleChange}
            input={<Input id="select-multiple-chip" />}
            renderValue={selected => (
              <div 
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                }} 
              >
                {selected.map(value => {
                  return (
                    <Chip key={value} label={value} style={{margin: 2,}}/>
                  )
                })}
              </div>
            )}
            MenuProps={MenuProps}
          >
            {sets.map(name => (
              <MenuItem key={name} value={name} >
                {name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

    );
  }
}


const mapStateToProps = state =>({
  newstas: state.chartStas.newstas
})
const mapDispatchToProps = (dispatch) => {
  return {
      changeChartStas: (payload)=>{
          dispatch(changeChartStas(payload))
      }
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(MultipleSelect);
