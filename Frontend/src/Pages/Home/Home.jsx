import React from 'react'
import './Home.css'
import { useEffect, useState, useRef } from 'react'
import NET from 'vanta/dist/vanta.net.min'
import { motion } from "framer-motion"
import Laser from '../../Components/Laser/Laser'

const Home = () => {

  const draw = {
    hidden: { pathLength: 0, opacity: 0 },
    visible: (i) => {
      const delay = 1 + i * 0.5;
      return {
        pathLength: 1,
        opacity: 1,
        transition: {
          pathLength: { delay, type: "spring", duration: 1.5, bounce: 0 },
          opacity: { delay, duration: 0.01 }
        }
      };
    }
  };

  const [vantaEffect, setVantaEffect] = useState(null);
  const [mouseControls, setMouseControls] = useState(true);
  useEffect(() => {
    if (!vantaEffect) {
      setVantaEffect(NET({
        el: ".vanta-bg",
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1,
        scaleMobile: 1.00,
        color: 0x5a9dfc,
        backgroundColor: 0x110a1f,
        
      }))
    }
    return () => {
      if (vantaEffect) vantaEffect.destroy()
    }
  }, [vantaEffect])

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

      {/* <div className='blur-gradient'></div> */}

      <div className="infosec">

        {/* <div className="laser-ctn">
          <div className="bulb blas-shadow">
          </div>
          <motion.svg
            width="10"
            height="800"
            viewBox="0 0 10 800"
            initial="hidden"
            animate="visible"
            className='laser'
          >
            <motion.line
              x1={0}
              x2={0}
              y1={0}
              y2={800}
              stroke={'#47d4ff'}
              strokeWidth={10}
              cen
              custom={1}
          
            />
          </motion.svg>
        </div> */}
        <div className='laser-title-ctn'>
          {/* <img src='/images/createPage.png' className='bg-eg-image'></img> */}
          <Laser color='#47d4ff'></Laser>
          <div className="titles">
            <h1 className='med blastoise' id='customised-tests'>Customised Tests</h1>
            <h3 className="title-desc">
              Simulate sustained pressure or sudden traffic surges to assess your system's resilience.
            </h3>
            {/* <div className='cursor-trigger big'
              data-cursor-trigger="explore"
            >trigger</div> */}
          </div>
        </div>

        <div className='laser-title-ctn'>
          <Laser color='#fcdc3f'></Laser>
          <div className="titles">
            <h1 className='med pikachu'>In-Depth Analysis</h1>
            <h3 className="title-desc">
              Gain comprehensive metrics and reports to analyze your test results effectively.
            </h3>

          </div>
        </div>

        <div className='laser-title-ctn'>
          <Laser color='#84ff57'></Laser>
          <div className="titles">
            <h1 className='med venusaur'>Distributed Testing</h1>
            <h3 className="title-desc">            
              Stress test your web server with Poké-powered load testing!
            </h3>
          </div>
        </div>

        <div className='laser-title-ctn'>
          <Laser color='#ff894a'></Laser>
          <div className="titles">
            <h1 className='med charizard'>Impressive Throughput</h1>
            <h3 className="title-desc">
              Push your platform to its limits, simulating up to 500 requests per node.
            </h3>
          </div>
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