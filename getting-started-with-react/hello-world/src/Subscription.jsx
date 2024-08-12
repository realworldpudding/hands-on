import { useState } from 'react';

function Subscription({ buttonLabel, onSubscribe, children }) {
  const [email, setEmail] = useState("")

  const handleSubmit = () => {
    onSubscribe(email);
  }

  return (
    <>
      {children}
      <input
        type="text"
        placeholder="이메일 주소를 입력해주세요"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={handleSubmit}>{buttonLabel}</button>
    </>
  )
}

export default Subscription;
