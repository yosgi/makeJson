import DialogTitle from "@material-ui/core/DialogTitle";
import React, { useState, useRef, useEffect } from "react";
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
export default function ListComponent(props: any) {
  const { setDialog, addObj, editting, editObj, type } = props;
  const classes = useStyles();
  console.log(editting);
  const attrMap = [];
  const attrs = {};
  types.forEach((v: any) => {
    attrs[v.key] = "";
    attrMap.push(v.key);
  });
  const [forms, setForm] = useState(editting ? editting : [attrs]);
  const addRow = () => {
    setForm([...forms, attrs]);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    let index = 0;
    let res: any = [];
    for (let key in formProps) {
      if (!res[Math.floor(index / attrMap.length)]) {
        res[Math.floor(index / attrMap.length)] = {};
      }
      res[Math.floor(index / attrMap.length)][
        types[index % attrMap.length].key
      ] = formProps[key];
      index++;
    }
    editting ? editObj(type, res) : addObj(type, res);
    setDialog(false);
  };

  return (
    <div>
      <DialogTitle>图文列表</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {forms.map((form: any, index: number) => {
            return attrMap.map((key, v) => {
              return (
                <FormControl key={index + "" + v} className={classes.input}>
                  <TextField
                    name={"content" + index + "-" + v}
                    defaultValue={form[key]}
                    id="standard-basic"
                    label={v + 1 + "." + types[v].label}
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
