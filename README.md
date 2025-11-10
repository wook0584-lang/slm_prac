# 📊 AI Stock + PDF Analyzer with Llama 3.2 1B

AI 기반 **미국 증시 분석** + **PDF 문서 분석** 웹 앱 - 초경량 LLM으로 실시간 주식 정보, 뉴스 분석, PDF 문서 분석을 제공합니다.

## ✨ 주요 기능

### 📈 주식 분석
- 🤖 **Llama 3.2 1B**: Meta의 최신 경량 LLM (2024년 9월)
- 📊 **Alpha Vantage API**: 안정적인 실시간 주식 데이터 (Yahoo Finance fallback)
- 📰 **뉴스 수집**: Yahoo Finance에서 최신 뉴스 자동 수집
- 🧠 **AI 감성 분석**: LLM 기반 뉴스 감성 분석 (Positive/Negative/Neutral)

### 📄 PDF 문서 분석 (NEW!)
- 📤 **PDF 업로드**: 재무제표, 실적 보고서, 뉴스 기사 등 (최대 10MB)
- 🔍 **AI 분석**:
  - 요약 (Summary)
  - 감성 분석 (Sentiment)
  - 재무 분석 (Financial)
- 🎯 **주식 연계 분석**: 특정 주식(티커)과 연관하여 PDF 분석
- 💡 **투자 인사이트**: LLM이 문서에서 핵심 정보 추출 및 해석

### 🎨 UI/UX
- 탭 기반 인터페이스 (주식 분석 / PDF 분석)
- 드래그 & 드롭 파일 업로드
- 반응형 웹 디자인 (모바일 친화적)

## 🚀 빠른 시작

### 1. 사전 요구사항

