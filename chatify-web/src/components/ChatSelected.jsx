import { useEffect, useRef } from "react";
import { chatStore } from "../stores/chatStore";
import { userStore } from "../stores/userStore";
import ChatHeader from "./ChatHeader";
import MessagesInLoad from "./MessagesInLoad";
import MessageInput from "./MessageInput";

const ChatSelected = () => {
  const {
    messages,
    getMessages,
    isMessagesLoading,
    selectedConversation,
    subscribeToMessages,
    unsubscribeFromMessages,
  } = chatStore();
  const { loginUser } = userStore();
  const messageEndRef = useRef(null);

  useEffect(() => {
    getMessages(selectedConversation._id);

    subscribeToMessages();

    return () => unsubscribeFromMessages();
  }, [selectedConversation._id, getMessages, subscribeToMessages, unsubscribeFromMessages]);

  useEffect(() => {
    if (messageEndRef.current && messages) {
      messageEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  if (isMessagesLoading) {
    return (
      <div className="flex-1 flex flex-col overflow-auto">
        <ChatHeader />
        <MessagesInLoad />
        <MessageInput />
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col overflow-auto">
      <ChatHeader />

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message._id}
            className={`chat ${message.sender_id === loginUser._id ? "chat-end" : "chat-start"}`}
            ref={messageEndRef}
          >
            <div className=" chat-image avatar">
              <div className="size-10 rounded-full border">
                <img
                  src={
                    "/avatar.png"
                  }
                  alt="profile pic"
                />
              </div>
            </div>
            <div className="chat-header mb-1">
              <time className="text-xs opacity-50 ml-1">
                {message.send_time}
              </time>
            </div>
            <div className="chat-bubble flex flex-col">
              {message.content && <p>{message.content}</p>}
            </div>
          </div>
        ))}
      </div>

      <MessageInput />
    </div>
  );
};
export default ChatSelected;