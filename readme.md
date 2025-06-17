# 🏥 건강 불평등 분석 대시보드

대한민국 지역별 건강 불평등을 종합 분석하는 인터랙티브 대시보드입니다.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 주요 기능

### 📊 **7개 분석 섹션**
1. **🏥 지역별 건강 지표** - 음주율, 비만율, 흡연율, 신체활동율 분석
2. **🏥 의료 접근성** - 병원, 보건소, 의사 수 분석  
3. **💰 사회경제 지표** - 소득, 교육, 고용 분석
4. **📈 건강 불평등 종합 지수** - 서울=100 기준 통합 분석
5. **🗺️ 지역 클러스터링** - 유사 특성 지역 그룹화
6. **📊 정책 우선순위 매트릭스** - 지역별 맞춤형 정책 제안
7. **💡 정책 제안** - 단기/장기 개선 방안

### 🔗 **상관관계 분석**
- 건강 지표 간 상관관계
- 의료 접근성 상관관계  
- 사회경제 지표 상관관계

### 📥 **데이터 다운로드**
- 건강불평등 종합지수 (CSV)
- 지역 클러스터링 결과 (CSV)
- 정책 우선순위 매트릭스 (CSV)
- 지역별 정책 제안서 (CSV)

## 🚀 설치 및 실행

### 1. 레포지토리 클론
```bash
git clone https://github.com/yourusername/health_dashboard.git
cd health_dashboard
```

### 2. 가상환경 생성 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 앱 실행
```bash
streamlit run app.py
```

### 5. 브라우저에서 확인
- 로컬: `http://localhost:8501`
- 네트워크: `http://192.168.x.x:8501`

## 📁 데이터 구조

```
data/
├── health_region/          # 지역별 건강 지표
├── health_accessibility/   # 의료 접근성 데이터  
└── socioeconomic/         # 사회경제 지표
```

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Analysis**: 통계 분석, 클러스터링

## 📈 분석 방법론

### 건강 불평등 지수 계산
```
종합지수 = 건강행동(15%) + 의료접근성(35%) + 사회경제(50%)
```

### 클러스터링 기법
- 규칙 기반 클러스터링 (4개 그룹)
- 정규화된 가중평균 사용

### 정책 우선순위 산정
- 지역별 다차원 순위 분석
- 가중평균을 통한 종합 우선순위 도출

## 🎨 주요 시각화

- 📊 인터랙티브 히트맵
- 📈 상관관계 산점도
- 🎯 레이더 차트  
- 🏆 순위 막대 그래프
- 📋 종합 비교 차트

## 💡 정책 제안

### 단기 개선 방안 (1-2년)
- 🏥 의료 접근성 개선
- 🎯 건강증진 프로그램  
- 💰 경제적 지원

### 중장기 개선 방안 (3-5년)
- 🎯 지역균형발전
- 🎓 교육 격차 해소
- 🛡️ 사회안전망 강화
- 📊 데이터 기반 정책

## 🤝 기여하기

1. Fork 프로젝트
2. Feature 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 Push (`git push origin feature/AmazingFeature`)
5. Pull Request 오픈

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 👥 개발자

- **Your Name** - 초기 작업 - [YourGitHub](https://github.com/yourusername)

## 🙏 감사의 말

- 건강보험공단, 통계청 등 공공데이터 제공 기관
- Streamlit 커뮤니티
- 오픈소스 기여자들

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

