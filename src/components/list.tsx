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
export default function ListComponent(props) {
  const { setDialog, addObj } = props;
  const classes = useStyles();
  const ref = useRef<HTMLInputElement>(null);
  const [forms, setForm] = useState([
    {
      content1: "",
      content2: "",
      content3: "",
      content4: ""
    }
  ]);
  const addRow = () => {
    setForm([
      ...forms,
      {
        content1: "",
        content2: "",
        content3: "",
        content4: ""
      }
    ]);
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    let index = 0;
    let res: any = [];
    for (let key in formProps) {
      if (!res[Math.floor(index / 4)]) {
        res[Math.floor(index / 4)] = {};
      }
      res[Math.floor(index / 4)][types[index % 4].key] = formProps[key];
      index++;
    }
    console.log(res);
    addObj("list", res);
    setDialog(false);
  };

  return (
    <div>
      <DialogTitle>列表</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {forms.map((form, index) => {
            return [1, 2, 3, 4].map((v) => {
              return (
                <FormControl key={index + "" + v} className={classes.input}>
                  <TextField
                    name={"content" + index + "-" + v}
                    defaultValue={form["content" + v]}
                    id="standard-basic"
                    label={v + "." + types[v - 1].label}
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
