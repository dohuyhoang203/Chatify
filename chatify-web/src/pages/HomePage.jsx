import React from 'react';
import {Toaster} from 'react-hot-toast';
import { Link } from 'react-router';
import { userStore } from '../stores/userStore';
import NavBar from '../components/NavBar';

const HomePage = () => {

  const {loginUser} = userStore();
  console.log(loginUser);

  return (
    <>
      <NavBar />
      <div
        className="hero min-h-screen"
        style={{
          backgroundImage: "url(/login-bg.png)",
        }}>
        <div className="hero-overlay"></div>
        <div className="hero-content text-neutral-content text-center">
          <div className="max-w-md">
            <h1 className="mb-5 text-5xl font-bold">Xin chào {loginUser.email}</h1>
            <p className="mb-5">
              Hãy khám phá tất cả các tính năng, làm quen vài người bạn mới hoặc giữ liên lạc với gia đình, bạn bè và nửa kia của bạn.
            </p>
            <Link to="/chat" className="btn btn-primary">Bắt đầu</Link>
          </div>
        </div>
      </div>
      <Toaster />
    </>
  )
}

export default HomePage