- Python 3.8+
- [Ollama](https://ollama.ai/) 설치
- **Alpha Vantage API 키** (무료, 권장)

### 2. Ollama 설치 및 모델 다운로드

```bash
# Ollama 설치 (Mac/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Windows는 https://ollama.ai/download 에서 다운로드

# Llama 3.2 1B 모델 다운로드
ollama pull llama3.2:1b
```

### 3. Alpha Vantage API 키 발급 (중요!)

1. https://www.alphavantage.co/support/#api-key 에서 무료 API 키 발급 (30초)
2. 이메일로 API 키 수신

### 4. 프로젝트 설치

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

### 5. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
nano .env  # 또는 vi, code 등

# 아래 내용 입력:
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

⚠️ **중요**: API 키를 입력하지 않으면 Yahoo Finance로 fallback되며, rate limiting이 발생할 수 있습니다.

### 6. 서버 실행

```bash
# 방법 1: uvicorn 직접 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: Python으로 실행
python -m app.main
```

### 7. 웹 브라우저에서 접속

```
http://localhost:8000
```

## 📁 프로젝트 구조

```
slm_prac/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI 메인 앱
│   ├── llm.py                 # Llama 3.2 1B 연동
│   ├── stock.py               # Yahoo Finance (fallback)
│   ├── stock_alphavantage.py  # Alpha Vantage API
│   ├── news.py                # 뉴스 수집
│   └── pdf_analyzer.py        # PDF 분석 (NEW!)
├── static/
│   ├── index.html             # 프론트엔드 HTML
│   ├── style.css              # 스타일시트
│   ├── script.js              # JavaScript
│   └── favicon.svg            # 파비콘
├── requirements.txt           # Python 의존성
├── .env.example               # 환경 변수 템플릿
├── .gitignore
└── README.md
```

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Ollama**: 로컬 LLM 실행 환경
- **Llama 3.2 1B**: Meta의 초경량 언어 모델 (1B 파라미터)
- **Alpha Vantage**: 주식 시장 데이터 API (주)
- **yfinance**: Yahoo Finance API 래퍼 (fallback)
- **PyPDF2**: PDF 텍스트 추출

### Frontend
- **Vanilla JavaScript**: 프레임워크 없이 순수 JS
- **Modern CSS**: Gradient, Flexbox, 탭 UI
- **Responsive Design**: 모바일 친화적

## 🔧 API 엔드포인트

### 주식 분석
- `POST /api/analyze` - 주식 티커 분석
- `GET /api/trending` - 인기 주식 목록
- `POST /api/summarize` - 텍스트 요약

### PDF 분석 (NEW!)
- `POST /api/analyze-pdf` - PDF 문서 분석
  - 파라미터: `file` (PDF), `analysis_type` (summary/sentiment/financial)
- `POST /api/analyze-pdf-with-stock` - 주식 연계 PDF 분석
  - 파라미터: `file` (PDF), `ticker` (주식 티커)

## 💡 사용 예시

### 주식 분석
1. 📈 **Stock Analysis** 탭 클릭
2. 티커 입력 (예: `AAPL`, `TSLA`, `NVDA`)
3. **Analyze** 버튼 클릭
4. 결과 확인:
   - 현재 가격 & 변동률
   - AI 생성 분석 요약
   - 감성 분석 (Positive/Neutral/Negative)
   - 최신 뉴스 5개

### PDF 분석 (NEW!)
1. 📄 **PDF Analysis** 탭 클릭
2. PDF 파일 드래그 & 드롭 또는 클릭하여 업로드
3. 분석 유형 선택:
   - **Summary**: 문서 요약
   - **Financial Analysis**: 재무 정보 추출
   - **Sentiment Analysis**: 문서 감성 분석
4. (선택) 특정 주식과 연관 분석:
   - "Analyze in context of specific stock" 체크
   - 티커 입력 (예: `AAPL`)
5. **Analyze PDF with AI** 버튼 클릭
6. AI 분석 결과 확인

## ⚡ 성능 최적화

- **Llama 3.2 1B**: CPU에서도 빠른 추론 (< 2초)
- **비동기 처리**: FastAPI의 async/await
- **경량 모델**: 1GB 미만 메모리 사용
- **Alpha Vantage**: Rate limiting 관대 (500 요청/일)

## 🔍 Alpha Vantage vs Yahoo Finance

| | **Alpha Vantage** | **Yahoo Finance** |
|---|---|---|
| 안정성 | ⭐⭐⭐⭐⭐ | ⭐⭐ (불안정) |
| Rate Limit | 500 요청/일 | 매우 엄격 (429 에러 빈발) |
| API 키 | 필요 (무료) | 불필요 |
| 데이터 품질 | 공식 API | 웹 스크래핑 기반 |
| **추천** | ✅ **적극 권장** | ❌ Fallback용 |

💡 **반드시 Alpha Vantage API 키를 설정하세요!**

## 🐛 문제 해결

### Ollama 연결 오류
```bash
# Ollama 서비스 시작
ollama serve

# 모델 확인
ollama list
```

### Alpha Vantage API 키 오류
```bash
# .env 파일 확인
cat .env

# API 키가 "your_api_key_here"가 아닌지 확인
# 실제 API 키로 변경 필요
```

### PDF 업로드 실패
- 파일 크기: 최대 10MB
- 파일 형식: `.pdf`만 지원
- 텍스트 기반 PDF만 분석 가능 (스캔 이미지 PDF는 제한적)

### 포트 충돌
```bash
# 다른 포트로 실행
uvicorn app.main:app --port 8001
```

## 📝 향후 계획

- [ ] 차트 시각화 (Plotly/Chart.js)
- [ ] OCR 지원 (스캔된 PDF 분석)
- [ ] 다중 PDF 비교 분석
- [ ] 포트폴리오 추적 기능
- [ ] 알림 기능 (가격 변동 알림)
- [ ] 엑셀/CSV 내보내기

## 📄 라이선스

MIT License

## 🤝 기여

Issues와 Pull Requests를 환영합니다!

## 🙏 Credits

- **Llama 3.2 1B**: Meta AI
- **Alpha Vantage**: https://www.alphavantage.co/
- **Ollama**: https://ollama.ai/
- **FastAPI**: https://fastapi.tiangolo.com/

---

**Made with ❤️ using Llama 3.2 1B | Powered by Alpha Vantage API**
