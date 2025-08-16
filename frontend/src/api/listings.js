import axios from "axios";

// const API_URL = 'http://localhost:8080/api';
const API_URL = "http://localhost:3000/api";

// Create an axios instance
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});
// Get all listings
export const getAllListings = async () => {
  try {
    const response = await api.get("/listings");

    return response.data;
  } catch (error) {
    console.error("Error fetching listings:", error);
    // Return empty array instead of throwing to make it easier to handle in components
    return [];
  }
};

// Get a single listing by ID
export const getListingById = async (id) => {
  try {
    const response = await api.get(`/listings/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching listing with ID ${id}:`, error);
    return null;
  }
};

// Get listings by category
export const getListingsByCategory = async (category) => {
  try {
    const response = await api.get(`/listings/categories/${category}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching listings for category ${category}:`, error);
    return [];
  }
};

// Search listings by destination
export const searchListings = async (destination) => {
  try {
    if (!destination || typeof destination !== "string") {
      console.error("Invalid search term:", destination);
      return [];
    }
    const response = await api.post("/listings/search", {
      destination: destination.trim(),
    });
    return response.data;
  } catch (error) {
    console.error("Error searching listings:", error);
    return [];
  }
};

// Create a review for a listing
export const createReview = async (listingId, reviewData) => {
  try {
    const response = await api.post(`/listings/${listingId}/reviews`, {
      review: reviewData,
    });
    return response.data;
  } catch (error) {
    console.error("Error creating review:", error);
    throw error;
  }
};

// Delete a review
export const deleteReview = async (listingId, reviewId) => {
  try {
    const response = await api.delete(
      `/listings/${listingId}/reviews/${reviewId}`
    );
    return response.data;
  } catch (error) {
    console.error("Error deleting review:", error);
    throw error;
  }
};

// Create a new listing
export const createListing = async (listingData) => {
  try {
    const formData = new FormData();

    for (const key in listingData) {
      if (key === "image" && listingData.image) {
        formData.append("listing[image]", listingData.image);
      } else if (key === 'category') {
        // Handle category array properly
        if (Array.isArray(listingData.category)) {
          listingData.category.forEach(cat => {
            formData.append('listing[category][]', cat);
          });
        }
      } else {
        formData.append(`listing[${key}]`, listingData[key]);
      }
    }

    const response = await api.post("/listings", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error creating listing:", error);
    throw error;
  }
};

// Update an existing listing
export const updateListing = async (id, listingData) => {
  try {
    // Create FormData for file upload
    const formData = new FormData();

    // Add listing data to FormData
    for (const key in listingData) {
      if (key === "image" && listingData.image) {
        // Only append image if it's a new file
        formData.append("listing[image]", listingData.image);
      } else if (key === 'category') {
        // Handle category array properly
        if (Array.isArray(listingData.category)) {
          listingData.category.forEach(cat => {
            formData.append('listing[category][]', cat);
          });
        }
      } else if (key !== 'image') {
        // Append all other fields, but ignore a null/empty image field
        formData.append(`listing[${key}]`, listingData[key]);
      }
    }

    const response = await api.put(`/listings/${id}`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  } catch (error) {
    console.error(`Error updating listing with ID ${id}:`, error);
    throw error;
  }
};

// Delete a listing
export const deleteListing = async (id) => {
  try {
    const response = await api.delete(`/listings/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting listing with ID ${id}:`, error);
    throw error;
  }
};

export default {
  getAllListings,
  getListingById,
  getListingsByCategory,
  searchListings,
  createListing,
  updateListing,
  deleteListing,
  createReview,
  deleteReview,
};
