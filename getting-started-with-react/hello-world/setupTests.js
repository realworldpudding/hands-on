import '@testing-library/jest-dom/vitest';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// 테스트 매처 확장
expect.extend(matchers);

// 각 테스트 후 클린업
afterEach(() => {
  cleanup();
}); 