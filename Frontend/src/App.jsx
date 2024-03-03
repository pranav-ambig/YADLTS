import './Reset.css'
import './App.css'
import SideBar from './Components/SideBar/SideBar'
import DashBoard from './Pages/DashBoard/DashBoard'
import Create from './Pages/Create/Create'
import NavBar from './Components/NavBar/NavBar'
import { io } from 'socket.io-client'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import History from './Pages/History/History'
import { useEffect, useState } from 'react'
import axios from 'axios'
import Home from './Pages/Home/Home'


export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
console.log('test', BACKEND_URL)

const socket = io(BACKEND_URL, {
    withCredentials: true,
    extraHeaders: {
      'Access-Control-Allow-Origin': 'http://localhost:5173',
    },
});

function App() {

  const [testID, setTestID] = useState("--");

  const handleVisibilityChange = ()=>{

    if (testID === '--') {
      return
    }
    if (document.visibilityState === 'hidden'){
      axios.post(BACKEND_URL+'/timeout', {
        test_id: testID,
        active: "NO"
      })
    }
    else {
      axios.post(BACKEND_URL+'/timeout', {
        test_id: testID,
        active: "YES"
      })
    }
  }

  useEffect(()=>{
    document.addEventListener('visibilitychange', handleVisibilityChange)
    return ()=>{
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [testID])

  const moveMouseShine = (e)=>{

    let x = e.clientX;
    let y = e.clientY;

    let mouseShine = document.getElementById('mouse-shine');
    let closest = e.target.closest('a,input,select')

    let translationKeyframes = {
      transform: `translate(${x}px, ${y}px)`,
      width: `25px`,
      height: `25px`,
      borderRadius: `50%`,
      opacity: 0.6,
      // backdropFilter: 'blur(10px)'
    }
    
    if (closest){
      let targetWidth = closest.offsetWidth;
      let targetHeight = closest.offsetHeight;
      let targetX = closest.offsetLeft + (targetWidth/2);
      let targetY = closest.offsetTop + (targetHeight/2);
      let targetBorderRadius =  getComputedStyle(closest).borderRadius;
      // console.log(closest.style)

      // let adaptationKeyframes = {
      //   width: `${targetWidth+20}px`,
      //   height: `${targetHeight+20}px`,
      //   borderRadius: `10px`,
      //   opacity: 0.2,
      // }
      // mouseShine.animate(adaptationKeyframes, {
      //   duration: 200,
      // })

      translationKeyframes = {
        transform: `translate(${x}px, ${y}px)`,
        width: `${targetWidth+20}px`,
        height: `${targetHeight+20}px`,
        borderRadius: `max(10px,${targetBorderRadius})`,
        transform: `translate(${targetX}px, ${targetY}px)`,
        opacity: 0.1,
        filter: 'none'
      }

    }

    mouseShine.animate(translationKeyframes, {
      duration: 200,
      fill: 'forwards',
    })
  }

  useEffect(()=>{
    document.addEventListener('mousemove', moveMouseShine)
    document.addEventListener('scroll', moveMouseShine)
    document.addEventListener('wheel', moveMouseShine)

    return ()=>{
      document.removeEventListener('mousemove', moveMouseShine)
      document.removeEventListener('scroll', moveMouseShine)
      document.removeEventListener('wheel', moveMouseShine)
    }

  }, [])



  return (
    <div className='App'>
      <div id='mouse-shine'></div>
      <div className='routed-comp'>
        <BrowserRouter>
          <NavBar></NavBar>
          <Routes>
            <Route path='/' element={<Home></Home>}></Route>
            <Route path='/create' element={<Create testID={testID} setTestID={setTestID} ></Create>}></Route>
            <Route path='/view' element={<DashBoard testID={testID} setTestID={setTestID} ></DashBoard>}></Route>
            <Route path='/history' element={<History></History>}></Route>
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  )
}

export default App
export {socket}
