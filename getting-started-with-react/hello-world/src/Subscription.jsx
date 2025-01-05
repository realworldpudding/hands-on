import { useState, useEffect, useRef } from 'react';

function Subscription({ buttonLabel, onSubscribe, children }) {
  const [email, setEmail] = useState("")
  const inputRef = useRef(null);

  const handleSubmit = () => {
    onSubscribe(email);
  }

  useEffect(() => {
    const tid = setInterval(() => {
      if(email) {
        return;
      }
      inputRef.current.focus();
    }, 5000);

    return () => clearInterval(tid);
  }, [email]);
  
  return (
    <>
      {children instanceof Function ? children('학습과 성장 컨텐츠 소식', email) : children}
      <input
        ref={inputRef}
        type="text"
        placeholder="이메일 주소를 입력해주세요"
        value={email}
        onChange={(e) => {
          const newValue = e.target.value;
          setEmail(newValue);
        }}
      />
      <button role="button" aria-label={buttonLabel} onClick={handleSubmit}>{buttonLabel}</button>
    </>
  )
}

export default Subscription;
