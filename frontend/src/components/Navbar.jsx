import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();

  // Check if the user is logged in
  const isAuthenticated = localStorage.getItem("access_token");

  // Handle Logout
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">Resume Analyzer</div>
      <ul className="navbar-links">
        <li><Link to="/">Home</Link></li>
        {isAuthenticated && <li><Link to="/upload">Upload</Link></li>}
        {/* Conditionally render Login/Signup or Logout based on authentication */}
        {!isAuthenticated ? (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/signup">Signup</Link></li>
          </>
        ) : (
          <li><button onClick={handleLogout} className="logout-btn">Logout</button></li>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
