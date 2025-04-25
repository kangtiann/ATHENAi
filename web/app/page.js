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
import Task from '@mui/icons-material/Task';
import { useState } from 'react';
import {axiosGet} from './http';


export default function VisionPage() {
  const [visions, setVisions] = useState([])
  const [currentVision, setCurrentVision] = useState("")

  const [researchs, setResearchs] = useState([])
  const [currentResearch, setCurrentResearch] = useState("")

  const [deepthinks, setDeepthinks] = useState([])
  const [currentDeepthink, setCurrentDeepthink] = useState("")

  const [tasks, setTasks] = useState([])
  const [currentTask, setCurrentTask] = useState("")

  const fetchVisions = () => {
    axiosGet("/api/v1/vision/", (data) => {
      setVisions(data)
    }, (err) => {})
  }

  const fetchResearchs = (vision) => {
    var newVision = vision ? vision : currentVision
    if (newVision !== "") {
      axiosGet("/api/v1/research/?vision="+newVision, (data) => {
        setResearchs(data)
      }, (err) => {})
    } else {
      console.log("not set vision, skip fetchResearchs")
    }
  }

  const fetchDeepthinks = (research) => {
    var newResourch = research ? research : currentResearch
    if (newResourch !== "") {
      axiosGet("/api/v1/deepthink/?research="+newResourch, (data) => {
        setDeepthinks(data)
      }, (err) => {})
    } else {
      console.log("not set research, skip fetchResearchs")
    }
  }

  const fetchTasks = (deepthink) => {
    var newDeepthink = deepthink ? deepthink : currentDeepthink
    if (newDeepthink !== "") {
      axiosGet("/api/v1/task/?deepchink="+newDeepthink, (data) => {
        setTasks(data)
      }, (err) => {})
    } else {
      console.log("not set deepthink, skip fetchTasks")
    }
  }

  React.useEffect(() => {
    fetchVisions();
    fetchResearchs();
    fetchDeepthinks();
    fetchTasks();
  }, []);

  let visionListItems = visions.map((vision) => {
    var propose_time = new Date(vision.propose_time*1000).toLocaleDateString()
    return (
      <ListItemButton key={vision.id} selected={vision.id === currentVision}>
        <ListItemAvatar>
          <SportsScore />
        </ListItemAvatar>

        <ListItemText key={vision.id}
          primary={vision.vision} 
          secondary={ "🎯: "+propose_time}
          onClick={() => {
            console.log("click vision: "+vision.id)
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
    var propose_time = new Date(research.propose_time*1000).toLocaleDateString()
    return (
      <ListItemButton key={research.id} selected={research.id === currentResearch}>
        <ListItemAvatar>
          <Science />
        </ListItemAvatar>

        <ListItemText key={research.id}
          primary={research.research} 
          secondary={ "🕰️: "+propose_time}
          onClick={() => {
            console.log("click research: "+research.id)
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
    var propose_time = new Date(deepthink.propose_time*1000).toLocaleDateString()
    return (
      <ListItemButton key={deepthink.id} selected={deepthink.id === currentDeepthink}>
        <ListItemAvatar>
          <Psychology />
        </ListItemAvatar>

        <ListItemText key={deepthink.id}
          primary={deepthink.deepthink} 
          secondary={ "⏰: "+propose_time}
          onClick={() => {
            console.log("click research: "+deepthink.id)
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
    var propose_time = new Date(task.propose_time*1000).toLocaleDateString()
    return (
      <ListItemButton key={task.id} selected={task.id === currentTask}>
        <ListItemAvatar>
          <Task />
        </ListItemAvatar>

        <ListItemText key={task.id}
          primary={task.task_desc} 
          secondary={ "⏳: "+propose_time}
          onClick={() => {
            setCurrentTask(task.id)
          }}
        />
      </ListItemButton>
    )
  })

  return (
    <Box>
      <Grid container spacing={0}>
        <Grid size={2}>
          <List
          sx={{ width: '100%', bgcolor: 'background.paper' }}
          component="nav"
          subheader={<ListSubheader>Visions(愿景) - 永不停止</ListSubheader>}
          >
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
