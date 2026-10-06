import axios from 'axios';


const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true
});

api.interceptors.request.use((config) => {
  // config = request ki saari info (url, headers, body, etc.)

  const token = localStorage.getItem('access_token')  
  // localStorage se token uthao

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    // request ke header mein token add karo
  }

  return config  
  // modified config wapas bhejo — request ab jaayegi
})

api.interceptors.response.use(
  (response)=>response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }

)


export default api