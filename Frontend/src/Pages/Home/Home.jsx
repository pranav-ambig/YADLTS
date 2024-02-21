import React from 'react'
import './Home.css'
import { useEffect, useState, useRef } from 'react'
import NET from 'vanta/dist/vanta.net.min'

const Home = () => {

  const [vantaEffect, setVantaEffect] = useState(null);
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
      <div className="titles">
          <h1 className='big'>Server Testing</h1>
          <h1 className='big has-gradient'>Redefined</h1>
      </div>

      <div className="titles">
        <h1 className='big'>Lalalala</h1>
        <h1 className='big has-gradient'>Lala</h1>
      </div>
    
    </div>
  )
}

export default Home