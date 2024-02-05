import { useEffect, useState } from 'react';
import './History.css'
import axios from 'axios';
import MetricBox from '../../Components/MetricBox/MetricBox';
import { BACKEND_URL } from '../../App';



/* 

IN DEV

*/
const History = ()=>{

    const [history, setHistory] = useState({});
    const [TestIds, setTestIds] = useState([]);


    useEffect(()=>{
        console.log(history[TestIds[0]])
    }, [TestIds])

    useEffect(()=>{
        axios.get(BACKEND_URL+'/history')
        .then((res)=>{
            // console.log(res.data.history)
            setHistory(res.data.history)
            setTestIds(Object.keys(res.data.history))
            // console.log(res.data.history)
    
            console.log('sakfkds', res)
        })
    }, [])

    return (
        <div className="History">
            <div className='spacer'></div>
            <h1 className="title">History</h1>
            {/* <h2>{TestIds[0]}</h2> */}

            <div className='history-blocks'>
                {TestIds.map((test_id, i)=>{
                    return (
                        <div className='test-metric-block' key={i}>
                            <h2>{test_id}</h2>
                            <MetricBox stats={history[test_id]}></MetricBox>
                        </div>
                    )
                })}
            </div>
            <div className='spacer'></div>
        </div>
    )
}

export default History;
