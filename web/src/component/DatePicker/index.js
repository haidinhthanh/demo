import 'date-fns';
import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import DateFnsUtils from '@date-io/date-fns';
import {
  MuiPickersUtilsProvider,
  KeyboardTimePicker,
  KeyboardDatePicker,
} from '@material-ui/pickers';
import {connect} from "react-redux"; 
import {changeChartStas} from "../../store/actions/chart";

class DatePicker extends Component{
  constructor(props){
    super(props)
    this.state={
      selectedDate: new Date(this.props.time)
    }
    this.props.onChangeStas(new Date(this.props.time))
  }

  handleDateChange = date => {
    this.setState({
      selectedDate: date
    })
    this.props.onChangeStas(date)
  };
  render() {
    const {selectedDate} = this.state
    return (
      <MuiPickersUtilsProvider utils={DateFnsUtils}>
        <Grid container justify="space-around">
          <KeyboardDatePicker
            margin="normal"
            id="date-picker-dialog"
            label="Date picker dialog"
            format="dd/MM/yyyy"
            value={selectedDate}
            onChange={(date)=>{
              console.log("111111111111", date)
              this.handleDateChange(date)
            }}
            KeyboardButtonProps={{
              'aria-label': 'change date',
            }}
          />
        </Grid>
      </MuiPickersUtilsProvider>
    );
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
      changeChartStas: (payload)=>{
          dispatch(changeChartStas(payload))
      }
  }
}
export default connect(null,mapDispatchToProps)(DatePicker);