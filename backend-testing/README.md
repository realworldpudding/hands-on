
## 의존성 설치

```bash
# test와 dev 의존성 모두 설치
uv pip install -e ".[test,dev]"

# 또는 pyproject.toml의 모든 옵셔널 의존성 설치
uv pip install -e ".[all]"
```
