# 🚀 GitHub Actions 설정 가이드

## 📋 필수 설정

### 1. Repository Settings

#### GitHub Pages 활성화
1. Repository → Settings → Pages
2. Source: "GitHub Actions" 선택
3. Save 클릭

#### Secrets 설정 (선택사항)
Repository → Settings → Secrets and variables → Actions에서 다음 추가:

- `DOCKER_HUB_USERNAME`: Docker Hub 사용자명 (선택)
- `DOCKER_HUB_ACCESS_TOKEN`: Docker Hub 액세스 토큰 (선택)

### 2. Permissions 설정

Repository → Settings → Actions → General:
- Workflow permissions: "Read and write permissions" 선택
- "Allow GitHub Actions to create and approve pull requests" 체크

### 3. 워크플로우 파일 구조

```
.github/
└── workflows/
    ├── update.yml    # 메인 자동 업데이트 워크플로우
    └── test.yml      # 테스트 워크플로우
```

## 🔄 자동 실행 스케줄

- **매일 09:00 KST**: 자동 데이터 업데이트
- **코드 변경시**: 자동 테스트 실행
- **수동 실행**: GitHub Actions 탭에서 언제든 실행 가능

## 📊 워크플로우 구성

### update.yml 주요 기능:

1. **📈 데이터 분석 업데이트**
   - 암호화폐 데이터 수집
   - 최적 MA 계산
   - 매매 신호 생성

2. **🌐 GitHub Pages 배포**
   - 정적 HTML 페이지 생성
   - 분석 결과 시각화
   - 자동 배포

3. **🐳 Docker 이미지 빌드**
   - 멀티 플랫폼 지원
   - 자동 태깅
   - Docker Hub 푸시 (선택)

4. **📢 알림 시스템**
   - 실패시 이슈 자동 생성
   - 완료 상태 요약
   - 상세 로그 제공

## 🛠️ 로컬 테스트

워크플로우를 로컬에서 테스트하려면:

```bash
# Act 설치 (GitHub Actions 로컬 실행 도구)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# 워크플로우 실행
act workflow_dispatch -W .github/workflows/update.yml
```

## 📋 체크리스트

배포 전 확인사항:

- [ ] Repository가 public으로 설정됨
- [ ] GitHub Pages가 활성화됨 
- [ ] 필요한 파일들이 모두 커밋됨
- [ ] requirements.txt가 최신 상태임
- [ ] data_processor.py가 정상 동작함
- [ ] 워크플로우 권한이 올바르게 설정됨

## 🐛 문제 해결

### 일반적인 문제들:

1. **권한 오류**
   - Repository Settings → Actions → General → Workflow permissions 확인

2. **Pages 배포 실패**
   - Repository Settings → Pages → Source가 "GitHub Actions"인지 확인

3. **종속성 설치 실패**
   - requirements.txt 파일 존재 확인
   - Python 버전 호환성 확인

4. **데이터 수집 실패**
   - 외부 API 접근 가능 여부 확인
   - 네트워크 연결 상태 확인

### 로그 확인 방법:

1. Repository → Actions 탭
2. 실행된 워크플로우 클릭
3. 각 job의 상세 로그 확인

## 🔧 커스터마이징

### 실행 시간 변경:
```yaml
schedule:
  - cron: '0 1 * * *'  # 매일 10:00 KST (01:00 UTC)
```

### 추가 알림 설정:
```yaml
- name: 📧 Send Email Notification
  if: success()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 587
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "✅ Crypto Analysis Updated"
    body: "Analysis completed successfully at ${{ steps.timestamp.outputs.time }}"
    to: your-email@example.com
```

## 📈 모니터링

워크플로우 실행 상태는 다음에서 확인:

- Repository badge로 상태 표시
- GitHub Actions 탭에서 실행 히스토리
- GitHub Pages URL에서 결과 확인
- 실패시 자동 생성되는 이슈

---

**💡 팁**: 첫 실행시에는 수동으로 "Run workflow"를 클릭하여 정상 동작을 확인하세요!
