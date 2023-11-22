import './NavBar.css'
import { useNavigate } from 'react-router-dom';

const NavBar = ()=>{

    const navigate = useNavigate();

    return (
        <div className="NavBar">
            <div className="nav-links">
                <div className='left-links'>
                    <h1 className='curr-page'>Dashboard</h1>
                </div>
                <div className="right-links">
                    <a onClick={()=>{navigate('/')}}>Create</a>
                    <a onClick={()=>{navigate('/view')}}>View</a>
                    <a onClick={()=>{navigate('/history')}}>History</a>
                </div>
            </div>
        </div>
    )
}

export default NavBar;
