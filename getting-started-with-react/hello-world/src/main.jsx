import React from 'react';

import { createRoot } from 'react-dom/client';

const rootElement = React.createElement(
  'div',
  {
    style: {
      color: '#1A8DF7',
      fontWeight: 'bold',
    },
  },
  'Hello World!',
  ...[
    React.createElement('p', null, '푸딩캠프에 오신 걸 환영합니다!'),
    React.createElement(
      'p',
      null,
      '컨텐츠',
      React.createElement(
        'ul',
        null,
        React.createElement('li', null, '시리즈'),
        React.createElement('li', null, '커피챗'),
        React.createElement('li', null, '소식지'),
      ),
    ),
    React.createElement('p', null, '커피챗'),
    React.createElement('p', null, '푸딩까페'),
    React.createElement('p', null, '뉴스레터'),
  ]
);

const container = document.getElementById('root');
const root = createRoot(container)
root.render(rootElement);
