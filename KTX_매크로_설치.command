#!/bin/bash
# KTX 매크로 설치 (더블클릭 실행용)
# - 처음 실행 시 macOS가 "확인되지 않은 개발자" 경고를 띄울 수 있음
#   → 우클릭 → 열기 → 다시 우클릭 → 열기 → "열기" 버튼 클릭
exec /bin/bash -c 'curl -fsSL https://raw.githubusercontent.com/Chihun-Lee/ktx-macro/main/install.sh | bash'
