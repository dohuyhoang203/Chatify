import { create } from "zustand";
import toast from "react-hot-toast";
import { io } from "socket.io-client";
import axiosInstance from "../utils/axiosUtil";
import { chatStore } from "./chatStore";

const BASE_URL = "ws://localhost:5173"

export const userStore = create((set, get) => ({
    loginUser : localStorage.getItem("loginUser") === null ? null : JSON.parse(localStorage.getItem("loginUser")),
    token : localStorage.getItem("token"),
    isLoggingIn : false,
    isSigningUp : false,
    isSignUpSuccess : false,
    socket: null,
    isConnectingSocket: false,

    setIsSignUpSuccess: async (isSuccess) => {
        set({isSignUpSuccess: isSuccess});
    },

    asyncConnectSocket: async () => {
        set({isConnectingSocket: false});
        try{
            console.log("Call async connect socket");
            get().connectSocket();
        }catch (error) {
            toast.error(error.message);
        }finally{
            set({isConnectingSocket: false});
        }
    },

    login: async (data) => {
        set({isLoggingIn : true});
        try {
            const res = await axiosInstance.post("/user/login", data);
            set({token : res.data.token});
            set({loginUser : res.data.data});
            toast.success(res.data.message);
            localStorage.setItem('token', get().token);
            localStorage.setItem('loginUser', JSON.stringify(get().loginUser));
            get().connectSocket();
        } catch (error) {
            console.log("Login error: ", error);
            if (error.status === 400) {
                toast.error(error.response.data.message);
            }else{
                toast.error(error.message);
            }
        } finally {
            set({isLoggingIn : false});
        }
    },

    signup: async (data) => {
        set({isSigningUp : true});
        try {
            const res = await axiosInstance.post("/user/sign-up", data);
            toast.success("data: " + JSON.stringify(res.data));
            set({loginUser: data});
            set({isSignUpSuccess: true});
            localStorage.setItem('loginUser', JSON.stringify(get().loginUser));
        } catch (error) {
            console.log("Signup error: ", error);
            if (error.status === 400) {
                toast.error(error.response.data.message);
            }else{
                toast.error(error.message);
            }
        } finally {
            set({isSigningUp : false});
        }
        return get().isSignUpSuccess;
    },

    logout: async () => {
        console.log('Đăng xuất...')
        localStorage.clear();
        set({loginUser: {"email": get().loginUser.email}});
        set({token: null});
        localStorage.setItem("loginUser", JSON.stringify(get().loginUser));
        get().disconnectSocket();
        chatStore.getState().setSelectedConversation(null);
    },

    connectSocket: () => {
        const { token } = get();
        if (!token || get().socket?.connected) return;
        console.log('Can connect socket!!!');
        const socket = io(BASE_URL);
        socket.connect();
        set({ socket: socket });
    },
    
    disconnectSocket: () => {
      if (get().socket?.connected) get().socket.disconnect();
    },
}))