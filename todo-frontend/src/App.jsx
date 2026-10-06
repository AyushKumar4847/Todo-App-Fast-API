import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './components/login'
import Register from './components/register'
import Todos from './components/Todos'


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/todos" element={<Todos />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
