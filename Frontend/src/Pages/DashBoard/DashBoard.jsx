import './DashBoardStyle.css'
import RealtimeChart from '../../Components/RealtimeChart/RealtimeChart';
import { useState, useEffect } from 'react'
import axios from "axios"
import RealtimeMetricBox from '../../Components/RealtimeMetricBox/RealtimeMetricBox';
import RealtimeMetricBoxMini from '../../Components/RealtimeMetricBoxMini/RealtimeMetricBoxMini'
import { BACKEND_URL } from '../../App';

const DashBoard = (props) => {

  const {testID, setTestID} = props
  const [availableDrivers, setAvailabeDrivers] = useState(0);
  const [TestStatus, setTestStatus] = useState("Idle");

  const [miniCharts, setMiniCharts] = useState(<></>);

  useEffect(()=>{
    // setInterval(()=>{
      axios.get(BACKEND_URL+'/driver_ids')
      .then((res)=>{
        if (availableDrivers == 0 && res["data"]["driver_ids"].length > 0){
          // console.log(availableDrivers, res["data"]["driver_ids"].length)
          setAvailabeDrivers(res["data"]["driver_ids"].length)
  
          setMiniCharts(
            <div className='MiniCharts'>
              {res["data"]["driver_ids"].map((pokemon, i)=>{
                return(
                <div key={i} className='ChartBlock'>
                  <div className="img-ctn">
                    <img src={`\\public\\${pokemon}.gif`}></img>
                  </div>
                  <RealtimeMetricBoxMini name={pokemon} miniMode={true}></RealtimeMetricBoxMini>
                  <RealtimeChart color='#EC8F5E' name={pokemon}></RealtimeChart>
                </div>
                )
              })}
            </div>
          )
        }
        else if (res["data"]["driver_ids"].length == 0) {
          setAvailabeDrivers(0)
          setMiniCharts(<></>)
          setTestID('--')
        }
      })
      .catch(()=>{})
    // }, 500)
  }, [availableDrivers])
  
  return (
    <div className="DashBoard">
      <div className='dash-spacer'></div>
      <h3>Test ID: {testID}</h3>
      <div className="MainChartMetrics">
        <div className="MainChart">
          {/* <h2>Status: {TestStatus}</h2> */}
          <RealtimeChart color='#ffffff' name='test_metrics' bigChart={true}></RealtimeChart>
        </div>
        <div className="MainMetrics">
          <RealtimeMetricBox miniMode={false} name='test_metrics'></RealtimeMetricBox>
        </div>

      </div>
      {miniCharts}

    </div>
  );
}

export default DashBoard
