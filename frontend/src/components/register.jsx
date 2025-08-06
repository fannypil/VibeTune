import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, User, CheckCircle, Loader2, AlertCircle } from 'lucide-react';
import { authService } from '../services/authService';

export default function Register({ onSwitchToLogin }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    firstName: '',
    lastName: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  // Client-side validation logic
  const validateForm = () => {
    const newErrors = {};


    // First Name & Last Name validation
    if (!formData.firstName) newErrors.firstName = 'First name is required.';
    if (!formData.lastName) newErrors.lastName = 'Last name is required.';
    // Username validation
    if (!formData.username) {
      newErrors.username = 'Username is required.';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters.';
    } else if (formData.username.length > 50) {
      newErrors.username = 'Username cannot exceed 50 characters.';
    }

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required.';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email address is invalid.';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required.';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters.';
    } else if (!/\d/.test(formData.password)) {
      newErrors.password = 'Password must contain at least one number.';
    } else if (!/[A-Z]/.test(formData.password)) {
      newErrors.password = 'Password must contain at least one uppercase letter.';
    }

    // Confirm Password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }
    
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({}); // Clear previous errors

    // Perform client-side validation first
    const validationErrors = validateForm();
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setIsLoading(true);
    setIsSuccess(false);

    try {
      await authService.register({
        username: formData.username,
        email: formData.email,
        firstName: formData.firstName,
        lastName: formData.lastName,
        password: formData.password
      });

      setIsSuccess(true);
      
      // Automatically log the user in after successful registration
      const loginResponse = await authService.login({
        email: formData.email,
        password: formData.password
      });
      localStorage.setItem('token', loginResponse.access_token);
      
      // Delay navigation to show success message
      setTimeout(() => {
        navigate('/home');
      }, 2000);

    } catch (err) {
      // Handle specific backend errors
      const errorMessage = err.message || 'An unexpected error occurred.';
      const newErrors = {};
      if (errorMessage.toLowerCase().includes('email')) {
        newErrors.email = errorMessage;
      } else if (errorMessage.toLowerCase().includes('username')) {
        newErrors.username = errorMessage;
      } else {
        newErrors.general = errorMessage;
      }
      setErrors(newErrors);
      setIsSuccess(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    // Clear the error for a field when the user starts typing in it
    if (errors[name]) {
      setErrors({ ...errors, [name]: null });
    }
  };
    if (isSuccess) {
    return (
      <div className="w-full text-center py-8">
        <div className="flex justify-center mb-4">
          <div className="w-16 h-16 bg-green-500/10 rounded-full flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-green-400" />
          </div>
        </div>
        <h3 className="text-2xl font-bold text-white mb-2">Registration Successful!</h3>
        <p className="text-purple-200 mb-4">
          Welcome to VibeTune! Redirecting you to your dashboard...
        </p>
        <div className="flex justify-center">
          <Loader2 className="w-6 h-6 text-purple-400 animate-spin" />
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <h2 className="text-2xl font-bold text-white mb-6">Create Account</h2>
      
      {errors.general && (
        <div className="bg-red-500/10 text-red-200 p-4 rounded-lg mb-6 flex items-center">
          <AlertCircle className="w-5 h-5 mr-3" />
          {errors.general}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name Fields */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 w-5 h-5" />
              <input
                type="text"
                name="firstName"
                placeholder="First Name"
                value={formData.firstName}
                onChange={handleChange}
                className={`w-full pl-10 pr-4 py-3 bg-white/5 border rounded-lg text-white ${errors.firstName ? 'border-red-500' : 'border-white/10'}`}
                required
              />
            </div>
            {errors.firstName && <p className="text-red-400 text-sm mt-1">{errors.firstName}</p>}
          </div>
          <div>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 w-5 h-5" />
              <input
                type="text"
                name="lastName"
                placeholder="Last Name"
                value={formData.lastName}
                onChange={handleChange}
                className={`w-full pl-10 pr-4 py-3 bg-white/5 border rounded-lg text-white ${errors.lastName ? 'border-red-500' : 'border-white/10'}`}
                required
              />
            </div>
            {errors.lastName && <p className="text-red-400 text-sm mt-1">{errors.lastName}</p>}
          </div>
        </div>

        {/* Username Field */}
        <div>
          <div className="relative">
            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 w-5 h-5" />
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              className={`w-full pl-10 pr-4 py-3 bg-white/5 border rounded-lg text-white ${errors.username ? 'border-red-500' : 'border-white/10'}`}
              required
            />
          </div>
          {errors.username && <p className="text-red-400 text-sm mt-1">{errors.username}</p>}
        </div>

        {/* Email Field */}
        <div>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 w-5 h-5" />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              className={`w-full pl-10 pr-4 py-3 bg-white/5 border rounded-lg text-white ${errors.email ? 'border-red-500' : 'border-white/10'}`}
              required
            />
          </div>
          {errors.email && <p className="text-red-400 text-sm mt-1">{errors.email}</p>}
        </div>

        {/* Password Fields */}
        <div>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 w-5 h-5" />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              className={`w-full pl-10 pr-4 py-3 bg-white/5 border rounded-lg text-white ${errors.password ? 'border-red-500' : 'border-white/10'}`}
              required
            />
          </div>
          {errors.password && <p className="text-red-400 text-sm mt-1">{errors.password}</p>}
        </div>
        <div>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-white/40 w-5 h-5" />
            <input
              type="password"
              name="confirmPassword"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={handleChange}
              className={`w-full pl-10 pr-4 py-3 bg-white/5 border rounded-lg text-white ${errors.confirmPassword ? 'border-red-500' : 'border-white/10'}`}
              required
            />
          </div>
          {errors.confirmPassword && <p className="text-red-400 text-sm mt-1">{errors.confirmPassword}</p>}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg font-medium disabled:opacity-50 transition-opacity"
        >
          {isLoading ? (
            <span className="flex items-center justify-center">
              <Loader2 className="animate-spin h-5 w-5 mr-3" />
              Creating account...
            </span>
          ) : (
            'Create Account'
          )}
        </button>
      </form>

      <div className="mt-6 text-center">
        <button
          onClick={onSwitchToLogin}
          className="text-purple-200 hover:text-white transition-colors"
        >
          Already have an account? Sign in
        </button>
      </div>
    </div>
  );
}