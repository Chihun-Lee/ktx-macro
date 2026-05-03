# KTX Macro

본인 코레일 계정·본인 카드로 KTX/ITX-새마을/무궁화호 좌석을 폴링·예매·결제하는 macOS 개인 도구.

> ⚠ **개인용.** 자격증명·카드정보는 본인 Mac의 **macOS Keychain**에 암호화 저장됩니다. 서버는 `127.0.0.1:8911`에만 바인딩됩니다.
>
> ⚠ **법적 책임은 사용자 본인에게 있습니다.** 본인 계정·본인 카드 외 사용 금지. 영리적 사용 금지.

---

## 친구한테 보낼 1줄 가이드 (설치)

친구가 본인 Mac에서 **터미널을 열어** 아래 한 줄 붙여넣고 엔터:

```bash
curl -fsSL https://raw.githubusercontent.com/Chihun-Lee/ktx-macro/main/install.sh | bash
```

> 또는 [`KTX_매크로_설치.command`](https://github.com/Chihun-Lee/ktx-macro/raw/main/KTX_매크로_설치.command) 파일 다운로드 → Finder에서 **우클릭 → 열기**

설치 끝나면 **Launchpad → "KTX 매크로"** 검색 → 더블클릭. 종료는 **"KTX 매크로 종료"** 더블클릭.

---

## SRT 매크로와의 차이

| 항목 | SRT | KTX |
|------|-----|------|
| 라이브러리 | SRTrain | srtgo (lapis42, MIT) + Dynapath bypass (k-skill, MIT) |
| anti-bot | NetFunnel만 | **MACRO ERROR / Dynapath / Sid** — 패치 필요 |
| 결제 자동화 | ✅ 직접 API | ✅ srtgo의 pay_with_card |
| 포트 | 8910 | **8911** (동시 실행 가능) |
| 열차종류 | KTX(SRT)만 | KTX, ITX-새마을, 무궁화호, 누리로, ITX-청춘 등 |

---

## 기능

- 출발/도착/날짜/시각/열차종류/특정 열차 지정 → 백그라운드 폴링
- **폴링 간격: 1~30초 균등 랜덤** (트래픽 패턴 분산)
- 좌석 풀리면 즉시 예약, 결제 두 가지 모드:
  - **수동** — 예약만 잡고 GUI에 안내 → "결제 진행" 버튼 누르면 카드결제
  - **자동** — 예약 직후 즉시 결제
- 여러 작업 동시 실행
- Dynapath anti-bot 자동 우회 (`x-dynapath-m-token` + `Sid`)

---

## 직접 빌드 / 개발

```bash
git clone https://github.com/Chihun-Lee/ktx-macro.git
cd ktx-macro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py
# → http://127.0.0.1:8911
```

### 파일 구조

- `server.py` — FastAPI 엔트리
- `ktx_worker.py` — JobManager + 폴링/예약/결제 워커
- `ktx_korail.py` — 패치된 srtgo Korail (Dynapath bypass)
- `config.py` — 자격증명 Keychain 저장
- `static/index.html` — single-page GUI

### 의존성

- [srtgo](https://github.com/lapis42/srtgo) (MIT) — KTX `pay_with_card` 구현
- Dynapath bypass — [nomadamas/k-skill](https://github.com/nomadamas/k-skill) (MIT)에서 발췌

### 결제 deadline 처리

코레일은 예약 후 약 10분 안에 결제 안 하면 자동 취소합니다. 수동 모드는 9분(540초) 사용자 확인 대기 후 timeout error.
