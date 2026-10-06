import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
function Todos() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: "",
  });
  const [error, setError] = useState("");
  const [todos, setTodoslist] = useState([]);
  const [editId, setEditId] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const res = await api.get("/todos/");
      setTodoslist(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to load todos");
    }
  };

  const handleEdit = (task) => {
    setForm({ title: task.title });
    setEditId(task.id);
  };

  const handleToggle = (task) => async () => {
    try {
      await api.put(`/todos/${task.id}`, { completed: !task.completed });
      fetchTodos();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update todo");
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      fetchTodos();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to delete todo");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await api.put(`/todos/${editId}`, form);
        setEditId(null);
      } else {
        await api.post("/todos/", form);
      }
      setForm({ title: "" });
      fetchTodos();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to add todo");
    }
  };

  const handleLogout = async () => {
  await api.post('/auth/logout')
  localStorage.removeItem('access_token')
  navigate('/login')
}


  return (
    <div className="todos-container">
      <h2>My Todos</h2>
      {error && <p className="error">{error}</p>}
      <form className="todo-form" onSubmit={handleSubmit}>
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          type="text"
          placeholder="Add a new todo..."
        />
        <button type="submit">Add</button>
      </form>

      <ul className="todo-list">
        {todos.map((task) => (
          <li className="todo-item" key={task.id}>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle(task)}
            />
            <span>{task.title}</span>
            <button className="update-btn" onClick={() => handleEdit(task)}>
              Update
            </button>
            <button
              className="delete-btn"
              onClick={() => handleDelete(task.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      <button className="logout-btn" onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default Todos;
