import './App.css';

import { useState } from 'react';

import Subscription from './Subscription';

function App() {
  const [email, setEmail] = useState("")
  return (
    <div>
      <h1>푸딩캠프 뉴스레터</h1>

      <p>
        <a href="https://pudding.camp/~/newsletter">푸딩캠프의 소식</a>을 이메일로 받아보세요.
      </p>

      <Subscription buttonLabel="구독하세요!" />

      {!!email && <p>입력한 E-mail 주소 : {email}</p>}
      {email ? <p>입력했당</p> : <p>입력 안 했당</p>}
    </div>
  )
}

export default App;
