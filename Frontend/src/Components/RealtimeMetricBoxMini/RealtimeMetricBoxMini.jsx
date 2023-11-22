import { useEffect, useState } from "react";
import { socket } from "../../App";
import './RealtimeMetricsMini.css'

const RealtimeMetricBox = (props) =>{

    const [Stats, setStats] = useState({})

    const round = (x) =>{
        if (x === undefined) return 0.0
        return (Math.round(x * 1000) / 1000)
    }

    useEffect(()=>{
        socket.on(props.name, data => {
            setStats(data["metrics"])
        })
    })
    return (
        <div className='RealtimeMetricBoxMini'>
          {props.miniMode?<></>:<h2 id="stat-title-mini">Stats</h2>}
          <div className="stats-mini">
            <h4>Mean</h4>
            <h4>{round(Stats["Mean"])} ms</h4>
            <h4>Median</h4>
            <h4>{round(Stats["Median"])} ms</h4>
            <h4>Mode</h4>
            <h4>{round(Stats["Mode"])} ms</h4>
            <h4>Min</h4>
            <h4>{round(Stats["Min"])} ms</h4>
            <h4>Max</h4>
            <h4>{round(Stats["Max"])} ms</h4>
            <h4>Requests</h4>
            <h4>{round(Stats["Requests"])}</h4>
          </div>
        </div>
    )
}

export default RealtimeMetricBox;