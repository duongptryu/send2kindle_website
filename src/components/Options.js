import React from "react";
import "../public/css/main.css";
import { FormGroup, Input, Col, Label, CustomInput } from "reactstrap";

const Option = (props) => {
  const engines = props.engines;
  const engineClick = props.clickEngine;
  const bruteForce = props.bruteForce;
  const burteClick = props.clickBrute;
  const onInputPort = props.onInputPort
  const handleCheckAll = props.handleCheckAll
  const checkAllStatus = props.checkAllStatus
  return (
    <div className="options">
      <b>
        <p>🅞🅟🅣🅘🅞🅝🅢</p>
      </b>
      <FormGroup row className="abc">
        <Label for="Brutefoce" sm={4}>
          Brutefoce:{" "}
        </Label>
        <Label sm={2}><strong>Disabled</strong></Label>
        <CustomInput sm={4} type="switch" className="nut" id="bruteForce" name="bruteForce" onClick={burteClick} checked={bruteForce}/>
        <Label sm={2}><strong>Enabled</strong></Label>
      </FormGroup>
      <FormGroup row>
        <Label for="Port" sm={4}>
          Port:{" "}
        </Label>
        <Col sm={8}>
          <Input type="text" placeholder="Input the port - split by ," id="port" name="port" onChange={onInputPort} pattern="[\d,]"/>
        </Col>
      </FormGroup>
      <FormGroup row>
        <Label for="engine" sm={4}>
          Engines:
        </Label>
        <Col sm={8}>
          <div>
          <CustomInput sm={4} type="checkbox" id="checkAll" name="checkAll" onClick={handleCheckAll} checked={checkAllStatus} label="Choose All"/>
            {engines.length !== 0 &&
              engines.map((engine, index) => {
                return (
                  <CustomInput
                  key={index}
                    type="switch"
                    id={engine.id}
                    name={engine.id}
                    label={engine.name}
                    checked={engine.status}
                    onClick={engineClick(engine)}
                  />
                );
              })}
          </div>
        </Col>
      </FormGroup>
    </div>
  );
};

export default Option;
