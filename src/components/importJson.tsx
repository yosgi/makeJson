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
    },
    uploadButton: {
      position: "fixed",
      top: 70,
      right: 30
    }
  })
);

export default function UploadButtons(props: any) {
  const { setObj } = props;
  const classes = useStyles();
  const handleChange = (event: any) => {
    console.log(111);
    var reader = new FileReader();
    console.log(event.target.files[0]);
    reader.onload = function (event) {
      var jsonObj = JSON.parse(event.target.result);
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
        <Button
          className={classes.uploadButton}
          variant="contained"
          color="primary"
          component="span"
        >
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
