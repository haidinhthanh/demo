import {CHANGE_STAS} from "../type";

const initialState = {
    startRend: false,
    chartType: "",
    aspect: "",
    startTime: "",
    endTime: "",
    lstBarValue: [],
    newstas: [],
}

export const chartStas = (state = initialState, {type, payload})=>{
    switch(type){
        case CHANGE_STAS:{
            return {
                ...state,
                ...payload
            }
        }
        default:
            return state;
    }
}
