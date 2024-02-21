import './NavBar.css'
import { useNavigate } from 'react-router-dom';

const NavBar = ()=>{

    const navigate = useNavigate();

    return (
        <div className="NavBar">
            {/* <div className='blur-bg'></div> */}
            <div className="nav-links">
                <div className='left-links' onClick={()=>{navigate('/')}}>
                    <img src="/horizontal_logo.png" className='horz-logo'/>
                </div>
                <div className="right-links">
                    <a onClick={()=>{navigate('/create')}}>Create</a>
                    <a onClick={()=>{navigate('/view')}}>View</a>
                    <a onClick={()=>{navigate('/history')}}>History</a>
                </div>
            </div>
        </div>
    )
}

export default NavBar;
