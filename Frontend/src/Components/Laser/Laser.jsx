import React from 'react'
import './Laser.css'
import { motion } from "framer-motion"

const Laser = ({color}) => {
  return (
    <div className="laser-ctn">
        <div className="bulb blas-shadow" style={{
            backgroundColor: color,
            boxShadow: `0px 0px 20px ${color}, 0px 0px 25px ${color}`
        }}>
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
            stroke={color}
            strokeWidth={10}
            cen
            custom={1}
        
        />
        </motion.svg>
    </div>
  )
}

export default Laser