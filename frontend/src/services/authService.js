const API_BASE_URL = 'http://localhost:8000/auth';

export const authService = {
  async login({ email, password }) {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        'username': email,  // FastAPI OAuth expects 'username'
        'password': password
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return response.json();
  },

   async register({ username, email, firstName, lastName, password }) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username,
        email: email,
        first_name: firstName,
        last_name: lastName,
        password: password
      })
    });

    const data = await response.json();

    if (!response.ok) {
      // Create a custom error that includes the detailed validation data
      const error = new Error(data.detail || 'Registration failed');
      
      // Check for FastAPI's detailed validation error format
      if (response.status === 422 && Array.isArray(data.detail)) {
        error.message = 'Please correct the errors below.'; // Set a general message
        error.validationDetails = data.detail; // Attach the array of specific errors
      }
      
      throw error;
    }

    return data;
  },

async getCurrentUser() {
    const token = localStorage.getItem('token');
    if (!token) return null;

    const response = await fetch(`${API_BASE_URL}/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      localStorage.removeItem('token');
      throw new Error('Failed to get user');
    }

    return response.json();
  }
};