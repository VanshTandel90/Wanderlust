import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Listings from './pages/Listings';
import SearchResults from './pages/SearchResults';
import ShowListing from './pages/ShowListing';
import Notifications from './pages/Notifications';
import CreateListing from './pages/CreateListing';
import UpdateListing from './pages/UpdateListing';
import Signup from './pages/Signup';
import Login from './pages/Login';
import ProtectedRoute from './components/ProtectedRoute';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Listings />} />
            <Route path="/categories/:category" element={<Listings />} />
            <Route path="/search" element={<SearchResults />} />
            <Route path="/listings/new" element={<ProtectedRoute><CreateListing /></ProtectedRoute>} />
            <Route path="/listings/:id/edit" element={<ProtectedRoute><UpdateListing /></ProtectedRoute>} />
            <Route path="/listings/:id" element={<ShowListing />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </main>
        <Footer />
      </div>
          </BrowserRouter>
  );
}

export default App;
