import React from "react";
import "../public/css/main.css";
import Option from "./Options";
import { Alert, Form, Button, FormGroup, Input, Col } from "reactstrap";
import Wait from "./Wait";
import Result from "./Result";
import Download from "./download";

class Main extends React.Component {
  constructor(props) {
    super(props);
    this.elementInput = React.createRef();

    this.initalState = {
      check: {
        option: true,
        loading: false,
        result: false,
        input: true,
      },
      domain: "",
      port: "",
      bruteForce: false,
      allEngine: true,
      engines: [
        { name: "Baidu", status: true, id: "baidu" },
        { name: "Yahoo", status: true, id: "yahoo" },
        { name: "Google", status: true, id: "google" },
        { name: "Bing", status: true, id: "bing" },
        { name: "Ask", status: true, id: "ask" },
        { name: "Net Craft", status: true, id: "netcraft" },
        { name: "DNS Dumpster", status: true, id: "dnsdumpster" },
        { name: "Virus Total", status: true, id: "virustotal" },
        { name: "Threat Crowd", status: true, id: "threatcrowd" },
        { name: "SSL Certificates", status: true, id: "ssl" },
        { name: "Passive Dns", status: true, id: "passivedns" },
      ],
      result: [],
      error: "",
    };

    this.state = this.initalState;

    this.handleClickEngine = this.handleClickEngine.bind(this);
    this.handleClickBrute = this.handleClickBrute.bind(this);
    this.onInputPort = this.onInputPort.bind(this);
    this.onInputDomain = this.onInputDomain.bind(this);
    this.callAPI = this.callAPI.bind(this);
    this.checkData = this.checkData.bind(this);
    this.handleCheckAll = this.handleCheckAll.bind(this);
    this.handleNewScan = this.handleNewScan.bind(this);
  }
  componentDidMount() {
    this.elementInput.current.focus();
  }

  handleClickEngine(engine) {
    return (e) => {
      const engines = this.state.engines;
      const index = engines.indexOf(engine);
      const status = engines[index].status;
      if (status) {
        this.setState({
          allEngine: false,
        });
      }
      this.setState({
        engines: [
          ...engines.slice(0, index),
          {
            ...engine,
            status: !status,
          },
          ...engines.slice(index + 1),
        ],
      });
    };
  }

  handleClickBrute() {
    this.setState({
      bruteForce: !this.state.bruteForce,
    });
  }

  handleNewScan() {
    this.setState({
      ...this.initalState,
    });
  }

  onInputPort(e) {
    const port = e.target.value;
    this.setState({
      port: port,
    });
  }

  onInputDomain(e) {
    const domain = e.target.value;
    this.setState({
      domain: domain,
    });
  }

  handleCheckAll() {
    const checkAll = this.state.allEngine;
    this.setState({
      allEngine: !checkAll,
      engines: [
        { name: "Baidu", status: !checkAll, id: "baidu" },
        { name: "Yahoo", status: !checkAll, id: "yahoo" },
        { name: "Google", status: !checkAll, id: "google" },
        { name: "Bing", status: !checkAll, id: "bing" },
        { name: "Ask", status: !checkAll, id: "ask" },
        { name: "Net Craft", status: !checkAll, id: "netcraft" },
        { name: "DNS Dumpster", status: !checkAll, id: "dnsdumpster" },
        { name: "Virus Total", status: !checkAll, id: "virustotal" },
        { name: "Threat Crowd", status: !checkAll, id: "threatcrowd" },
        { name: "SSL Certificates", status: !checkAll, id: "ssl" },
        { name: "Passive Dns", status: !checkAll, id: "passivedns" },
      ],
    });
  }

  checkData() {
    const domain = this.state.domain;
    if (domain.length === 0) {
      console.log(domain.length);
      throw new Error("Require domain");
    }
  }

  async callAPI(e) {
    e.preventDefault();
    try {
      await this.checkData();
    } catch (error) {
      await this.setState({
        error: error.message,
      });
      return;
    }
    this.setState({
      check: {
        input: false,
        loading: true,
        option: false,
        result: false,
      },
      error: "",
    });
    const domain = this.state.domain.toLowerCase();
    const portQuery = this.state.port ? "&ports=" + this.state.port : "";
    const bruteForceQuery = "?bruteforce=" + this.state.bruteForce;

    let engineQuery = "";
    if (!this.state.allEngine) {
      const engines = this.state.engines;
      engines.forEach((engine) => {
        if (engine.status) {
          engineQuery = engineQuery + engine.id + ",";
        }
      });
      engineQuery = engineQuery.slice(0, -1);
      engineQuery = "&engines=" + engineQuery;
    }

    const query =
      "http://localhost:8000/api/" +
      domain +
      bruteForceQuery +
      portQuery +
      engineQuery;
    let status_code = "";
    const data = await fetch(query, {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((res) => {
      status_code = res.status;
      return res.json();
    });

    if (status_code === 400 || status_code === 504) {
      this.setState({
        check: {
          option: true,
          loading: false,
          result: false,
          input: true,
        },
        error: data.Error,
      });
    } else if (status_code === 200) {
      console.log(data);
      if (data.result.length !== 0) {
        this.setState({
          result: [...data.result],
          check: {
            option: false,
            loading: false,
            result: true,
            input: false,
          },
          error: "",
        });
      } else {
        this.setState({
          check: {
            option: false,
            loading: false,
            result: true,
            input: false,
          },
          error: "",
        });
      }
    }
  }

  render() {
    const option = this.state.check.option;
    const loading = this.state.check.loading;
    const result = this.state.check.result;
    const input = this.state.check.input;
    return (
      <div className="cus-container">
        <h2>🅵🅸🅽🅳 🆂🆄🅱🅳🅾🅼🅰🅸🅽</h2>
        <Form>
          {input && (
            <div className="inputDomain">
              <FormGroup row>
                <Col sm={10}>
                  <Input
                    type="text"
                    name="domainInput"
                    id="domainInput"
                    placeholder="Input the domain to scan"
                    ref={this.elementInput}
                    onChange={this.onInputDomain}
                  />
                </Col>
                <Button color="warning" type="submit" onClick={this.callAPI}>
                  🆂🅲🅰🅽
                </Button>
              </FormGroup>
            </div>
          )}
          {this.state.error.length > 0 && (
            <Alert color="warning" className="error">
              {this.state.error}
            </Alert>
          )}
          {loading && (
            <div>
              <Wait engines={this.state.engines} domain={this.state.domain} />
            </div>
          )}
          {option && (
            <div>
              <Option
                clickEngine={this.handleClickEngine}
                engines={this.state.engines}
                bruteForce={this.state.bruteForce}
                clickBrute={this.handleClickBrute}
                onInputPort={this.onInputPort}
                handleCheckAll={this.handleCheckAll}
                checkAllStatus={this.state.allEngine}
              />
            </div>
          )}
          {result && (
            <div>
              <Button
                color="success"
                className="button-new-scan"
                onClick={this.handleNewScan}
              >
                New scan
              </Button>
              <b>
                <p className="result-lable">🆁🅴🆂🆄🅻🆃: Found {this.state.result.length} result </p>
              </b>
              <Result result={this.state.result} />
              <Download result={this.state.result} className="button-result" />
            </div>
          )}
        </Form>
      </div>
    );
  }
}

export default Main;
