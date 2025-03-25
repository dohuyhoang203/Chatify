import NavBar from '../components/NavBar'
import SideBar from '../components/SideBar'
import NoChatSelected from '../components/NoChatSelected'
import ChatSelected from '../components/ChatSelected'
import { chatStore } from '../stores/chatStore'
import { Toaster } from 'react-hot-toast'

const ChatPage = () => {
  const { selectedConversation } = chatStore();
  return (
    <>
      <NavBar />
      <div className="h-screen bg-base-200 bg-cover bg-center" style={{
        backgroundImage: "url(/login-bg.png)",
      }}>
        <div className="flex items-center justify-center pt-20 px-4">
          <div className="bg-base-100 rounded-lg shadow-cl w-full max-w-6xl h-[calc(100vh-8rem)]">
            <div className="flex h-full rounded-lg overflow-hidden">
              <SideBar />

              {!selectedConversation ? <NoChatSelected /> : <ChatSelected />}
              <Toaster />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default ChatPage