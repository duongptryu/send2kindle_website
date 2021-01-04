import React from "react";
import { Spinner } from "reactstrap";

const Wait = (props) => {
  const engines = props.engines;
  const domain = props.domain;
  return (
    <div>
      <div className="loading">
      <em>🅻🅾🅰🅳🅸🅽🅶</em>
      <div>
        <Spinner type="grow" color="primary" />
        <Spinner type="grow" color="secondary" />
        <Spinner type="grow" color="success" />
        <Spinner type="grow" color="danger" />
        <Spinner type="grow" color="warning" />
        <Spinner type="grow" color="info" />
        <Spinner type="grow" color="light" />
        <Spinner type="grow" color="dark" />
      </div>
      </div>
      <div className="scan-wait">
        <b>
          <p>🅢🅒🅐🅝</p>
        </b>
        <p>[-] Enumerating subdomains now for {domain}</p>
        {engines.length > 0 &&
          engines.map((engine, index) => {
            if (engine.status === true) {
              return <p>[-] Searching now in {engine.name}..</p>;
            }
            return null;
          })}
      </div>
    </div>
  );
};

export default Wait;
