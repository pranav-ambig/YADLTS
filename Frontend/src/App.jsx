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
import { createContext } from 'react'


export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
// console.log('test', BACKEND_URL)

const socket = io(BACKEND_URL, {
    withCredentials: true,
    extraHeaders: {
      'Access-Control-Allow-Origin': 'http://localhost:5173',
    },
});

// const exploreDiv = 
// <div className="explorediv">

// </div>

const custTestsScoller = ()=>{
  let custTests = document.getElementById('customised-tests')
  custTests.scrollIntoView({behavior: 'smooth', block: 'center'})
}

export const globalContext = createContext({});

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
    let closestElement = e.target.closest('*')

    let translationKeyframes = {
      transform: `translate(${x}px, ${y}px)`,
      width: `25px`,
      height: `25px`,
      borderRadius: `50%`,
      opacity: 0.6,
      zIndex: 10,
      filter: 'none',
      mixBlendMode: 'normal',
    }

    let cursorTriggerValue = closestElement.getAttribute('data-cursor-trigger')

    if (cursorTriggerValue !== null){

      let targetWidth = closestElement.offsetWidth;
      let targetHeight = closestElement.offsetHeight;
      let targetX = closestElement.offsetLeft + (targetWidth/2);
      let targetY = closestElement.offsetTop + (targetHeight/2);

      if (cursorTriggerValue == 'logo'){
        translationKeyframes = {
          transform: `translate(${x}px, ${y}px)`,
          width: `50px`,
          height: `50px`,
          borderRadius: `100%`,
          transform: `translate(${x}px, ${y}px)`,
          opacity: 1,
          zIndex: 10,
          mixBlendMode: 'difference',
        }
      }
      else if (cursorTriggerValue == 'explore') {
        translationKeyframes = {
          transform: `translate(${x}px, ${y}px)`,
          width: `100px`,
          height: `100px`,
          borderRadius: `100%`,
          transform: `translate(${x}px, ${y}px)`,
          opacity: 1,
          zIndex: 10,
        }
        if (mouseShine.childElementCount == 0){

          document.addEventListener('click', custTestsScoller)

          let exploreElement = document.createElement('div')
          exploreElement.id = 'explore-div'
          exploreElement.classList.add('explore-div')

          let exploreH3 = document.createElement('h3')
          exploreH3.innerHTML = 'Explore'
          exploreH3.classList.add('explore-h3')
          

          let exploreDownIcon = document.createElement('div')
          exploreDownIcon.innerHTML = '<i class="fa-solid fa-arrow-down"></i>'

          exploreElement.appendChild(exploreH3)
          exploreElement.appendChild(exploreDownIcon)

          mouseShine.appendChild(exploreElement)
        }
      }
    }
    else {
      if (mouseShine.childElementCount == 1){
        mouseShine.removeChild(document.getElementById('explore-div'))
        document.removeEventListener('click', custTestsScoller)
      }
    }


    if (closest){

      let boundingRect = closest.getBoundingClientRect()

      let targetWidth = closest.offsetWidth;
      let targetHeight = closest.offsetHeight;
      let targetX = boundingRect.left + (targetWidth/2);
      let targetY = boundingRect.top + (targetHeight/2);
      let targetBorderRadius =  getComputedStyle(closest).borderRadius;

      translationKeyframes = {
        transform: `translate(${x}px, ${y}px)`,
        width: `${targetWidth+20}px`,
        height: `${targetHeight+20}px`,
        borderRadius: `max(10px,${targetBorderRadius})`,
        transform: `translate(${targetX}px, ${targetY}px)`,
        opacity: 0.1,
        zIndex: 10,
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
    <globalContext.Provider value={{testID, setTestID}}>
      <div className='App'>
        <div id='mouse-shine'></div>
        <div className='routed-comp'>
          <BrowserRouter>
            <NavBar></NavBar>
            <Routes>
              <Route path='/' element={<Home></Home>}></Route>
              <Route path='/create' element={<Create ></Create>}></Route>
              <Route path='/view' element={<DashBoard ></DashBoard>}></Route>
              <Route path='/history' element={<History></History>}></Route>
            </Routes>
          </BrowserRouter>
        </div>
      </div>
    </globalContext.Provider>
  )
}

export default App
export {socket}
