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

  }, [])

  return (
    <div className='App'>
      <SideBar></SideBar>
      <div className='routed-comp'>
        <BrowserRouter>
          <NavBar></NavBar>
          <Routes>
            <Route path='/' element={<Create testID={testID} setTestID={setTestID} ></Create>}></Route>
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
