# 📊 AI Stock Analysis with Llama 3.2 1B

AI 기반 미국 증시 분석 웹 앱 - 초경량 LLM으로 실시간 주식 정보와 뉴스 분석을 제공합니다.

## ✨ 주요 기능

- 🤖 **Llama 3.2 1B**: Meta의 최신 경량 LLM (2024년 9월)
- 📈 **실시간 증시 데이터**: Yahoo Finance API로 미국 주식 정보 제공
- 📰 **뉴스 수집 및 분석**: 최신 주식 뉴스 자동 수집
- 🧠 **AI 감성 분석**: LLM 기반 뉴스 감성 분석 (Positive/Negative/Neutral)
- 🎨 **Modern UI**: 직관적이고 반응형 웹 인터페이스

## 🚀 빠른 시작

### 1. 사전 요구사항

- Python 3.8+
- [Ollama](https://ollama.ai/) 설치

### 2. Ollama 설치 및 모델 다운로드

```bash
# Ollama 설치 (Mac/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Windows는 https://ollama.ai/download 에서 다운로드

# Llama 3.2 1B 모델 다운로드
ollama pull llama3.2:1b
```

### 3. 프로젝트 설치

```bash
# 저장소 클론
git clone <repository-url>
cd slm_prac

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 4. 서버 실행

```bash
# 방법 1: uvicorn 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: Python으로 실행
python -m app.main
```

### 5. 웹 브라우저에서 접속

```
http://localhost:8000
```

## 📁 프로젝트 구조

```
slm_prac/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 메인 애플리케이션
│   ├── llm.py           # Llama 3.2 1B 연동
│   ├── stock.py         # 증시 데이터 수집 (yfinance)
│   └── news.py          # 뉴스 수집
├── static/
│   ├── index.html       # 프론트엔드 HTML
│   ├── style.css        # 스타일시트
│   └── script.js        # JavaScript
├── requirements.txt     # Python 의존성
├── .gitignore
└── README.md
```

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Ollama**: 로컬 LLM 실행 환경
- **Llama 3.2 1B**: Meta의 초경량 언어 모델 (1B 파라미터)
- **yfinance**: Yahoo Finance API 래퍼
- **feedparser**: RSS 피드 파싱

### Frontend
- **Vanilla JavaScript**: 프레임워크 없이 순수 JS
- **Modern CSS**: Gradient, Flexbox, 애니메이션
- **Responsive Design**: 모바일 친화적

## 🔧 API 엔드포인트

### `POST /api/analyze`
주식 티커 분석

**Request:**
```json
{
  "ticker": "AAPL"
}
```

**Response:**
```json
{
  "ticker": "AAPL",
  "current_price": 178.23,
  "change_percent": 2.45,
  "summary": "AI generated analysis...",
  "sentiment": "Positive",
  "news": [...]
}
```

### `GET /api/trending`
인기 주식 티커 목록

### `POST /api/summarize`
텍스트 요약 (뉴스 요약 등)

### `GET /health`
서버 상태 확인

## 💡 사용 예시

1. **티커 입력**: `AAPL`, `TSLA`, `GOOGL` 등
2. **Analyze 버튼 클릭** 또는 **Enter 키**
3. **AI 분석 확인**:
   - 현재 가격 및 변동률
   - LLM 생성 분석 요약
   - 감성 분석 결과
   - 최신 뉴스 5개

## ⚡ 성능 최적화

- **Llama 3.2 1B**: CPU에서도 빠른 추론 (< 2초)
- **비동기 처리**: FastAPI의 async/await
- **경량 모델**: 1GB 미만 메모리 사용

## 🔍 주요 특징

### Llama 3.2 1B를 선택한 이유
- ✅ **초경량**: 1B 파라미터로 빠른 응답
- ✅ **로컬 실행**: API 비용 없음, 프라이버시 보장
- ✅ **최신 모델**: 2024년 9월 릴리스
- ✅ **충분한 성능**: 뉴스 분석, 요약, 감성 분석에 적합

## 🐛 문제 해결

### Ollama 연결 오류
```bash
# Ollama 서비스 시작
ollama serve

# 모델 확인
ollama list
```

### 포트 충돌
```bash
# 다른 포트로 실행
uvicorn app.main:app --port 8001
```

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 개별 설치
pip install fastapi uvicorn ollama yfinance feedparser
```

## 📝 향후 계획

- [ ] 차트 시각화 (Plotly/Chart.js)
- [ ] 포트폴리오 추적 기능
- [ ] 알림 기능 (가격 변동 알림)
- [ ] 다중 티커 비교
- [ ] 과거 데이터 분석

## 📄 라이선스

MIT License

## 🤝 기여

Issues와 Pull Requests를 환영합니다!

---

**Made with ❤️ using Llama 3.2 1B**
