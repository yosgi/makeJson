import React from "react";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";
import ImageList from "@material-ui/core/ImageList";
import ImageListItem from "@material-ui/core/ImageListItem";
import ImageListItemBar from "@material-ui/core/ImageListItemBar";
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      display: "flex",
      flexWrap: "wrap",
      justifyContent: "center",
      overflow: "hidden",
      backgroundColor: theme.palette.background.paper
    },
    imageList: {
      width: "100%"
    }
  })
);
export default function Banner(props: any) {
  const { data } = props;
  console.log(data);
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <ImageList rowHeight={180} className={classes.imageList}>
        <ImageListItem>
          <img src={data.image} alt={data.main} />
          <ImageListItemBar
            title={data.des}
            subtitle={<span> {data.text}</span>}
          />
        </ImageListItem>
      </ImageList>
    </div>
  );
}
