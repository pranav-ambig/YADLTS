import React from 'react'
import './Laser.css'
import { motion } from "framer-motion"

const Laser = ({color}) => {

  const draw = {
    hidden: { pathLength: 0 },
    visible: {
      pathLength: 1,
      transition: {delay: 0.1 ,type: "spring", duration: 2 }
    }
  };

  return (
    <div className="laser-ctn">
        <motion.div 
          className="bulb blas-shadow" 
          initial={{
                    opacity: 0,
                    backgroundColor: '#aaaaaa',
                    boxShadow: `0px 0px 20px ${color}, 0px 0px 25px ${color}`}}
          whileInView={{
                    opacity: 1,
                    backgroundColor: color,
                    boxShadow: `0px 0px 20px ${color}, 0px 0px 25px ${color}`,
                    transition: {delay: 0.1 ,type: "spring", duration: 2 }
                  }}
          viewport={{once: true}}
        
        >
        </motion.div>
        <motion.svg
          width="10"
          height="800"
          viewBox="0 0 10 800"
          className='laser'
          initial='hidden'
          whileInView='visible'
          variants={draw}
          viewport={{once: true}}
        >
          <motion.line
            x1={0}
            x2={0}
            y1={0}
            y2={800}
            stroke={color}
            strokeWidth={10}
            variants={draw}
          />
        </motion.svg>
    </div>
  )
}

export default Laser