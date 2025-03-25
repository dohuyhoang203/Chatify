import { Image, Send, X } from "lucide-react";
import { useState } from "react";
import toast from "react-hot-toast";
import { chatStore } from "../stores/chatStore";
import { getUID, getNow } from "../utils/utils";
import { userStore } from "../stores/userStore";

const MessageInput = () => {
  const [ text, setText ] = useState("");
  const { sendMessage, selectedConversation } = chatStore();
  const { loginUser } = userStore();

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    try {
      await sendMessage({
        content: text.trim(),
        conversation_id: selectedConversation._id,
        _id: getUID(),
        sender_id: loginUser._id,
        recipient_id: selectedConversation.recipient_id,
        send_time: getNow()
      });

      // Clear form
      setText("");
    } catch (error) {
      toast.error("Gửi tin nhắn lỗi:", error);
    }
  };

  return (
    <div className="p-4 w-full">
    
        {/* <div className="mb-3 flex items-center gap-2">
          <div className="relative">
            <img
              src={"/vite.svg"}
              alt="Preview"
              className="w-20 h-20 object-cover rounded-lg border border-zinc-700"
            />
            <button
              className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-base-300
              flex items-center justify-center"
              type="button"
            >
              <X className="size-3" />
            </button>
          </div>
        </div> */}

        <form onSubmit={handleSendMessage} className="flex items-center gap-2">
            <div className="flex-1 flex gap-2">
            <input
                type="text"
                className="w-full input input-bordered rounded-lg input-sm sm:input-md"
                placeholder="Nhập tin nhắn..."
                value={text}
                onChange={(e) => setText(e.target.value)}
            />
            </div>
            <button
            type="submit"
            className="btn btn-sm btn-circle"
            disabled={!text.trim()}
            >
            <Send size={22} />
            </button>
        </form>
    </div>
  );
};
export default MessageInput;
