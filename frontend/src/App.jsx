import { useEffect, useState } from "react";
import { API_BASE_URL, getCurrentUser, loginUser, logoutUser, registerUser } from "./api";

const TOKEN_KEY = "secure_auth_token";

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY) || "");
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!token) {
      setUser(null);
      return;
    }

    getCurrentUser(token)
      .then((data) => setUser(data))
      .catch((err) => {
        setError(err.message);
        localStorage.removeItem(TOKEN_KEY);
        setToken("");
      });
  }, [token]);

  async function handleRegister(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const data = await registerUser({ email, password });
      setMessage(data.message || "Registration successful");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleLogin(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setMessage("");
    try {
      const data = await loginUser({ email, password });
      localStorage.setItem(TOKEN_KEY, data.access_token);
      setToken(data.access_token);
      setMessage("Login successful");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleLogout() {
    if (!token) {
      return;
    }
    setLoading(true);
    setError("");
    setMessage("");
    try {
      await logoutUser(token);
      setMessage("Logged out successfully");
    } catch (err) {
      setError(err.message);
    } finally {
      localStorage.removeItem(TOKEN_KEY);
      setToken("");
      setUser(null);
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="card">
        <h1>Secure Authentication System</h1>
        <p className="sub">React frontend connected to Flask JWT backend</p>
        <p className="sub">API: {API_BASE_URL}</p>

        <form className="form" onSubmit={handleLogin}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="user@example.com"
            required
          />

          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Minimum 8 characters"
            required
          />

          <div className="row">
            <button type="submit" disabled={loading}>
              {loading ? "Please wait..." : "Login"}
            </button>
            <button type="button" className="secondary" onClick={handleRegister} disabled={loading}>
              Register
            </button>
            <button type="button" className="danger" onClick={handleLogout} disabled={loading || !token}>
              Logout
            </button>
          </div>
        </form>

        {message && <p className="message success">{message}</p>}
        {error && <p className="message error">{error}</p>}

        <section className="profile">
          <h2>Session</h2>
          {token ? <p className="token">Token saved in localStorage.</p> : <p>No active session.</p>}
          {user && (
            <div className="user">
              <p>
                <strong>ID:</strong> {user.id}
              </p>
              <p>
                <strong>Email:</strong> {user.email}
              </p>
              <p>
                <strong>Created:</strong> {user.created_at}
              </p>
              <p>
                <strong>Last Login:</strong> {user.last_login_at || "N/A"}
              </p>
            </div>
          )}
        </section>
      </section>
    </main>
  );
}
