import React from 'react'
import { Navigate, Route, Routes } from 'react-router'
import ChatPage from './pages/ChatPage'
import HomePage from './pages/HomePage'
import SignUpPage from './pages/SignUpPage'
import LoginPage from './pages/LoginPage'
import { userStore } from './stores/userStore'
import { Loader } from 'lucide-react'

const App = () => {

  const { token } = userStore();

  return (
    <>
      <Routes>
        <Route path="/" element={token ? <HomePage /> : <Navigate to="/login" />} />
        <Route path="/chat" element={token ? <ChatPage /> : <Navigate to="/login"/>} />
        <Route path="/signup" element={token === null ? <SignUpPage /> : <Navigate to="/" />} />
        <Route path="/login" element={token === null ? <LoginPage /> : <Navigate to="/" />} />
      </Routes>
    </>
  )
}

export default App