import { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Home() {
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get("http://localhost:8000/me/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setEmail(res.data.email);
      } catch (err) {
        navigate("/login");
      }
    };

    fetchUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <div className="container">
      <form style={{ textAlign: "center" }}>
        <h2 style={{ color: "var(--primary)", marginBottom: "10px" }}>
          Welcome!
        </h2>
        <p style={{ marginBottom: "20px" }}>
          Logged in as <strong>{email}</strong>
        </p>
        <button type="button" onClick={handleLogout}>
          Logout
        </button>
      </form>
    </div>
  );
}

export default Home;
