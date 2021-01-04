import React from "react";
import "../public/css/main.css";
import { Table } from "reactstrap";

const Result = (props) => {
  const subdomains = props.result;
  const checkResult = props.checkResult
  console.log(checkResult)
  let port = props.port;
  if(port == null){
    port = "None"
  }
  return (
    <div className="options scrollBar">
      <b>
        <p>🆁🅴🆂🆄🅻🆃</p>
      </b>
      {checkResult === true && (
         <Table striped bordered hover variant="dark">
         <thead>
           <tr>
             <th>#</th>
             <th>Sub Domain Name</th>
             <th>Port</th>
           </tr>
         </thead>
         <tbody>
           {subdomains.length > 0 &&
             subdomains.map((subdomain, index) => {
               return (
                 <tr>
                   <td>{index}</td>
                   <td>{subdomain}</td>
                   <td>{port}</td>
                 </tr>
               );
             })}
         </tbody>
       </Table>
      )}
      {checkResult === false && <h1>No result</h1>}
    </div>
  );
};

export default Result;
