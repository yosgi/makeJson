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
export default function BannerComponent(props: any) {
  const { setDialog, addObj, editting, editObj, type } = props;
  const classes = useStyles();
  const [forms, setForm] = useState(
    editting
      ? editting
      : {
          image: "",
          main: "",
          des: "",
          text: ""
        }
  );

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const formProps = Object.fromEntries(formData);
    editting ? editObj(type, formProps) : addObj(type, formProps);
    setDialog(false);
  };

  return (
    <div>
      <DialogTitle>主图，或者文章+ 主图模块</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          {types.map((v) => {
            return (
              <FormControl key={v.key} className={classes.input}>
                <TextField
                  defaultValue={forms[v.key]}
                  name={v.key}
                  id="standard-basic"
                  label={v.label}
                />
              </FormControl>
            );
          })}
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
