import { Mail, Phone, ShieldUser, Eye, EyeOff, Lock, Loader2 } from 'lucide-react';
import React, { useState } from 'react'
import { userStore } from '../stores/userStore';
import { Link, useNavigate } from 'react-router';
import { Toaster } from 'react-hot-toast';

const SignUpPage = () => {

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [formData, setFormData] = useState({
    "username": "",
    "email": "",
    "phone_number": "",
    "password": "",
    "confirm_password": ""
  })
  let navigate = useNavigate();
  const {isSigningUp, signup, setIsSignUpSuccess} = userStore();
  const handleSubmit = async (e) => {
    e.preventDefault();
    let isSuccess = await signup(formData);
    console.log(isSuccess);
    if (isSuccess) {
      console.log("navigate login");
      navigate('/login');
      setIsSignUpSuccess(false);
    }
  };

  return (
    <div className="h-screen grid lg:grid-cols-2">
      {/* Left Side - Form */}
      <div className="flex flex-col justify-center items-center p-6 sm:p-12">
        <div className="w-full max-w-md space-y-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="flex flex-col items-center gap-2 group">
              
              <h1 className="text-2xl font-bold mt-2">Đăng ký tài khoản</h1>
              <p className="text-base-content/60">Hãy nhập thông tin của bạn để tham gia</p>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Tên tài khoản</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  className={`input input-bordered w-full pl-10`}
                  placeholder="your_username"
                  value={formData.username}
                  onChange={(e) => setFormData({...formData, username: e.target.value})}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <ShieldUser className="h-5 w-5 text-base-content/40" />
                </div>
              </div>
            </div>

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
                <span className="label-text font-medium">Số điện thoại</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  className={`input input-bordered w-full pl-10`}
                  placeholder="0987xxxxxx"
                  value={formData.phone_number}
                  onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Phone className="h-5 w-5 text-base-content/40" />
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

            <div className="form-control">
              <label className="label">
                <span className="label-text font-medium">Xác nhận mật khẩu</span>
              </label>
              <div className="relative">
                <input
                  type={showConfirmPassword ? "text" : "password"}
                  className={`input input-bordered w-full pl-10`}
                  placeholder="••••••••"
                  value={formData.confirm_password}
                  onChange={(e) => setFormData({...formData, confirm_password: e.target.value})}
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-base-content/40" />
                </div>
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeOff className="h-5 w-5 text-base-content/40" />
                  ) : (
                    <Eye className="h-5 w-5 text-base-content/40" />
                  )}
                </button>
              </div>
            </div>

            <button type="submit" className="btn btn-primary w-full" disabled={isSigningUp}>
                  {
                    isSigningUp ? (
                      <>
                        <Loader2 className="h-5 w-5 animate-spin" />
                        Đang tải...
                      </>
                    ) : (
                      "Đăng ký"
                    )
                  }
            </button>
          </form>

          <div className="text-center">
            <p className="text-base-content/60">
              Bạn đã có tài khoản?{" "}
              <Link to="/login" className="link link-primary">
                Đăng nhập
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

export default SignUpPage