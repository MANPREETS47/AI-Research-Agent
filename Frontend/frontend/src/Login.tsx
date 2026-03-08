import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Login failed");
      }

      const data = await response.json();
      localStorage.setItem("access_token", data.access_token);
      navigate("/");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#1a1a1a] text-white flex flex-col items-center justify-center">
      <h1 className="text-4xl mb-6">Welcome Back</h1>

      <form
        onSubmit={handleLogin}
        className="flex flex-col w-96 border border-gray-600 p-6 rounded-2xl shadow-[0_0_8px_rgba(255,255,255,0.3)] gap-4"
      >
        {error && (
          <p className="text-red-400 text-sm text-center">{error}</p>
        )}

        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
          className="w-full bg-transparent border border-gray-600 rounded-xl p-3 outline-none focus:border-gray-400 transition-colors"
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
          className="w-full bg-transparent border border-gray-600 rounded-xl p-3 outline-none focus:border-gray-400 transition-colors"
        />

        <button
          type="submit"
          disabled={loading || !email.trim() || !password.trim()}
          className="bg-gray-600 px-4 py-2 rounded-xl hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-sm text-gray-400 text-center">
          Don't have an account?{" "}
          <Link to="/register" className="text-white underline hover:text-gray-300">
            Register
          </Link>
        </p>
      </form>
    </div>
  );
}

export default Login;
