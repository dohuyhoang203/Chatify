import axios from "axios";


const axiosInstance = axios.create({
    baseURL: "http:////163.124.2.102:5002//chatify/api",
    timeout: 30000
})

export default axiosInstance;