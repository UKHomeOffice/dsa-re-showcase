import React, { useEffect, useState } from "react";
import "./Admin.css";
import EditUser from "../../components/modal/EditUser";

const AdminPage = () => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await fetch("http://localhost:8080/api/v1/user");
      const data = await response.json();
      setUsers(data);
    };
    fetchUsers();
  }, []);

  const handleEditClick = (user) => {
    setSelectedUser(user);
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this user?"
    );

    if (confirmDelete) {
      await fetch(`http://localhost:8080/api/v1/user/${id}`, {
        method: "DELETE",
      });
    }
    setUsers(users.filter((user) => user.id !== id));
  };

  const handleModalClose = () => {
    setShowModal(false);
    setSelectedUser(null);
  };

  const handleUpdate = async () => {
    const response = await fetch("http://localhost:8080/api/v1/user");
    const data = await response.json();
    setUsers(data);
    handleModalClose();
  };

  return (
    <div className="admin-container">
      <div className="admin-content">
        <h1 className="admin-title">Admin Page</h1>
        <div className="admin-table-container">
          <table className="user-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Date of Birth</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.name}</td>
                  <td>{user.email}</td>
                  <td>{user.dob}</td>
                  <td>
                    <button
                      className="edit-btn"
                      onClick={() => handleEditClick(user)}
                    >
                      Edit
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(user.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {showModal && (
          <EditUser
            user={selectedUser}
            onClose={handleModalClose}
            onUpdate={handleUpdate}
          />
        )}
      </div>
    </div>
  );
};

export default AdminPage;
