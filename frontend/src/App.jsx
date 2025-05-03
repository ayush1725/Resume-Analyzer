import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Home from "./pages/Home";
import ResumeUpload from "./pages/ResumeUpload";
import Navbar from "./components/Navbar";
import { useEffect } from "react";

function AppWrapper() {
  const location = useLocation();

  // Pages where Navbar should be hidden
  const hideNavbarRoutes = ["/login", "/signup"];

  useEffect(() => {
    window.scrollTo(0, 0); // scroll to top on route change
  }, [location]);

  return (
    <>
      {!hideNavbarRoutes.includes(location.pathname) && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/upload" element={<ResumeUpload />} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppWrapper />
    </BrowserRouter>
  );
}

export default App;
