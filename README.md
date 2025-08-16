# Wanderlust - MERN Stack Application

A travel and accommodation booking platform built using the MERN stack (MongoDB, Express, React, Node.js).

## Project Structure

This project is organized into two main parts:

- **Backend**: RESTful API built with Express.js and MongoDB
- **Frontend**: Client application built with React and Vite

## Getting Started

### Prerequisites

- Node.js (v14 or later)
- MongoDB (local installation or MongoDB Atlas)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd wanderlust
```

2. Install backend dependencies:
```
cd backend
npm install
```

3. Install frontend dependencies:
```
cd ../frontend
npm install
```

### Running the Application

#### Backend

1. Start the MongoDB service on your machine or ensure you have access to your MongoDB Atlas cluster.

2. From the backend directory, start the server:
```
cd backend
npm run dev
```

The API server will run on http://localhost:8080.

#### Frontend

1. From the frontend directory, start the development server:
```
cd frontend
npm run dev
```

The React application will run on http://localhost:5173.

## Features

- Browse travel listings
- Filter listings by category
- Search for destinations
- View detailed listing information
- User authentication (coming soon)
- Create, update, and delete listings (coming soon)
- Post and view reviews (coming soon)

## Technologies Used

### Backend
- Node.js
- Express.js
- MongoDB with Mongoose
- Passport.js for authentication
- Multer for file uploads
- Cloudinary for image storage

### Frontend
- React
- React Router
- Axios for API requests
- Bootstrap for styling
- Font Awesome for icons