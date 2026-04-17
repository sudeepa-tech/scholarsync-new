import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getApiError, registerUser } from "../api/scholarsyncApi";
import { LogoIcon } from "../components/Icons";
import { storeUser } from "../utils/session";

export default function Signup() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ fullName: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((currentForm) => ({ ...currentForm, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const response = await registerUser({
        full_name: form.fullName.trim(),
        email: form.email.trim(),
        password: form.password,
      });

      storeUser(response.user);
      navigate("/dashboard");
    } catch (requestError) {
      setError(getApiError(requestError, "Unable to create account"));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-page">
      <div className="auth-gradient auth-gradient-left" />
      <div className="auth-gradient auth-gradient-right" />

      <section className="auth-hero">
        <div className="brand-lockup centered">
          <div className="brand-logo large">
            <LogoIcon className="icon-xl" />
          </div>
          <h1>ScholarSync</h1>
          <p>Manage your students with ease (Demo Mode)</p>
        </div>

        <form className="auth-card" onSubmit={handleSubmit}>
          <div className="auth-copy">
            <h2>Create an account</h2>
            <p>Join us to start managing your students</p>
          </div>

          <label className="field-group">
            <span>Full Name</span>
            <input
              name="fullName"
              placeholder="Rahul Kumar"
              value={form.fullName}
              onChange={handleChange}
              required
            />
          </label>

          <label className="field-group">
            <span>Email Address</span>
            <input
              name="email"
              type="email"
              placeholder="name@example.com"
              value={form.email}
              onChange={handleChange}
              required
            />
          </label>

          <label className="field-group">
            <span>Password</span>
            <input
              name="password"
              type="password"
              placeholder="********"
              value={form.password}
              onChange={handleChange}
              required
            />
          </label>

          {error ? <div className="auth-alert">{error}</div> : null}

          <button type="submit" className="primary-button full-width" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Account"}
          </button>

          <p className="auth-switch">
            Already have an account? <Link to="/">Sign in</Link>
          </p>
        </form>
      </section>
    </main>
  );
}
