import './Reset.css'
import './App.css'
import SideBar from './Components/SideBar/SideBar'
import DashBoard from './Pages/DashBoard/DashBoard'
import Create from './Pages/Create/Create'
import NavBar from './Components/NavBar/NavBar'
import { io } from 'socket.io-client'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import History from './Pages/History/History'

const socket = io('http://127.0.0.1:5000', {
    withCredentials: true,
    extraHeaders: {
      'Access-Control-Allow-Origin': 'http://localhost:5173',
    },
});

function App() {

  return (
    <div className='App'>
      <SideBar></SideBar>
      <div className='routed-comp'>
        <BrowserRouter>
          <NavBar></NavBar>
          <Routes>
            <Route path='/' element={<Create></Create>}></Route>
            <Route path='/view' element={<DashBoard></DashBoard>}></Route>
            <Route path='/history' element={<History></History>}></Route>
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  )
}

export default App
export {socket}