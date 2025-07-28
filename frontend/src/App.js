import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import * as THREE from 'three';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const FeedbackPortal = () => {
  const [activeView, setActiveView] = useState('dashboard');
  const [feedbackData, setFeedbackData] = useState([]);
  const [stats, setStats] = useState(null);
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_email: '',
    category: 'overall',
    rating: 5,
    comment: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const sceneRef = useRef();
  const rendererRef = useRef();
  const animationRef = useRef();

  // Fetch data
  const fetchFeedbackData = async () => {
    try {
      const [feedbackRes, statsRes] = await Promise.all([
        axios.get(`${API}/feedback`),
        axios.get(`${API}/feedback/stats`)
      ]);
      setFeedbackData(feedbackRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Submit feedback
  const handleSubmitFeedback = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await axios.post(`${API}/feedback`, formData);
      setFormData({
        customer_name: '',
        customer_email: '',
        category: 'overall',
        rating: 5,
        comment: ''
      });
      await fetchFeedbackData();
      alert('Feedback submitted successfully!');
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Error submitting feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // 3D Visualization Setup
  const init3DVisualization = () => {
    if (!stats || !sceneRef.current) return;

    // Clear previous scene
    if (rendererRef.current) {
      sceneRef.current.removeChild(rendererRef.current.domElement);
    }

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0a);

    const camera = new THREE.PerspectiveCamera(75, sceneRef.current.clientWidth / sceneRef.current.clientHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(sceneRef.current.clientWidth, sceneRef.current.clientHeight);
    sceneRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    scene.add(directionalLight);

    // Create 3D bars for rating distribution
    const ratingDistribution = stats.rating_distribution || {};
    const barGroup = new THREE.Group();
    
    Object.entries(ratingDistribution).forEach(([rating, count], index) => {
      const height = Math.max(count * 0.5, 0.1);
      const geometry = new THREE.BoxGeometry(0.8, height, 0.8);
      
      // Color based on rating
      const colors = [0xff4444, 0xff8844, 0xffaa44, 0x44ff44, 0x44aa44];
      const material = new THREE.MeshPhongMaterial({ 
        color: colors[parseInt(rating) - 1] || 0x44aa44,
        transparent: true,
        opacity: 0.8
      });
      
      const bar = new THREE.Mesh(geometry, material);
      bar.position.set((index - 2) * 2, height / 2, 0);
      barGroup.add(bar);

      // Add text label
      const loader = new THREE.FontLoader();
      // For simplicity, we'll use basic shapes instead of text
      const labelGeometry = new THREE.SphereGeometry(0.1);
      const labelMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const label = new THREE.Mesh(labelGeometry, labelMaterial);
      label.position.set((index - 2) * 2, height + 0.5, 0);
      barGroup.add(label);
    });

    scene.add(barGroup);

    // Create floating particles for sentiment
    const particleGeometry = new THREE.BufferGeometry();
    const particleCount = 100;
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20;

      colors[i * 3] = Math.random();
      colors[i * 3 + 1] = Math.random();
      colors[i * 3 + 2] = Math.random();
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 0.1,
      vertexColors: true,
      transparent: true,
      opacity: 0.6
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    camera.position.set(0, 5, 10);
    camera.lookAt(0, 0, 0);

    // Animation loop
    const animate = () => {
      animationRef.current = requestAnimationFrame(animate);
      
      barGroup.rotation.y += 0.005;
      particles.rotation.x += 0.001;
      particles.rotation.y += 0.002;
      
      renderer.render(scene, camera);
    };
    animate();
  };

  useEffect(() => {
    fetchFeedbackData();
  }, []);

  useEffect(() => {
    if (activeView === 'dashboard' && stats) {
      init3DVisualization();
    }
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [activeView, stats]);

  // Handle window resize
  useEffect(() => {
    const handleResize = () => {
      if (rendererRef.current && sceneRef.current) {
        const width = sceneRef.current.clientWidth;
        const height = sceneRef.current.clientHeight;
        rendererRef.current.setSize(width, height);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const renderDashboard = () => (
    <div className="dashboard-container">
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Feedback</h3>
          <div className="stat-number">{stats?.total_feedback || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Average Rating</h3>
          <div className="stat-number">{stats?.avg_rating?.toFixed(1) || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Categories</h3>
          <div className="stat-number">{Object.keys(stats?.category_breakdown || {}).length}</div>
        </div>
      </div>
      
      <div className="visualization-container">
        <h2 className="viz-title">3D Feedback Visualization</h2>
        <div ref={sceneRef} className="three-container"></div>
      </div>

      <div className="recent-feedback">
        <h3>Recent Feedback</h3>
        <div className="feedback-list">
          {stats?.recent_feedback?.slice(0, 5).map((feedback) => (
            <div key={feedback.id} className="feedback-item">
              <div className="feedback-header">
                <span className="customer-name">{feedback.customer_name}</span>
                <span className="rating">{'⭐'.repeat(feedback.rating)}</span>
              </div>
              <div className="feedback-comment">{feedback.comment}</div>
              <div className="feedback-meta">
                <span className="category">{feedback.category}</span>
                <span className="date">{new Date(feedback.timestamp).toLocaleDateString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderFeedbackForm = () => (
    <div className="form-container">
      <div className="form-card">
        <h2>Submit Your Feedback</h2>
        <form onSubmit={handleSubmitFeedback}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              value={formData.customer_name}
              onChange={(e) => setFormData({...formData, customer_name: e.target.value})}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={formData.customer_email}
              onChange={(e) => setFormData({...formData, customer_email: e.target.value})}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Category</label>
            <select
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
            >
              <option value="overall">Overall Experience</option>
              <option value="product">Product</option>
              <option value="service">Service</option>
              <option value="support">Support</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Rating: {formData.rating} {'⭐'.repeat(formData.rating)}</label>
            <input
              type="range"
              min="1"
              max="5"
              value={formData.rating}
              onChange={(e) => setFormData({...formData, rating: parseInt(e.target.value)})}
              className="rating-slider"
            />
          </div>
          
          <div className="form-group">
            <label>Comments</label>
            <textarea
              value={formData.comment}
              onChange={(e) => setFormData({...formData, comment: e.target.value})}
              required
              rows="4"
              placeholder="Tell us about your experience..."
            />
          </div>
          
          <button type="submit" disabled={isSubmitting} className="submit-btn">
            {isSubmitting ? 'Submitting...' : 'Submit Feedback'}
          </button>
        </form>
      </div>
    </div>
  );

  return (
    <div className="feedback-portal">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Customer Feedback Portal</h1>
          <p className="hero-subtitle">Experience the future of feedback visualization with our 3D interactive dashboard</p>
        </div>
      </div>

      <nav className="navigation">
        <button 
          className={`nav-btn ${activeView === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveView('dashboard')}
        >
          3D Dashboard
        </button>
        <button 
          className={`nav-btn ${activeView === 'submit' ? 'active' : ''}`}
          onClick={() => setActiveView('submit')}
        >
          Submit Feedback
        </button>
      </nav>

      <main className="main-content">
        {activeView === 'dashboard' ? renderDashboard() : renderFeedbackForm()}
      </main>
    </div>
  );
};

export default FeedbackPortal;