import React from 'react'
import './Home.css'
import { useEffect, useState, useRef } from 'react'
import NET from 'vanta/dist/vanta.net.min'
import { motion } from "framer-motion"
import Laser from '../../Components/Laser/Laser'
import InfosecTitle from '../../Components/InfosecTitle/InfosecTitle'

const Home = () => {

  const [vantaEffect, setVantaEffect] = useState(null);
  const [vantaOn, setVantaOn] = useState(false);
  
  useEffect(() => {
    setVantaOn(true)
  }, [])

  useEffect(()=>{
    if (vantaOn) {
      setVantaEffect(NET({
        el: ".vanta-bg",
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 100.00,
        minWidth: 100.00,
        scale: 1.2,
        scaleMobile: 1.2,
        color: 0x5a9dfc,
        backgroundColor: 0x110a1f,
        
      }))
      setVantaOn(true)
    }
    else {
      setVantaEffect(null)
    }
    return () => {
      if (vantaEffect) vantaEffect.destroy()
    }
  }, [vantaOn])

  // const vantaHandler = (e)=>{
  //   let scrollPos = e.offsetTop;
  //   let windowHeight = window.innerHeight;
  //   console.log(scrollPos, windowHeight)
  //   if (scrollPos > windowHeight) {
  //     setVantaOn(false);
  //   }
  //   else {
  //     if (!vantaOn){
  //       setVantaOn(true)
  //     }
  //   }
  // }


  return (
    <div className='Home'>
      <div className='vanta-bg'></div>

      <div className="main-title">
        <h1 className='big' >Server Testing</h1>
        <h1 className='big has-gradient'>Redefined.</h1>
      </div>


      <div className='cursor-trigger big'
        data-cursor-trigger="explore"
      >trigger</div>

      <div className="infosec">
        <div className='laser-title-ctn'>
          <Laser color='#47d4ff'></Laser>
          <InfosecTitle 
            title='Customised Tests'
            desc="Simulate sustained pressure or sudden traffic surges to assess your system's resilience."
            titleId='customised-tests'
            color='blastoise'
          ></InfosecTitle>
        </div>

        <div className='laser-title-ctn'>
          <Laser color='#fcdc3f'></Laser>
          <InfosecTitle 
            title='In-Depth Analysis'
            desc="Gain comprehensive metrics and reports to analyze your test results effectively."
            titleId='in-dep-an'
            color='pikachu'
          ></InfosecTitle>
        </div>


        <div className='laser-title-ctn'>
          <Laser color='#84ff57'></Laser>
          <InfosecTitle 
            title='Distributed Testing'
            desc="Stress test your web server with Poké-powered load testing!"
            titleId='dist-test'
            color='venusaur'
          ></InfosecTitle>
        </div>

        <div className='laser-title-ctn'>
          <Laser color='#ff894a'></Laser>
          <InfosecTitle 
            title='Impressive Throughput'
            desc="Push your platform to its limits, simulating up to 500 requests per node."
            titleId='imp-through'
            color='charizard'
          ></InfosecTitle>
        </div>
      </div>
      
      <footer>
        <div className="footer-links">
          <img src="/horizontal_logo.png" className='horz-logo' data-cursor-trigger="logo"/>
          <div className="links">
            <a>About</a>
            <a>Contacts</a>
          </div>

        </div>

        <div className="seperator"></div>

        <div className="address-links">
          <div className="footer-addr">
            <p>Bengaluru, India</p>
            <p></p>
            <p></p>
            <p>BSK III Stage</p>
            <p>560085</p>
          </div>

          <div className="footer-socials">
            <a>Instagram</a>
            <a>LinkedIn</a>
            <a>GitHub</a>
          </div>
        </div>

        <div className="final">
          <p>Made with ❤️ by Pranav and Rahul</p>
          <p>© All rights reserved</p>
        </div>

      </footer>
    
    </div>
  )
}

export default Home