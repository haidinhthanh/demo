import {OC_SIDEBAR} from "../type";


export const sideBar = (state = {isOpen: false}, {type, payload})=>{
    switch(type){
        case OC_SIDEBAR:{
            return {
                isOpen: payload.isOpen
            }
        }
        default:
            return {
                isOpen: state.isOpen
            }
    }
}