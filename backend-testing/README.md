
## 의존성 설치

```bash
# test와 dev 의존성 모두 설치
uv pip install -e ".[test,dev]"

# 또는 pyproject.toml의 모든 옵셔널 의존성 설치
uv pip install -e ".[all]"
```

## Test 돌릴 때 패스, 실패가 오락가락할 때

`pyproject.toml` 에서 pytest section에 `pythonpath` 항목에 `src` 추가.
```bash
uv pip install -e .
```

실행해서 개발모드 패키지 설치.

그 다음 VSCode 완전히 종료했다 실행.

