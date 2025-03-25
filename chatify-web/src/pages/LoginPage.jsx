import { Mail, EyeOff, Eye, Lock, MessageSquare, Loader2 } from "lucide-react";
import { useState } from "react"
import { Link } from "react-router-dom";

import {Toaster} from 'react-hot-toast';
import { userStore } from "../stores/userStore";


const LoginPage = () => {

  const [showPassword, setShowPassword] = useState(false);
  const {login, isLoggingIn, loginUser} = userStore();
  const [formData, setFormData] = useState({
    "email": loginUser === null ? "" : loginUser.email,
    "password": ""
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submit email: ', formData.email);
    console.log('isLoggingIn: ', isLoggingIn);
    login(formData);
  };

  return (
    <div className="h-screen grid lg:grid-cols-2">
      {/* Left Side - Form */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="flex flex-col items-center gap-2 group">
              
              <h1 className="text-2xl font-bold mt-2">Chào mừng quay trở lại</h1>
              <p className="text-base-content/60">Đăng nhập tài khoản của bạn</p>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Email</span>
              </label>
              <div className="relative">
                <input
                  type="email"
                  className={`input input-bordered w-full pl-10`}
                  placeholder="you@example.com"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-base-content/40" />
                </div>
              </div>
            </div>

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Mật khẩu</span>
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  className={`input input-bordered w-full pl-10`}
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={(e) => setFormData({...formData, password: e.target.value})}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-base-content/40" />
                </div>
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-base-content/40" />
                  ) : (
                    <Eye className="h-5 w-5 text-base-content/40" />
                  )}
                </button>
              </div>
            </div>

            <button type="submit" className="btn btn-primary w-full" disabled={isLoggingIn}>
                  {
                    isLoggingIn ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        Đang tải...
                      </>
                    ) : (
                      "Đăng nhập"
                    )
                  }
            </button>
          </form>

          <div className="text-center">
            <p className="text-base-content/60">
              Bạn chưa có tài khoản?{" "}
              <Link to="/signup" className="link link-primary">
                Tạo tài khoản
              </Link>
            </p>
          </div>
          <Toaster />
        </div>
      </div>
      <div className="bg-cover bg-center"  style={{
        backgroundImage: "url(/login-bg.png)",
      }}>

      </div>
    </div>
  )
}

export default LoginPage