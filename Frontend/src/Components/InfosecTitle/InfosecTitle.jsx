import React from 'react'
import './InfosecTitle.css'
import { motion } from "framer-motion"

const InfosecTitle = ({title, desc, titleId, color}) => {
  return (
    <div 
      className="titles"  
    >
      <motion.h1 
        className={'med '+color}
        id={titleId}
        initial={{opacity: 0, translateX: '-10%'}}
        whileInView={{opacity: 1, translateX: '0%'}}
        transition={{duration: 0.3, ease: 'easeInOut'}}
      >
        {title}
      </motion.h1>

      <motion.h3 
        className="title-desc"
        initial={{opacity: 0, translateX: '-10%'}}
        whileInView={{opacity: 1, translateX: '0%'}}
        transition={{delay: 0.3, duration: 0.3, ease: 'easeInOut'}}
      >
        {desc}
      </motion.h3>
    </div>
  )
}

export default InfosecTitle