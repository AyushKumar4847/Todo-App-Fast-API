import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api/axios'
function Register(){

    const [form, setForm] = useState({ name: '', email: '', password: '' })
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleChange=(e)=>{
        setForm({...form, [e.target.name]:e.target.value})
    }

    const handleSubmit=async(e)=>{
        e.preventDefault()

        try {
            await api.post('/auth/register', form)
            navigate('/login')
        } catch (error) {
            setError(error.response?.data?.detail || 'Registration failed')
        }

    }

    return(
<div className="container">
  <h2>Register</h2>
  {error && <p className="error">{error}</p>}
  <form onSubmit={handleSubmit}>
    <input name="name" type="text" value={form.name} placeholder="Username" onChange={handleChange} required />
    <input name="email" value={form.email} type="email" placeholder="Email" onChange={handleChange} required />
    <input name="password" type="password" value={form.password} placeholder="Password" onChange={handleChange} required />
    <button type="submit">Register</button>
  </form>
  <p>Already have an account? <Link to="/login">Login karo</Link></p>
</div>
    )
}
export default Register
