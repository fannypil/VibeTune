import { Navigate, useLocation } from 'react-router-dom';

export default function ProtectedRoute({ children }) {
  const location = useLocation();
  const token = localStorage.getItem('token');
  
  if (!token) {
    // Redirect to /auth but save the attempted location
    return <Navigate to="/auth" state={{ from: location }} replace />;
  }
  
  // If user is already authenticated and tries to access /auth, redirect to /home
  if (location.pathname === '/auth' && token) {
    return <Navigate to="/home" replace />;
  }
  
  return children;
}