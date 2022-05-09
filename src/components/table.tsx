import DialogTitle from "@material-ui/core/DialogTitle";
import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import DialogActions from "@material-ui/core/DialogActions";
import FormControl from "@material-ui/core/FormControl";
import TextField from "@material-ui/core/TextField";
import DialogContent from "@material-ui/core/DialogContent";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";
import { types } from "../data";
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    select: {
      width: 60
    },
    input: {
      width: 100,
      marginLeft: 10
    },
    button: {
      float: "left"
    }
  })
);
export default function TableComponent(props: any) {
  const { setDialog, addObj, editting, editObj, type } = props;
  const classes = useStyles();
  console.log(editting);
  const [forms, setForm] = useState(editting ? editting : [["", "", "", ""]]);
  console.log(forms);
  const addRow = () => {
    setForm([...forms, ["", "", "", ""]]);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    console.log(formProps);
    let index = 0;
    let res: any = [];
    for (let key in formProps) {
      if (!res[Math.floor(index / 4)]) {
        res[Math.floor(index / 4)] = [];
      }
      res[Math.floor(index / 4)].push(formProps[key]);
      index++;
    }
    editting ? editObj(type, res) : addObj(type, res);
    setDialog(false);
  };

  return (
    <div>
      <DialogTitle>列表</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {forms.map((form: any, i: number) => {
            return form.map((v: string, j: number) => {
              return (
                <FormControl key={i + "-" + j} className={classes.input}>
                  <TextField
                    name={i + "-" + j}
                    defaultValue={v}
                    label={i === 0 ? `表头第${j + 1}列` : `第${j + 1}列`}
                  />
                </FormControl>
              );
            });
          })}
          <Button
            onClick={addRow}
            className={classes.button}
            color="primary"
            autoFocus
          >
            增加一行
          </Button>
        </DialogContent>
        <DialogActions>
          <Button color="primary" onClick={() => setDialog(false)}>
            取消
          </Button>
          <Button color="primary" type="submit">
            确定
          </Button>
        </DialogActions>
      </form>
    </div>
  );
}
