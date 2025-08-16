import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { login as apiLogin, signup as apiSignup, logout as apiLogout } from '../api/users.js';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkUser = async () => {
            try {
                // I need an endpoint to verify the current user from the session
                const response = await axios.get('http://localhost:3000/api/me', {
                    headers: { 'Cache-Control': 'no-cache' },
                    withCredentials: true,
                });
                if (response.data && response.data._id) {
                    setUser(response.data);
                }
            } catch (error) {
                // No user is logged in, or server is down.
                setUser(null);
            } finally {
                setLoading(false);
            }
        };
        checkUser();
    }, []);

    const login = async (credentials) => {
        const userData = await apiLogin(credentials);
        setUser(userData);
        return userData;
    };

    const signup = async (userData) => {
        const newUser = await apiSignup(userData);
        // Optionally log the user in directly after signup
        // setUser(newUser); 
        return newUser;
    };

    const logout = async () => {
        await apiLogout();
        setUser(null);
    };

    const value = {
        user,
        loading,
        login,
        signup,
        logout,
        isAuthenticated: !!user
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};