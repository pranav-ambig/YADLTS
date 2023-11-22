import './MetricBox.css'

const MetricBox = (props) =>{

    const round = (x) =>{
        if (x === undefined) return 0
        return (Math.round(x * 1000) / 1000)
    }

    return (
        <div className='MetricBox'>
          <div className="stats">
            <h4>Mean</h4>
            <h4>{round(props.stats.Mean)} ms</h4>
            <h4>Median</h4>
            <h4>{round(props.stats.Median)} ms</h4>
            <h4>Mode</h4>
            <h4>{round(props.stats.Mode)} ms</h4>
            <h4>Min</h4>
            <h4>{round(props.stats.Min)} ms</h4>
            <h4>Max</h4>
            <h4>{round(props.stats.Max)} ms</h4>
            <h4>Requests</h4>
            <h4>{props.stats.Requests}</h4>
          </div>
        </div>
    )
}

export default MetricBox;