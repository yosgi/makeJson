import React from "react";
import { makeStyles, createStyles, Theme } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      "& > *": {
        margin: theme.spacing(1)
      }
    },
    input: {
      display: "none"
    }
  })
);

export default function UploadButtons(props: any) {
  const { setObj } = props;
  const classes = useStyles();
  const handleChange = (event: any) => {
    var reader = new FileReader();
    reader.onload = function (event) {
      var jsonObj = JSON.parse(event.target.result +'');
      setObj(jsonObj);
    };
    if (event.target.files[0]) {
      reader.readAsText(event.target.files[0]);
    }
  };

  return (
    <div className={classes.root}>
      <input
        onChange={handleChange}
        accept="json/*"
        className={classes.input}
        id="contained-button-file"
        multiple
        type="file"
      />
      <label htmlFor="contained-button-file">
        <Button {...props} variant="contained" color="primary" component="span">
          导入JSON
        </Button>
      </label>
      <input
        onChange={handleChange}
        accept="json/*"
        className={classes.input}
        id="icon-button-file"
        type="file"
      />
    </div>
  );
}
