'use client'

import * as React from 'react';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import ListSubheader from '@mui/material/ListSubheader';
import Switch from '@mui/material/Switch';
import SportsScore from '@mui/icons-material/SportsScore';
import Science from '@mui/icons-material/Science';
import Psychology from '@mui/icons-material/Psychology';
import AddIcon from '@mui/icons-material/Add';
import Task from '@mui/icons-material/Task';
import { useState } from 'react';
import { axiosGet, axiosPost } from './http';

import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import Menu from '@mui/icons-material/Menu';
import AlarmIcon from '@mui/icons-material/Alarm';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import Fab from '@mui/material/Fab';
import { Add } from '@mui/icons-material';

import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';

import SendIcon from '@mui/icons-material/Send';
import Snackbar from '@mui/material/Snackbar';


export default function VisionPage() {
  const [visions, setVisions] = useState([])
  const [currentVision, setCurrentVision] = useState("")

  const [researchs, setResearchs] = useState([])
  const [currentResearch, setCurrentResearch] = useState("")

  const [deepthinks, setDeepthinks] = useState([])
  const [currentDeepthink, setCurrentDeepthink] = useState("")

  const [tasks, setTasks] = useState([])
  const [currentTask, setCurrentTask] = useState("")

  const [message, setMessage] = useState({ open: false, msg: "" })

  const isIdExists = (id, array) => {
    let exists = false
    for (let item in array) {
      if (item.id === id) {
        exists = true
        break
      }
    }
    return exists
  }

  const fetchVisions = () => {
    axiosGet("/api/v1/vision/", (data) => {
      setVisions(data)
      if (isIdExists(currentVision, data) === false) {
        setCurrentVision("")
      }
    }, (err) => { })
  }

  const fetchResearchs = (vision) => {
    var newVision = vision ? vision : currentVision
    if (newVision !== "") {
      axiosGet("/api/v1/research/?vision=" + newVision, (data) => {
        setResearchs(data)
        if (isIdExists(currentResearch, data) === false) {
          setCurrentResearch("")
          setCurrentDeepthink("")
          setCurrentTask("")
          setDeepthinks([])
          setTasks([])
        }
      }, (err) => { })
    } else {
      console.log("not set vision, skip fetchResearchs")
    }
  }

  const fetchDeepthinks = (research) => {
    var newResourch = research ? research : currentResearch
    if (newResourch !== "") {
      axiosGet("/api/v1/deepthink/?research=" + newResourch, (data) => {
        setDeepthinks(data)
        if (isIdExists(currentDeepthink, data) === false) {
          setCurrentDeepthink("")
          setCurrentTask("")
          setTasks([])
        }
      }, (err) => { })
    } else {
      console.log("not set research, skip fetchResearchs")
    }
  }

  const fetchTasks = (deepthink) => {
    var newDeepthink = deepthink ? deepthink : currentDeepthink
    if (newDeepthink !== "") {
      axiosGet("/api/v1/task/?deepchink=" + newDeepthink, (data) => {
        setTasks(data)
        if (isIdExists(currentTask, data) === false) {
          setCurrentTask("")
        }
      }, (err) => { })
    } else {
      console.log("not set deepthink, skip fetchTasks")
    }
  }

  const newVision = (data) => {
    console.log("newVision: " + data.vision)
    axiosPost("/api/v1/vision/", data,
      () => {
        setMessage({ open: true, msg: "新建Vision（愿景）成功" })
        fetchVisions()
      },
      (err) => { setMessage({ open: true, msg: "新建Vison（愿景）失败" + err }) })
  }

  React.useEffect(() => {
    fetchVisions();
    fetchResearchs();
    fetchDeepthinks();
    fetchTasks();
  }, []);

  let visionListItems = visions.map((vision) => {
    var propose_time = new Date(vision.propose_time * 1000).toLocaleDateString()
    return (
      <ListItemButton key={vision.id} selected={vision.id === currentVision}>
        <ListItemAvatar>
          <SportsScore />
        </ListItemAvatar>

        <ListItemText key={vision.id}
          primary={vision.vision}
          secondary={"🎯: " + propose_time}
          onClick={() => {
            console.log("click vision: " + vision.id)
            setCurrentVision(vision.id);
            fetchResearchs(vision.id);
          }}
        />

        <Switch
          edge="end"
          checked={vision.status != "suspend"}
        />
      </ListItemButton>
    )
  })

  let researchListItems = researchs.map((research) => {
    var propose_time = new Date(research.propose_time * 1000).toLocaleDateString()
    return (
      <ListItemButton key={research.id} selected={research.id === currentResearch}>
        <ListItemAvatar>
          <Science />
        </ListItemAvatar>

        <ListItemText key={research.id}
          primary={research.research}
          secondary={"🕰️: " + propose_time}
          onClick={() => {
            console.log("click research: " + research.id)
            setCurrentResearch(research.id);
            fetchDeepthinks(research.id);
          }}
        />

        <Switch
          edge="end"
          checked={research.status != "suspend"}
        />
      </ListItemButton>
    )
  })

  let deepthinkListItems = deepthinks.map((deepthink) => {
    var propose_time = new Date(deepthink.propose_time * 1000).toLocaleDateString()
    return (
      <ListItemButton key={deepthink.id} selected={deepthink.id === currentDeepthink}>
        <ListItemAvatar>
          <Psychology />
        </ListItemAvatar>

        <ListItemText key={deepthink.id}
          primary={deepthink.deepthink}
          secondary={"⏰: " + propose_time}
          onClick={() => {
            console.log("click research: " + deepthink.id)
            setCurrentDeepthink(deepthink.id)
            fetchTasks(deepthink.id)
          }}
        />

        <Switch
          edge="end"
          checked={deepthink.status != "suspend"}
        />
      </ListItemButton>
    )
  })

  let taskListItems = tasks.map((task) => {
    var propose_time = new Date(task.propose_time * 1000).toLocaleDateString()
    return (
      <ListItemButton key={task.id} selected={task.id === currentTask}>
        <ListItemAvatar>
          <Task />
        </ListItemAvatar>

        <ListItemText key={task.id}
          primary={task.task}
          secondary={"⏳: " + propose_time}
          onClick={() => {
            setCurrentTask(task.id)
          }}
        />
      </ListItemButton>
    )
  })

  return (
    <Box>
      <Snackbar
        open={message.open}
        autoHideDuration={5000}
        message={message.msg}
      />
      <Grid container spacing={0}>
        <Grid size={2}>
          <List
            sx={{ width: '100%', bgcolor: 'background.paper' }}
            component="nav"
            subheader={<ListSubheader>Visions(愿景) - 永不停止</ListSubheader>}
          >
            <Stack direction="row" spacing={1}>
              {newFormModal("vision", "Vision(愿景)", newVision)}
            </Stack>

            {visionListItems}
          </List>
        </Grid>

        <Grid size={3}>
          <List
            sx={{ width: '100%', bgcolor: 'background.paper' }}
            component="nav"
            subheader={<ListSubheader>Research(研究) - 月级</ListSubheader>}
          >
            {researchListItems}
          </List>
        </Grid>

        <Grid size={3}>
          <List
            sx={{ width: '100%', bgcolor: 'background.paper' }}
            component="nav"
            subheader={<ListSubheader>Deepthink(深度思考) - 小时级</ListSubheader>}
          >
            {deepthinkListItems}
          </List>
        </Grid>

        <Grid size={4}>
          <List
            sx={{ width: '100%', bgcolor: 'background.paper' }}
            component="nav"
            subheader={<ListSubheader>Task(任务) - 分钟级</ListSubheader>}
          >
            {taskListItems}
          </List>
        </Grid>
      </Grid>

    </Box>
  );
}


export function newFormModal(newWhat, desc, onSubmit) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 800,
    maxWidth: '100%',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  return (
    <Box>
      <IconButton color="primary" aria-label="add" onClick={handleOpen}>
        <AddIcon />
      </IconButton>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Box
            component="form"
            noValidate
            autoComplete="off"
          >
            <Typography variant="h4" gutterBottom>
              添加新的 {desc}
            </Typography>
            <TextField id={"input-" + newWhat} label={desc} variant="standard" style={{ width: "100%", marginBottom: "10px" }} />
            <TextField multiline rows={4} id={"input-desc-" + newWhat} label={desc + " 详细描述"} variant="standard" style={{ width: "100%", marginBottom: "20px" }} />

            <Stack direction="row" spacing={2}>
              <Button variant="contained" endIcon={<SendIcon />} onClick={
                () => {
                  let title = document.getElementById("input-" + newWhat).value;
                  let desc = document.getElementById("input-desc-" + newWhat).value;
                  onSubmit({ [newWhat]: title, [newWhat + "_desc"]: desc });
                }
              }>
                提交
              </Button>
            </Stack>
          </Box>
        </Box>
      </Modal>
    </Box>
  );
}