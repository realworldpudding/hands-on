import { useState } from 'react';

function Subscription() {
  const [email, setEmail] = useState("")
  return (
    <>
      <input
        type="text"
        placeholder="이메일 주소를 입력해주세요"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className={['email-input', email ? 'email-input--entered' : '']}
      />
      <button>구독하기</button>
    </>
  )
}

export default Subscription;
