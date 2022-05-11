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
      justifyContent: "space-around",
      overflow: "hidden"
    },
    imageList: {
      width: 500
    },
    href: {
      color: "#fff",
      textDecoration: "none",
      fontSize: 12,
      paddingRight: 10
    }
  })
);

export default function BasicImageList(props: any) {
  const classes = useStyles();
  const { data } = props;
  return (
    <div className={classes.root}>
      <ImageList className={classes.imageList} cols={3}>
        {data.map((item: any, index: number) => (
          <ImageListItem key={index} cols={item.cols || 1}>
            <img src={item.image} alt={item.title} />
            <ImageListItemBar
              title={item.main}
              subtitle={<span>{item.des}</span>}
              actionIcon={
                <a className={classes.href} href={item.url} target="_blank">
                  跳转
                </a>
              }
            ></ImageListItemBar>
          </ImageListItem>
        ))}
      </ImageList>
    </div>
  );
}
