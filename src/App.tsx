import "./styles.css";
import React, { useState } from "react";
import ListItem from "@material-ui/core/ListItem";
import List from "@material-ui/core/List";

import ListItemText from "@material-ui/core/ListItemText";
import Button from "@material-ui/core/Button";
import Drawer from "@material-ui/core/Drawer";
import Dialog from "@material-ui/core/Dialog";
import ListComponent from "./components/list";
import TableComponent from "./components/table";
import BannerComponent from "./components/banner";
import Box from "@material-ui/core/Box";
import { menuList } from "./data";
import RenderList from "./components/renderList";
import RenderBanner from "./components/renderBanner";
import RenderTable from "./components/renderTable";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";
import toJson from "./utils/exportJSON";
import UploadButton from "./components/importJson";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
const ComponentInModal = function (props: any) {
  let { type } = props;
  if (type.toUpperCase().indexOf("LIST") > -1) {
    return <ListComponent {...props}></ListComponent>;
  } else if (type.toUpperCase().indexOf("BANNER") > -1) {
    return <BannerComponent {...props}></BannerComponent>;
  } else if (type.toUpperCase().indexOf("TABLE") > -1) {
    return <TableComponent {...props}></TableComponent>;
  }
};
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    dialog: {
      width: 500
    },
    addButton: {
      position: "fixed",
      top: 10,
      right: 150
    },
    imageList: {
      width: 500,
      height: 450
    },
    drawer: {
      width: 100,
      marginLeft: 20
    },
    exportButton: {
      position: "fixed",
      top: 10,
      right: 30
    },

    App: {
      paddingTop: 50,
      width: 700,
      margin: "auto"
    },
    card: {
      marginBottom: 30
    },
    title: {
      padding: "20px 0 0 20px"
    }
  })
);
function chooseComponent(v: any, exportObj: any) {
  if (v.toUpperCase().indexOf("LIST") > -1) {
    return <RenderList data={exportObj[v]}></RenderList>;
  } else if (v.toUpperCase().indexOf("BANNER") > -1) {
    return <RenderBanner data={exportObj[v]}> </RenderBanner>;
  } else if (v.toUpperCase().indexOf("TABLE") > -1) {
    return <RenderTable data={exportObj[v]}> </RenderTable>;
  }
  return <div>none</div>;
}

export default function App() {
  const classes = useStyles();
  const [exportObj, setObj]: any = useState({});
  const [DrawerState, setDawerState] = useState(false);
  const [showDialog, setDialog] = useState(false);
  const [current, setCurrent] = useState("");
  const [editting, setEditting] = useState(null);
  const toggleDrawer = (open: boolean) => {
    setDawerState(open);
  };
  console.log(exportObj);
  const tabSelected = (tab: string) => {
    setCurrent(tab);
    toggleDrawer(false);
    setDialog(true);
  };
  const findTypeName: any = (type: string) => {
    if (exportObj[type]) {
      return findTypeName(type + "-1");
    }
    return type;
  };
  const addObj = (type: string, obj: any) => {
    let typeName = findTypeName(type);
    exportObj[typeName] = obj;
    setObj(exportObj);
  };
  const editObj = (type: string, obj: any) => {
    exportObj[type] = obj;
    setObj(exportObj);
    setCurrent("");
    setEditting(null);
  };
  const exportJSON = (json: any) => {
    toJson(json);
  };
  const handleDelete = (key: any) => {
    let newObj: any = { ...exportObj };
    delete newObj[key];
    setObj(newObj);
  };
  const handleEdit = (key: any) => {
    setCurrent(key);
    setEditting(exportObj[key]);

    setDialog(true);
  };

  console.log(exportObj);
  return (
    <div className={classes.App}>
      <Button
        onClick={() => toggleDrawer(!DrawerState)}
        variant="contained"
        color="primary"
        className={classes.addButton}
      >
        新增模块
      </Button>
      <Button
        onClick={() => exportJSON(exportObj)}
        color="primary"
        variant="contained"
        className={classes.exportButton}
      >
        导出Json
      </Button>
      <UploadButton setObj={setObj}></UploadButton>
      {Object.keys(exportObj).map((v) => {
        return (
          <Card className={classes.card}>
            <Typography className={classes.title}>{v.toUpperCase()}</Typography>
            <CardContent>{chooseComponent(v, exportObj)}</CardContent>
            <CardActions>
              <Button size="small" onClick={() => handleEdit(v)}>
                编辑
              </Button>
              <Button size="small" onClick={() => handleDelete(v)}>
                删除
              </Button>
            </CardActions>
          </Card>
        );
      })}
      <Drawer
        anchor="left"
        open={DrawerState}
        onClose={() => toggleDrawer(!DrawerState)}
      >
        <List>
          {menuList.map((v, index) => (
            <ListItem button key={v.key}>
              <ListItemText
                className={classes.drawer}
                onClick={() => {
                  tabSelected(v.key);
                }}
                primary={v.label}
              />
            </ListItem>
          ))}
        </List>
      </Drawer>
      <Dialog open={showDialog}>
        <Box className={classes.dialog}>
          <ComponentInModal
            editting={editting}
            type={current}
            addObj={addObj}
            setDialog={setDialog}
            editObj={editObj}
          ></ComponentInModal>
        </Box>
      </Dialog>
    </div>
  );
}
