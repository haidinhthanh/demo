import React,{Component} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles(theme => ({
  formControl: {
    margin: theme.spacing(0),
    minWidth: 150,
  },
}));

export default (props)=> {
    const classes = useStyles();
    const [value, setValue] = React.useState('');
    const inputLabel = React.useRef(null);
    const [labelWidth, setLabelWidth] = React.useState(0);
    React.useEffect(() => {
        setLabelWidth(inputLabel.current.offsetWidth);
    }, []);

    const handleChange = event => {
        setValue(event.target.value);   
        props.onChangeStas(event.target.value)
    };

    const {items, name} = props
    return (
        <div>
            <FormControl variant="outlined" className={classes.formControl}>
                <InputLabel ref={inputLabel} id="demo-simple-select-outlined-label">
                    {name}
                </InputLabel>
                <Select
                    labelId="demo-simple-select-outlined-label"
                    id="demo-simple-select-outlined"
                    value={value}
                    onChange={handleChange}
                    labelWidth={labelWidth}
                >
                    <MenuItem value="">
                        <em>None</em>
                    </MenuItem>
                    {
                        items.map((item,index)=>(
                            <MenuItem value={item}>{item}</MenuItem>
                        ))
                    }
                </Select>
            </FormControl>
        </div>
    );
    }