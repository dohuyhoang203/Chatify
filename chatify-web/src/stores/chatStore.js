import { create } from "zustand";
import toast from "react-hot-toast";
import { userStore } from "./userStore";
import axiosInstance from "../utils/axiosUtil";

export const chatStore = create((set, get) => ({
  messages: [],
  conversations: [],
  selectedConversation: null,
  isConversationsLoading: false,
  isMessagesLoading: false,
  isCreateConversationOK: false,

  setIsCreateConversationOK: async (isSuccess) => {
      set({isCreateConversationOK: isSuccess});
  },

  getConversations: async () => {
    set({ isConversationsLoading: true });
    try {
      axiosInstance.defaults.headers.common['Authorization'] = localStorage.getItem("token");
      const res = await axiosInstance.get("/conversation/list");
      set({ conversations: res.data.data });
    } catch (error) {
      if (error.status === 400) {
          toast.error(error.response.data.message);
      }else if (error.status === 401) {
        console.log("Token expired");
        userStore.getState().logout();
      }else{
        toast.error(error.message);
      }
    } finally {
      set({ isConversationsLoading: false });
    }
  },

  getMessages: async (conversationId) => {
    set({ isMessagesLoading: true });
    try {
      axiosInstance.defaults.headers.common['Authorization'] = localStorage.getItem("token");
      const res = await axiosInstance.get(`/message/list?conversation_id=${conversationId}`);
      set({ messages: res.data.data });
    } catch (error) {
      if (error.status === 400) {
        toast.error(error.response.data.message);
      }else if (error.status === 401) {
        console.log("Token expired");
        userStore.getState().logout();
      }else{
          toast.error(error.message);
      }
    } finally {
      set({ isMessagesLoading: false });
    }
  },

  sendMessage: async (messageData) => {
    const { messages } = get();
    const socket = userStore.getState().socket;
    try {
      axiosInstance.defaults.headers.common['Authorization'] = localStorage.getItem("token");
      const res = await axiosInstance.post(`/message/send`, messageData);
      socket.emit("newMessage", messageData);
      set({ messages: [...messages, messageData] }); 
    } catch (error) {
      if (error.status === 400) {
          toast.error(error.response.data.message);
      }else if (error.status === 401) {
        console.log("Token expired");
        userStore.getState().logout();
      }else{
        toast.error(error.message);
      }
    }
  },

  subscribeToMessages: () => {
    const { selectedConversation } = get();
    if (!selectedConversation) return;

    const socket = userStore.getState().socket;

    socket.on("newMessage", (newMessage) => {
      const isMessageSentFromSelectedUser = newMessage.sender_id === selectedConversation.recipient_id;
      if (!isMessageSentFromSelectedUser) return;

      set({
        messages: [...get().messages, newMessage],
      });
    });
  },

  subScribeToConversation: () => {
    const socket = userStore.getState().socket;
    const loginUser = userStore.getState().loginUser;
    socket.on("newConversation", (newConversation) => {
      console.log("Receive newConversation");
      const isOwnConversation = newConversation.sender_id === loginUser._id;
      if (isOwnConversation) {
        set({
          conversations: [...get().conversations, newConversation],
        });
      }
    });
  },

  unsubscribeFromConversations: () => {
    const socket = userStore.getState().socket;
    socket.off("newConversation");
  },

  unsubscribeFromMessages: () => {
    const socket = userStore.getState().socket;
    socket.off("newMessage");
  },

  setSelectedConversation: (selectedConversation) => set({ selectedConversation }),

  createConversation: async (email) => {
    const {conversations} = get();
    const socket = userStore.getState().socket;
    const loginUser = userStore.getState().loginUser;
    try {
      axiosInstance.defaults.headers.common['Authorization'] = localStorage.getItem("token");
      const res = await axiosInstance.post(`/conversation/create`, {"email": email});
      let newConversation = res.data.data;
      set({ conversations: [...conversations, newConversation] }); 
      let newConversationSocket = {
        "_id": newConversation._id,
        "last_message_time": newConversation.last_message_time,
        "recipient_id": loginUser._id,
        "recipient_name": loginUser.username,
        "sender_id": newConversation.recipient_id,
        "sender_name": newConversation.recipient_name
      }
      socket.emit("newConversation", newConversationSocket);
      get().setSelectedConversation(newConversation);
      set({isCreateConversationOK: true});
    } catch (error) {
      if (error.status === 400) {
          toast.error(error.response.data.message);
      }else if (error.status === 401) {
        console.log("Token expired");
        userStore.getState().logout();
      }else{
          toast.error(error.message);
      }
    }
    return get().isCreateConversationOK;
  },
}));
