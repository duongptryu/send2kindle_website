import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import Button from "@material-ui/core/Button";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

export default function Profile(props) {
  const classes = useStyles();
  const info = props.info;
  const isLog = props.isLog;
  const updateVipAccount = props.updateAccount
  if (info == null || isLog === false) {
    window.location.href = "/";
  }
  return (
    <div>
      <TableContainer component={Paper}>
        <h1>Profile User</h1>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            <TableRow>
              <TableCell align="center">
                {" "}
                <strong>First Name:</strong>{" "}
              </TableCell>
              <TableCell align="left">{info.first_name}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell align="center">
                {" "}
                <strong>Last Name:</strong>{" "}
              </TableCell>
              <TableCell align="left">{info.last_name}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell align="center">
                {" "}
                <strong>Username:</strong>{" "}
              </TableCell>
              <TableCell align="left">{info.username}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell align="center">
                {" "}
                <strong>Email</strong>{" "}
              </TableCell>
              <TableCell align="left">{info.email}</TableCell>
            </TableRow>
            <TableRow>
              <TableCell align="center">
                {" "}
                <strong>Vip Member</strong>{" "}
              </TableCell>
              {info.vip_member === true && (
                <TableCell align="left">VIP account</TableCell>
              )}
              {info.vip_member === false && (
                <TableCell align="left">Normal account</TableCell>
              )}
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
      {info.vip_member === false && (
        <div style={{marginTop: "20px", marginLeft: "40%"}}>
          <Button variant="contained" color="primary" disableElevation onClick={updateVipAccount}>
            Update to VIP member
          </Button>
        </div>
      )}
    </div>
  );
}

