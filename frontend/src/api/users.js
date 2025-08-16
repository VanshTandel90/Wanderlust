import axios from 'axios';

const API_URL = 'http://localhost:3000/api';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

export const signup = async (userData) => {
  try {
    const response = await api.post('/signup', userData);
    return response.data;
  } catch (error) {
    console.error('Error signing up:', error.response?.data || error.message);
    throw error.response?.data || error;
  }
};

export const login = async (credentials) => {
  try {
    const response = await api.post('/login', credentials);
    return response.data;
  } catch (error) {
    console.error('Error logging in:', error.response?.data || error.message);
    throw error.response?.data || error;
  }
};

export const logout = async () => {
  try {
    const response = await api.get('/logout');
    return response.data;
  } catch (error) {
    console.error('Error logging out:', error.response?.data || error.message);
    throw error.response?.data || error;
  }
}; 