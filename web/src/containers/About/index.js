import React,{Component} from 'react'
class About extends Component{
    constructor(props){
        super(props)
    }
    state = {
       count: 0
    }
   componentDidMount(){
        let element = this.progressBar;
        element.scrollIntoView({ behavior: "smooth" })
   }
   componentDidUpdate(){
    let element = this.progressBar;
    console.log( element );
    element.scrollIntoView({ behavior: "smooth" })
   }
   render() {

   return(
         <div >
             <div ref={(pb) =>this.progressBar=pb}>
                 <div>
                 Đinh Thanh Hải</div>
                 <div>
                 Đinh Thanh Hải</div>
            </div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
             <div>mèo</div>
         </div>
        );
   }
}
export default About;

// class App extends React.Component {
//     constructor(props){
//         super(props)
//     }
//     state = {
//        count: 0
//     }
//    componentDidMount(){
//         var deg = 30;
//         let element = this.progressBar;
//         console.log( element );
//         element.scrollIntoView({ behavior: "smooth" })
//    }
//    componentDidUpdate(){
//     let element = this.progressBar;
//     console.log( element );
//     element.scrollIntoView({ behavior: "smooth" })
//    }
//    render() {
    
  
//    console.log(this)
  
//    return(
//          <div >
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div>mèo</div>
//              <div ref={(pb) =>this.progressBar=pb}>Đinh Thanh Hải</div>
//          </div>
//         );
  
//    }
   
//   }

//   export default App;