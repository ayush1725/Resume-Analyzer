import { BrowserRouter, Routes, Route, useLocation, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Home from "./pages/Home";
import ResumeUpload from "./pages/ResumeUpload";
import Navbar from "./components/Navbar";
import { useEffect } from "react";
import NotFound from "./pages/NotFound";

// Wrapper Component for Route Management
function AppWrapper() {
  const location = useLocation();
  
  // Pages where Navbar should be hidden
  const hideNavbarRoutes = ["/login", "/signup"];
  
  // Check if user is logged in by verifying if the token exists in localStorage
  const isAuthenticated = localStorage.getItem("access_token");

  useEffect(() => {
    window.scrollTo(0, 0); // Scroll to top on route change
  }, [location]);

  return (
    <>
      {/* Show Navbar unless we are on login or signup page */}
      {!hideNavbarRoutes.includes(location.pathname) && <Navbar />}

      <Routes>
        {/* Home route */}
        <Route path="/" element={isAuthenticated ? <Home /> : <Navigate to="/login" />} />
        <Route path="/home" element={<Navigate to="/" />} />

        {/* Signup and Login routes */}
        <Route path="/signup" element={isAuthenticated ? <Navigate to="/" /> : <Signup />} />
        <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <Login />} />

        {/* Resume Upload */}
        <Route path="/upload" element={isAuthenticated ? <ResumeUpload /> : <Navigate to="/login" />} />

        {/* Catch-all 404 */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}

// Main App Component
function App() {
  return (
    <BrowserRouter>
      <AppWrapper />
    </BrowserRouter>
  );
}

export default App;
