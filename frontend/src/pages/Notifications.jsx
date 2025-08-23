import { useState, useEffect } from 'react';
import { getNotifications, deleteNotification } from '../api/users';
import './Notifications.css';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const data = await getNotifications();
      setNotifications(data);
    } catch (error) {
      console.error("Failed to fetch notifications", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleDelete = async (notificationId) => {
    if (window.confirm("Are you sure you want to remove this notification?")) {
      try {
        await deleteNotification(notificationId);
        // Refresh the list after deleting
        setNotifications(notifications.filter(n => n._id !== notificationId));
      } catch (error) {
        alert("Failed to remove notification.");
      }
    }
  };

  if (loading) {
    return <div className="text-center my-5">Loading notifications...</div>;
  }

  return (
    <div className="notifications-container">
      <h2>Interested Buyers</h2>
      {notifications.length === 0 ? (
        <p>You have no new notifications.</p>
      ) : (
        <div className="notifications-list">
          {notifications.map((noti) => (
            <div key={noti._id} className="notification-card">
              <button onClick={() => handleDelete(noti._id)} className="delete-noti-btn">X</button>
              <h4> {noti.listingTitle}</h4>
              <p><strong>Name:</strong> {noti.interestedUserName}</p>
              <p><strong>Email:</strong> {noti.interestedUserEmail}</p>
              <p><strong>Mobile:</strong> {noti.interestedUserMobile}</p>
              <p><strong>Location:</strong> {noti.interestedUserLocation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Notifications;