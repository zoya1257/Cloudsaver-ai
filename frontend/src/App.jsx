import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [service, setService] = useState("EC2");
  const [usageHours, setUsageHours] = useState(100);
  const [region, setRegion] = useState("us-east-1");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // ✅ Correct backend endpoint (must match FastAPI route)
      const response = await axios.post(
        "https://automatic-dollop-jjgpw4v79vxxc5grq-8001.app.github.dev/api/estimate",
        {
          service,
          usage_hours: Number(usageHours),
          region,
        },
        { headers: { "Content-Type": "application/json" } }
      );

      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to fetch cost estimation. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>☁ AWS AI Cost Estimator</h1>

      <form onSubmit={handleSubmit}>
        <label>Service:</label>
        <select value={service} onChange={(e) => setService(e.target.value)}>
          <option value="EC2">EC2</option>
          <option value="S3">S3</option>
          <option value="Lambda">Lambda</option>
          <option value="RDS">RDS</option>
        </select>

        <label>Usage Hours:</label>
        <input
          type="number"
          value={usageHours}
          onChange={(e) => setUsageHours(e.target.value)}
        />

        <label>Region:</label>
        <select value={region} onChange={(e) => setRegion(e.target.value)}>
          <option value="us-east-1">US East (N. Virginia)</option>
          <option value="us-west-1">US West (N. California)</option>
          <option value="ap-south-1">Asia Pacific (Mumbai)</option>
          <option value="eu-central-1">Europe (Frankfurt)</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Estimating…" : "Estimate Cost"}
        </button>
      </form>

      {result && (
        <div className="result">
          <h2>
            Estimated Cost: ${result.estimated_cost} {result.currency}
          </h2>

          <h3>AI Suggestions:</h3>
          <ul>
            {result.suggestions?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;