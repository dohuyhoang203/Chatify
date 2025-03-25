import { X } from "lucide-react";
import { chatStore } from "../stores/chatStore";

const ChatHeader = () => {
  const { selectedConversation, setSelectedConversation } = chatStore();
  return (
    <div className="p-2.5 border-b border-base-300">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Avatar */}
          <div className="avatar">
            <div className="size-10 rounded-full relative">
              <img src={"/avatar.png"} />
            </div>
          </div>

          {/* User info */}
          <div>
            <h3 className="font-medium">{selectedConversation === null ? "--" : selectedConversation.recipient_name}</h3>
            <p className="text-sm text-base-content/70">
              {"-"}
            </p>
          </div>
        </div>

        {/* Close button */}
        <button onClick={() => setSelectedConversation(null)}>
          <X />
        </button>
      </div>
    </div>
  );
};
export default ChatHeader;
