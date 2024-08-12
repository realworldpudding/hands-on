import './App.css';

import Subscription from './Subscription';

function App() {
  const handleSubscribe = (value) => {
    console.log('value from Subscription:', value);
  }

  return (
    <div>
      <h1>푸딩캠프 뉴스레터</h1>

      <Subscription buttonLabel="구독하세요!" onSubscribe={handleSubscribe}>
        {(title, email) => (
          <>
            <p>
              <a href="https://pudding.camp/~/newsletter">{title}</a>을 이메일로 받아보세요.
            </p>

            {!!email && <p>입력한 E-mail 주소 : {email}</p>}
            {email ? <p>입력했당</p> : <p>입력 안 했당</p>}
          </>
        )}
      </Subscription>
    </div>
  )
}

export default App;
