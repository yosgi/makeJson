import "./styles.css";
import React, { useState } from "react";
import ListItem from "@material-ui/core/ListItem";
import List from "@material-ui/core/List";
import ListItemText from "@material-ui/core/ListItemText";
import Button from "@material-ui/core/Button";
import Drawer from "@material-ui/core/Drawer";
import Dialog from "@material-ui/core/Dialog";
import Box from "@material-ui/core/Box";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import { Theme, createStyles, makeStyles } from "@material-ui/core/styles";

import ListComponent from "./components/list";
import TableComponent from "./components/table";
import BannerComponent from "./components/banner";
import LinkComponent from "./components/links";
import RenderLink from "./components/renderLink";
import { menuList } from "./data";
import RenderList from "./components/renderList";
import RenderBanner from "./components/renderBanner";
import RenderTable from "./components/renderTable";
import UploadButton from "./components/importJson";
import toJson from "./utils/exportJSON";
import useStore from "./utils/useStorage";
const ComponentInModal = function (props: any) {
  let { type } = props;
  if (type.toUpperCase().indexOf("LIST") > -1) {
    return <ListComponent {...props}></ListComponent>;
  } else if (type.toUpperCase().indexOf("BANNER") > -1) {
    return <BannerComponent {...props}></BannerComponent>;
  } else if (type.toUpperCase().indexOf("TABLE") > -1) {
    return <TableComponent {...props}></TableComponent>;
  } else if (type.toUpperCase().indexOf("LINK") > -1) {
    return <LinkComponent {...props}></LinkComponent>;
  }
};
const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    dialog: {
      width: 500
    },

    imageList: {
      width: 500,
      height: 450
    },
    drawer: {
      width: 100,
      marginLeft: 20
    },
    addButton: {
      position: "fixed",
      top: 10,
      right: 150,
      width: 100
    },
    importButton: {
      position: "fixed",
      top: 70,
      right: 150,
      width: 100
    },
    exportButton: {
      position: "fixed",
      top: 70,
      right: 30,

      width: 100
    },
    clearButton: {
      position: "fixed",
      top: 10,
      right: 30,
      width: 100
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
  } else if (v.toUpperCase().indexOf("LINK") > -1) {
    return <RenderLink data={exportObj[v]}></RenderLink>;
  }
  return <div>模块定义出错</div>;
}
export default function App() {
  const classes = useStyles();
  // const [exportObj, setObj]: any = useState(null);
  const [DrawerState, setDawerState] = useState(false);
  const [showDialog, setDialog] = useState(false);
  const [current, setCurrent] = useState("");
  const [editting, setEditting] = useState(null);
  const [storedValue, setValue] = useStore("json", {});
  const toggleDrawer = (open: boolean) => {
    setDawerState(open);
  };

  const tabSelected = (tab: string) => {
    setCurrent(tab);
    toggleDrawer(false);
    setDialog(true);
  };
  const findTypeName: any = (type: string) => {
    if (storedValue[type]) {
      return findTypeName(type + "-1");
    }
    return type;
  };
  const addObj = (type: string, obj: any) => {
    let typeName = findTypeName(type);
    storedValue[typeName] = obj;
    setValue(storedValue);
  };
  const editObj = (type: string, obj: any) => {
    storedValue[type] = obj;
    setValue(storedValue);
    setCurrent("");
    setEditting(null);
  };
  const exportJSON = (json: any) => {
    toJson(json);
  };
  const handleDelete = (key: any) => {
    let newObj: any = { ...storedValue };
    delete newObj[key];
    setValue(newObj);
  };
  const handleEdit = (key: any) => {
    setCurrent(key);
    setEditting(storedValue[key]);

    setDialog(true);
  };

  console.log(storedValue);
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
        onClick={() => setValue({})}
        variant="contained"
        color="primary"
        className={classes.clearButton}
      >
        清空模块
      </Button>
      <Button
        onClick={() => exportJSON(storedValue)}
        color="primary"
        variant="contained"
        className={classes.exportButton}
      >
        导出Json
      </Button>
      <UploadButton
        className={classes.importButton}
        setObj={setValue}
      ></UploadButton>
      {storedValue &&
        Object.keys(storedValue).map((v, index) => {
          return (
            <Card className={classes.card} key={index}>
              <Typography className={classes.title}>
                {v.toUpperCase()}
              </Typography>
              <CardContent>{chooseComponent(v, storedValue)}</CardContent>
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
