import { useState } from 'react';
import './Create.css'
import axios from "axios"
import { useNavigate } from 'react-router-dom';
import { BACKEND_URL } from '../../App';
import SideBar from '../../Components/SideBar/SideBar';
import NavBar from '../../Components/NavBar/NavBar';

// TODO: Limit max throughput to 5

const Create = (props)=>{

    const [DelThrSwitchLabel, setDelThrSwitchLabel] = useState(<h2>Throughput</h2>);
    const [DelThrSwitchInp, setDelThrSwitchInp] = useState(<input type='number' min={0} id='throughput'></input>);
    const [ConfigSent, setConfigSent] = useState(false);

    const navigate = useNavigate();
    
    let {testID, setTestID} = props

    const sendTestData = ()=>{
        let server_url = document.getElementById('server-url')
        let test_type = document.getElementById('select-sw')
        let delay = (document.getElementById('delay') != null)? document.getElementById('delay').value : 0
        let throughput = (document.getElementById('throughput') != null)? document.getElementById('throughput').value : 0
        let numDrivers = document.getElementById('numDrivers').value


        // console.log({server_url, test_type, delay, throughput, numDrivers})

        console.log(
            {
                "test_type": test_type.options[test_type.selectedIndex].text,
                "test_message_delay": Number(delay),
                "message_count_per_driver": Number(throughput),
                "num_drivers": Number(numDrivers),
                "server_url": server_url.value
            }
        )
        
        document.body.style.cursor = 'wait'
        axios.post(BACKEND_URL+'/test_config', 
            {
            "test_type": test_type.options[test_type.selectedIndex].text,
            "test_message_delay": Number(delay),
            "message_count_per_driver": Number(throughput),
            "num_drivers": Number(numDrivers),
            "server_url": server_url.value
            }
        )
        .then(res=>{
            // console.log('submitted', drivers)
            setTestID(res["data"]["test_id"])
            setConfigSent(true)
            document.body.style.cursor = 'default'
        })
    }

    const trigger = ()=>{
        axios.post(BACKEND_URL+'/trigger', 
          {
            "test_id": testID
          }
        ).then((res)=>{console.log(res)})
        navigate('/view')
      }


    const updateDelThrSwitch = ()=>{
        let sw = document.getElementById('select-sw')
        // console.log(sw.selectedIndex)
        if (sw.options[sw.selectedIndex].text == "TSUNAMI"){
            setDelThrSwitchLabel(<h2>Delay</h2>)
            setDelThrSwitchInp(<input type='number' min={1} id='delay'></input>)
        }
        else {
            setDelThrSwitchLabel(<h2>Throughput</h2>)
            setDelThrSwitchInp(<input type='number' min={1} id='throughput'></input>)
        }
    }

    return (
        <div className="Create">
            {/* <NavBar></NavBar> */}
            <SideBar></SideBar>
            <h1 className='title'>New Load Test</h1>
            <div className="controls">
                <div className="form">
                    <h2>Server URL</h2>
                    <input type='text' id='server-url'></input>
                    <h2>Test Type</h2>
                    <select onChange={updateDelThrSwitch} id='select-sw'>
                        <option>AVALANCHE</option>
                        <option>TSUNAMI</option>
                    </select>
                    {DelThrSwitchLabel}
                    {DelThrSwitchInp}
                    <h2>Drivers</h2>
                    <input type='number' min={0} max={2} id='numDrivers'></input>
                </div>
                <div className='actions'>
                    <h1 className='wrappable' onClick={(ConfigSent)?trigger:sendTestData}>{(ConfigSent)?'Start Test':'Load Drivers'}</h1>
                </div>
            </div>
        </div>
    )
}

export default Create;