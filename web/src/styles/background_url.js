import {StyleSheet} from "aphrodite";

export default (background_url)=>{
    return StyleSheet.create({
      bgu:{
        background: "url("+background_url+")",
      }
    })
}

