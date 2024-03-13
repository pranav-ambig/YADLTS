import { useEffect, useState } from 'react'
import './SideBarStyle.css'
import axios from "axios"
import { BACKEND_URL } from '../../App';


const SideBar = () => {

  const [availableDrivers, setAvailabeDrivers] = useState(0);
  const [pokemons, setPokemons] = useState(<></>);
    
  useEffect(()=>{
    setInterval(()=>{
      axios.get(BACKEND_URL+'/driver_ids')
      .then((res)=>{
        if (availableDrivers == 0 && res["data"]["driver_ids"].length > 0){
          setAvailabeDrivers(res["data"]["driver_ids"].length)
  
          setPokemons(
            <div className='links'>
              {res["data"]["driver_ids"].map((pokemon, i)=>{
                return (
                  <p className={pokemon} key={i}>{pokemon}</p>
                )
              })}
            </div>
          )
        }
        else if (res["data"]["driver_ids"].length == 0) {
          setAvailabeDrivers(0)
          setPokemons(<></>)
        }
      }
      ).catch(()=>{})
    }, 250)
  }, [])

    return (
      <div className="SideBar">
        <div className="blurred"></div>
        <div className="pokemons">
        {pokemons}
        </div>
        {/* <div className="links">
          <a className='char'>Charizard</a>
          <a className='blas'>Blastoise</a>
          <a className='venu'>Venusaur</a>
          <a className='zap'>Tentacruel</a>
          <a className='pika'>Pikachu</a>
        </div> */}

      </div>
    )

}

export default SideBar
