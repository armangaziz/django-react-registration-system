import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Home.css";

function Home() {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getUser();
    }, []);

    const getUser = async () => {
        try {
            const res = await api.get("/api/user/");
            setUser(res.data);
        } catch (error) {
            console.error(error);
        }
    };

    const logout = () => {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        navigate("/login");
    };

    if (!user) {
        return <h2>Loading...</h2>;
    }

    return (
        <div className="home-container">
            <div className="profile-card">
                <h1>Личный кабинет</h1>

                <div className="profile-info">
                    <strong>Username:</strong> {user.username}
                </div>

                <div className="profile-info">
                    <strong>Email:</strong> {user.email}
                </div>

                <div className="profile-info">
                    <strong>Role:</strong> {user.role}
                </div>

                <button className="form-button" onClick={logout}>
                    Logout
                </button>
            </div>
        </div>
    );
}

export default Home;