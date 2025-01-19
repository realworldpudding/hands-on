import { useState } from 'react';

const Login = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleSuccess = async () => {
    setIsLoggedIn(true)
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h1 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {isLoggedIn ? '홈 화면입니다' : '로그인'}
          </h1>
        </div>
        {isLoggedIn ? (
          <div>
            <p>로그인 성공</p>
          </div>
        ) : (
          <LoginForm onSuccess={handleSuccess} />
        )}
      </div>
    </div>
  );
};

function LoginForm({ onSuccess }) {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // 입력이 변경되면 에러 메시지 초기화
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // 여기서는 예시로 간단한 유효성 검사만 수행
      if (formData.email === 'hannal@puddingcamp.com' && formData.password === 'test1234') {
        // 로그인 성공 시 홈으로 이동
        onSuccess()
      } else {
        setError('이메일 혹은 비밀번호가 올바르지 않습니다');
      }
    } catch (err) {
      setError('로그인 중 오류가 발생했습니다. 다시 시도해주세요.');
    }
  };
 
  return (
    <div>
      
      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
        <div className="rounded-md shadow-sm space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              이메일 주소
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="example@email.com"
              value={formData.email}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              비밀번호
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="비밀번호를 입력하세요"
              value={formData.password}
              onChange={handleInputChange}
            />
          </div>
        </div>

        {error && (
          <div className="error-message text-red-500 text-sm text-center" role="alert">
            {error}
          </div>
        )}

        <button
          type="submit"
          className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          로그인
        </button>
      </form>
      <div className="text-center">
        <a href="/signup" className="text-sm text-blue-600 hover:text-blue-500 signup">
          계정이 없으신가요? 회원가입
        </a>
      </div>
    </div>
  );
}

export default Login;