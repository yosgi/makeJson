import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";

const useStyles = makeStyles({
  table: {
    width: 450
  }
});

export default function BasicTable(props: any) {
  const { data } = props;
  const classes = useStyles();

  return (
    <TableContainer component={Paper} className={classes.table}>
      <Table aria-label="simple table">
        <TableHead>
          <TableRow>
            {data.map((v: any, index: number) => {
              if (index === 0) {
                return v.map((w: string) => {
                  return <TableCell align="left">{w}</TableCell>;
                });
              }
            })}
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row: [], index: number) => {
            if (index === 0) return "";
            return (
              <TableRow key={index}>
                <TableCell align="left" component="th" scope="row">
                  {row[0]}
                </TableCell>
                <TableCell align="left">{row[1]}</TableCell>
                <TableCell align="left">{row[2]}</TableCell>
                <TableCell align="left">{row[3]}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
