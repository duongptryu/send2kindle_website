import React from "react";
import "../public/css/main.css";
import { Table } from "reactstrap";
import "../public/css/guide.css"
const Guide = () => {
  return (
    <div className="cus-container">
      <h2>🅶🆄🅸🅳🅴 🆂🆄🅱🅻🅸🆂🆃3🆁</h2>
      <div className="about">
        <h1>About Sublist3r</h1>
        <p>
          Sublist3r is a python tool designed to enumerate subdomains of
          websites using OSINT. It helps penetration testers and bug hunters
          collect and gather subdomains for the domain they are targeting.
          Sublist3r enumerates subdomains using many search engines such as
          Google, Yahoo, Bing, Baidu and Ask. Sublist3r also enumerates
          subdomains using Netcraft, Virustotal, ThreatCrowd, DNSdumpster and
          ReverseDNS.
        </p>
        <p>
          <a href="https://github.com/TheRook/subbrute">Subbrute</a> was
          integrated with Sublist3r to increase the possibility of finding more
          subdomains using bruteforce with an improved wordlist. The credit goes
          to TheRook who is the author of subbrute.
        </p>
      </div>
      <div className="guide">
        <h1>Usage</h1>
        <Table striped bordered hover variant="dark">
          <thead>
            <tr>
              <th>Function</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Brutefoce</td>
              <td>Enable or Disabled the subbrute bruteforce module</td>
            </tr>
            <tr>
              <td>Port</td>
              <td>
                Scan the found subdomains against specific tcp ports,{" "}
                <b>separated by commas </b>
              </td>
            </tr>
            <tr>
              <td>Engine</td>
              <td>Specify a comma-separated list of search engines</td>
            </tr>
          </tbody>
        </Table>
      </div>
      <div className="license">
        <h1>License</h1>
        <p>
          Sublist3r is licensed under the GNU GPL license. take a look at the{" "}
          <a href="https://github.com/aboul3la/Sublist3r/blob/master/LICENSE">
            LICENSE
          </a>{" "}
          for more information.
        </p>
      </div>
      <div>
        <h1>Credits</h1>
        <ul>
          <li>
            <a href="https://github.com/TheRook">TheRock</a>- The bruteforce
            module was based on his script <strong>subbrute</strong>.
          </li>
          <li>
            <a href="https://github.com/bitquark">Bitquark</a>- The Subbrute's wordlist was based on his research <strong>dnspop</strong>.
          </li>
        </ul>
      </div>
      <div>
          <h1>Version</h1>
          <strong>Current version is 1.0</strong>
      </div>
    </div>
  );
};

export default Guide;
