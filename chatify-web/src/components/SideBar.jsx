import { useEffect, useState } from "react";
import { MessageSquare, Plus, Users } from "lucide-react";
import { chatStore } from "../stores/chatStore";
import SideBarInLoad from "./SideBarInLoad";
import { userStore } from "../stores/userStore";

const Sidebar = () => {
  const { getConversations, conversations, selectedConversation, setSelectedConversation, isConversationsLoading, createConversation, setIsCreateConversationOK, subScribeToConversation, unsubscribeFromConversations } = chatStore();
  const [emailCreateConversation, setEmailCreateConversation] = useState("");
  const {asyncConnectSocket} = userStore();

  useEffect(() => {
    asyncConnectSocket();
    getConversations();

    subScribeToConversation();

    return () => unsubscribeFromConversations();
  }, [getConversations, subScribeToConversation, unsubscribeFromConversations, asyncConnectSocket]);

  if (isConversationsLoading) return <SideBarInLoad />;

  const handleCreateConversation = async (e) => {
    e.preventDefault();
    console.log("Call create conversation");
    let isSuccess = await createConversation(emailCreateConversation);
    if (isSuccess) {
        document.getElementById('my_modal_4').close();
        setIsCreateConversationOK(false);
    }
  }

  return (
    <aside className="h-full w-20 lg:w-72 border-r border-base-300 flex flex-col transition-all duration-200">
      <div className="border-b border-base-300 w-full p-5">
        <div className="flex items-center gap-2">
          <MessageSquare className="size-6" />
          <span className="font-medium hidden lg:block">Danh sách hội thoại</span>
          <button className="btn" onClick={()=>document.getElementById('my_modal_4').showModal()}><Plus /></button>
            <dialog id="my_modal_4" className="modal">
            <div className="modal-box w-5/12 max-w-5xl">
                <form method="dialog">
                    <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
                </form>
                <h3 className="font-bold text-lg">Trò chuyện!</h3>
                <p className="py-4">Hãy nhập email người bạn muốn trò chuyện</p>
                <div className="modal-action mt-1">
                <form onSubmit={handleCreateConversation} method="dialog" className="flex flex-3/4 justify-center">
                    {/* if there is a button, it will close the modal */}
                    <input type="email" placeholder="Email" value={emailCreateConversation} onChange={(e) => {setEmailCreateConversation(e.target.value)}} className="w-full input input-bordered rounded-lg input-sm sm:input-md" />
                    <button className="btn mx-2">Tạo hội thoại</button>
                </form>
                </div>
            </div>
            <form method="dialog" className="modal-backdrop">
                <button>close</button>
            </form>
            </dialog>
        </div>
      </div>

      <div className="overflow-y-auto w-full py-3">
        {conversations.map((conversation) => (
          <button
            key={conversation._id}
            onClick={() => setSelectedConversation(conversation)}
            className={`
              w-full p-3 flex items-center gap-3
              hover:bg-base-300 transition-colors
              ${selectedConversation?._id === conversation._id ? "bg-base-300 ring-1 ring-base-300" : ""}
            `}
          >
            <div className="relative mx-auto lg:mx-0">
              <img
                src={"/avatar.png"}
                alt={conversation.recipient_name}
                className="size-12 object-cover rounded-full"
              />
            </div>

            {/* User info - only visible on larger screens */}
            <div className="hidden lg:block text-left min-w-0">
              <div className="font-medium truncate">{conversation.recipient_name}</div>
              <div className="text-sm text-zinc-400">
                {conversation.snippet}
              </div>
              <div className="text-sm text-zinc-400">
                {conversation.last_message_time}
              </div>
            </div>
          </button>
        ))}

        {conversations.length === 0 && (
          <div className="text-center text-zinc-500 py-4">Bạn chưa có tin nhắn nào</div>
        )}
      </div>
    </aside>
  );
};
export default Sidebar;