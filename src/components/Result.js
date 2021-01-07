import React from "react";
import "../public/css/main.css";
import { Table } from "reactstrap";

const Result = (props) => {
  const subdomains = props.result;

  return (
    <div className="options scrollBar">
      {subdomains.length > 0 && (
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
                    <td>{index + 1}</td>
                    <td>{subdomain.host}</td>
                    {subdomain.port && <td>{subdomain.port}</td>}
                    {subdomain.port == null && <td>None</td>}
                  </tr>
                );
              })}
          </tbody>
        </Table>
      )}
      {subdomains.length === 0 && <h1>No result</h1>}
    </div>
  );
};

export default Result;
