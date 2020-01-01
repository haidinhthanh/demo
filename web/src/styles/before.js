import { StyleSheet } from "aphrodite";

export default StyleSheet.create({
    create_up_triagle: {
        ':before': {
            width: 0,
            height: 0,
            borderRight:"9px",
            borderRightStyle: "solid",
            borderRightColor: "transparent",
            borderLeft: "9px",
            borderLeftStyle: "solid",
            borderLeftColor: "transparent",
            borderBottom: "9px",
            borderBottomStyle: "solid",
            borderBottomColor: "#000000",
        }
    }
})