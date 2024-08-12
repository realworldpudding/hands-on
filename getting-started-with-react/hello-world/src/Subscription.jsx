import { useState } from 'react';

function Subscription({ buttonLabel }) {
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
      <button>{buttonLabel}</button>
    </>
  )
}

export default Subscription;
