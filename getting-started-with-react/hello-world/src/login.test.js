import { test, expect } from '@playwright/test';

test.describe('로그인 시나리오', () => {
  test.beforeEach(async ({ page }) => {
    // 각 테스트 전, 로그인 페이지로 이동
    await page.goto('http://localhost:5173/login');
  });

  test('로그인 성공 시 홈 화면으로 이동', async ({ page }) => {
    // 이메일, 비밀번호 입력
    await page.fill('input[name="email"]', 'hannal@puddingcamp.com');
    await page.fill('input[name="password"]', 'test1234');

    // 클릭과 동시에 페이지 이동 기다리기
    await page.click('button[type="submit"]');

    // 홈 화면으로 잘 이동했는지 확인
    await expect(page.locator('h1')).toHaveText('홈 화면입니다');
  });

  test('로그인 실패 시 에러 메시지 표시', async ({ page }) => {
    // 잘못된 비밀번호
    await page.fill('input[name="email"]', 'hannal@puddingcamp.com');
    await page.fill('input[name="password"]', 'wrong_password');

    await page.click('button[type="submit"]');

    // 에러 메시지가 표시될 때까지 대기 후 확인
    const errorMessage = page.locator('.error-message');
    await expect(errorMessage).toHaveText('이메일 혹은 비밀번호가 올바르지 않습니다');
    
    // 필요 시 스크린샷 저장
    await page.screenshot({ path: 'screenshots/login-fail.png' });
  });
});