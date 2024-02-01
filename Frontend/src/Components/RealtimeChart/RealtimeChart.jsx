import React, { useEffect, useState } from 'react';
import { socket } from '../../App';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import gradient from 'chartjs-plugin-gradient';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  gradient
);

const maxDatapoints = 20;


const RealtimeChart = (props) => {

  const options = {
    // responsive: (props.bigChart != undefined)? props.bigChart : false,
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: props.color,
          font: {
            family: 'Quicksand'
          },
        }
      },
    },
    scales: {
      x: {
        grid : {
          display: false
        },
        ticks: {
          color: props.color,
          font: {
            family: 'Quicksand'
          },
        }
      },
      y: {
        grid : {
          display: false
        },
        ticks: {
          color: props.color,
          font: {
            family: 'Quicksand'
          },
        }
      },

    },
    animation: {
      duration: 0
    },
    elements : {
      point : {
        radius: 0
      }
    },
  };


  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Mean',
        data: [],
        fill: true,
        // hidden: true,
        borderColor: '#EC8F5E',
        borderWidth: 1,
        gradient: {
          backgroundColor: {
            axis: 'y',
            colors: {
              100 : '#EC8F5E'+'44',
              0: '#EC8F5E'+'00'
            }
          }
        },
        tension:  0.4,
      },
      {
        label: 'Median',
        data: [],
        fill: true,
        borderColor: '#A0E9FF',
        borderWidth: 1,
        gradient: {
          backgroundColor: {
            axis: 'y',
            colors: {
              100 : '#A0E9FF'+'44',
              0: '#A0E9FF'+'00'
            }
          }
        },
        tension:  0.4,
      },
      {
        label: 'Mode',
        data: [],
        fill: true,
        // hidden: true,
        borderColor: '#A7D397',
        borderWidth: 1,
        gradient: {
          backgroundColor: {
            axis: 'y',
            colors: {
              100 : '#A7D397'+'44',
              0: '#A7D397'+'00'
            }
          }
        },
        tension:  0.4,
      },
      {
        label: 'Min',
        data: [],
        fill: true,
        // hidden: true,
        borderColor: '#FFD099',
        borderWidth: 1,
        gradient: {
          backgroundColor: {
            axis: 'y',
            colors: {
              100 : '#FFD099'+'44',
              0: '#FFD099'+'00'
            }
          }
        },
        tension:  0.4,
      },
      {
        label: 'Max',
        data: [],
        fill: true,
        // hidden: true,
        borderColor: '#FFFB73',
        borderWidth: 1,
        gradient: {
          backgroundColor: {
            axis: 'y',
            colors: {
              100 : '#FFFB73'+'44',
              0: '#FFFB73'+'00'
            }
          }
        },
        tension:  0.4,
      },
    ],
  });

  useEffect(() => {
    
    socket.on(props.name, (data)=>{
      setChartData((prevData) => {
        const newLabels = [...prevData.labels, new Date().toLocaleTimeString()];

        let newDatasets = [];
        prevData.datasets.forEach(metric=>{
          newDatasets.push({
            ...metric,
            data: [...metric.data, data["metrics"][metric.label]]
          })
        })
        // if (newLabels.length > maxDatapoints){
        //   newLabels.shift()
        //   newDatasets.forEach(metric=>{
        //     metric.data.shift()
        //   })
        // }

        return {
          labels: newLabels,
          datasets: newDatasets,
        };
      });

    })

    // Clear the interval on component unmount
    
  }, [chartData]);
  

  return (
    <div className="RealtimeChart">
      <Line 
        options={options} 
        data={chartData}
        ></Line>
    </div>
  );
}

export default RealtimeChart
