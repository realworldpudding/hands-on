import { useState } from 'react';

const posts = [
    { id: 240, title: '이력서를 읽긴 읽은 걸까요?', url: 'https://puddingcamp.com/topic/did-they-even-read-my-resume' },
    { id: 230, title: 'React에 입문하기', url: 'https://puddingcamp.com/topic/getting-started-with-react' },
    { id: 220, title: '정보처리모델로 수업 혁신하기 : 6단계 학습모형 적용', url: 'https://puddingcamp.com/topic/learning-science-lecture-6-apply-6-step-model' },
    { id: 210, title: '그때 왜 그런 행동을 한 거예요? 그럼 왜 그런 거예요? 왜죠?', url: 'https://puddingcamp.com/topic/why-you-chose-that-moment-to-act-that-way' },
    { id: 200, title: '취업은 드레스 코드가 맞는 곳을 찾는 여정입니다', url: 'https://puddingcamp.com/topic/trust-yourself-and-find-right-job-for-you' },
    { id: 190, title: 'console.log만 쓰지 말고 더 다양하게 쓰기', url: 'https://puddingcamp.com/topic/use-more-than-console-log' },
    { id: 180, title: '회사에서 성장을 할 수 없을 것 같다는 2년차 개발자', url: 'https://puddingcamp.com/topic/junior-feels-no-growth-at-company' },
    { id: 170, title: '대학 학습공동체에서 팀 성취목표지향성에 대한 팀 효능감 및 과제 가치의 영향', url: 'https://puddingcamp.com/topic/doi-10_26857-jlls_2018_11_14_4_231' },
    { id: 160, title: '사수가 없는 저는 어떻게 학습하고 성장하나요?', url: 'https://puddingcamp.com/topic/learning-methods-for-growth-without-a-coach' },
    { id: 150, title: 'Django의 모델단에 Async 사용하기', url: 'https://puddingcamp.com/topic/django-database-in-async-context' },
    { id: 140, title: '취업 못하면 길에 나앉을지도 모른다고요?', url: 'https://puddingcamp.com/topic/afraid-of-being-homeless-if-they-cant-find-a-job' },
    { id: 130, title: 'Python Doctest로 함수의 테스트 코드 작성하기', url: 'https://puddingcamp.com/topic/python-doctest-with-pytest' },
    { id: 120, title: '비전공 출신인 신입 개발자의 소극적인 이력서를 멘토링하다', url: 'https://puddingcamp.com/topic/mentoring-passive-resume-of-non-major-junior-developer' },
    { id: 110, title: '우리의 취약성은 서로를 연결하고 강하게 만들어 줍니다.', url: 'https://puddingcamp.com/topic/vulnerability-connect-us-and-make-us-stronger' },
    { id: 100, title: '크롬 브라우저에 내장된 AI API를 사용해서 웹페이지 요약해보기', url: 'https://puddingcamp.com/topic/summarize-webpage-by-window-ai-in-chrome' },
    { id: 90, title: 'HTML 문서를 확장하다, htmx', url: 'https://puddingcamp.com/topic/htmx-on-puddingcamp' },
    { id: 80, title: '할 일 관리 서비스 만들며 FastAPI에 입문하기 [연재 완료]', url: 'https://puddingcamp.com/topic/todo-app-for-fastapi-beginner' },
    { id: 70, title: 'Django 5에 새롭게 도입된 GeneratedField', url: 'https://puddingcamp.com/topic/django5-generated-field' },
    { id: 60, title: 'Python 객체 이야기', url: 'https://puddingcamp.com/topic/essential-for-python-object' },
    { id: 50, title: '윈도우 PowerShell 보안정책 설치', url: 'https://puddingcamp.com/topic/windows-powershell-security-policy' },
    { id: 40, title: 'Django의 View에 비동기', url: 'https://puddingcamp.com/topic/async-view-on-django' },
    { id: 30, title: '인공지능 음성합성기 구현하기', url: 'https://puddingcamp.com/topic/ai-tts-implementation' },
    { id: 20, title: '기능과 UI를 분리하는 Headless Component 이야기', url: 'https://puddingcamp.com/topic/headless-component-in-puddingcamp' },
    { id: 10, title: '맥OS에서 지셸(zsh, Z Shell) 시작하기 [연재 완료]', url: 'https://puddingcamp.com/topic/hello-zsh-on-macos' },
    { id: 1, title: 'Visual Studio Code 입문 과정 [연재 완료]', url: 'https://puddingcamp.com/topic/vscode-beginner' },
];

const perPage = 5;

function ContentList() {
  const page = 1;
  const start = (page - 1) * perPage;
  const end = start + perPage;
  
  return (
    <div>
      {
        posts.slice(start, end).map((post) => (
          <div key={post.id}>
            <h2><a href={post.url}>{post.title}</a></h2>
          </div>
        ))
      }
    </div>
  )
}

export default ContentList;

