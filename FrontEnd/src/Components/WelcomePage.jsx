import { useState } from "react";
import "./WelcomePage.css";

export default function WelcomePage() {
  const [name, setName] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [email, setEmail] = useState("");

  const handleNameSubmit = () => {
    if (name.trim()) {
      setSubmitted(true);
    }
  };

  return (
    <div className="welcome-container">
      {/* Navigation */}
      <nav className="navbar">
        <div className="navbar-content">
          <div className="logo">
            <span>CompanyName</span>
          </div>
          <div className="nav-links">
            <a href="#">Home</a>
            <a href="#">Features</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
          </div>
          <div>
            <button className="btn btn-primary">
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            {submitted ? (
              <div className="welcome-message">
                <h1>Welcome, {name}!</h1>
                <p>
                  We're glad to have you join us. Explore our platform and discover all the amazing features we have to offer.
                </p>
              </div>
            ) : (
              <div className="welcome-message">
                <h1>Welcome to Our Platform</h1>
                <p>
                  The easiest way to build beautiful, responsive websites with our innovative tools and community support.
                </p>
                <div className="name-input-container">
                  <input
                    type="text"
                    placeholder="Enter your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                  <button onClick={handleNameSubmit} className="btn btn-secondary">
                    Go <span className="arrow-icon">→</span>
                  </button>
                </div>
              </div>
            )}
          </div>
          <div className="hero-image">
            <div className="image-container">
              <div className="coming-soon">
                <div className="coming-soon-text">
                  <div className="coming-soon-title">Coming Soon</div>
                  <div className="coming-soon-subtitle">Our new application!</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="features-content">
          <h2>Our Features</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon message-icon">
                <span>💬</span>
              </div>
              <h3>Easy Communication</h3>
              <p>Keep in touch with your team and clients with our integrated messaging system.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon coffee-icon">
                <span>☕</span>
              </div>
              <h3>Simple Integration</h3>
              <p>Connect with your favorite tools and services without any hassle.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon heart-icon">
                <span>❤️</span>
              </div>
              <h3>User Friendly</h3>
              <p>Designed with the user in mind, making it easy for anyone to use.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="newsletter">
        <div className="newsletter-content">
          <h2>Stay Updated</h2>
          <p>Subscribe to our newsletter to get the latest updates and news directly to your inbox.</p>
          <div className="subscribe-container">
            <input 
              type="email" 
              placeholder="Enter your email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <button className="btn btn-secondary">
              Subscribe
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-sections">
            <div className="footer-company-info">
              <h3>CompanyName</h3>
              <p>Creating amazing digital experiences for businesses worldwide since 2023.</p>
            </div>
            <div className="footer-links-container">
              <div className="footer-links">
                <h4>Company</h4>
                <ul>
                  <li><a href="#">About</a></li>
                  <li><a href="#">Careers</a></li>
                  <li><a href="#">Blog</a></li>
                </ul>
              </div>
              <div className="footer-links">
                <h4>Resources</h4>
                <ul>
                  <li><a href="#">Documentation</a></li>
                  <li><a href="#">Help Center</a></li>
                  <li><a href="#">Tutorials</a></li>
                </ul>
              </div>
              <div className="footer-links">
                <h4>Connect</h4>
                <ul>
                  <li><a href="#">Twitter</a></li>
                  <li><a href="#">LinkedIn</a></li>
                  <li><a href="#">Facebook</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2025 CompanyName. All rights reserved.</p>
            <div className="footer-policies">
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}