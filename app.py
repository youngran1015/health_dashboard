import streamlit as st
import health_charts  # 👈 별도 모듈 import
import inequality_index
import regional_clustering  
import policy_matrix
# import future_scenarios  # 제거

# 페이지 설정
st.set_page_config(
    page_title="건강 불평등 시각화 대시보드",
    page_icon="🏥",
    layout="wide",
)

# 상단 여백 줄이기
st.markdown("""
    <style>
        .block-container {
            padding-top:  0rem !important;
            padding-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# 상단 고정 배너
st.markdown("""
<div style="
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 50px;
    background-color: rgba(15, 23, 42, 0.85);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
">
    <span style="
        color: #F3F4F6;
        font-size: 18px;
        font-weight: bold;
    ">
        건강 불평등 조사 프로젝트
    </span>
</div>
""", unsafe_allow_html=True)

# 사이드바 스타일 및 탐색 메뉴
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 5px solid #F97316;
        }

        [data-testid="stSidebar"] * {
            color: #F3F4F6;
            font-weight: 500;
        }

        .menu-box {
            background-color: #0F172A;
            border-left: 5px solid #F97316;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s;
        }

        .menu-box:hover {
            background-color: #1E293B;
        }

        .menu-box a {
            color: #F3F4F6;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <h3 style="margin-bottom: 20px;">탐색 메뉴</h3>
        <div class="menu-box"><a href="#region_health">지역 별 건강 지표</a></div>
        <div class="menu-box"><a href="#accessibility">의료 접근성</a></div>
        <div class="menu-box"><a href="#socioeconomic">사회 경제 지표</a></div>
        <div class="menu-box"><a href="#inequality_index">건강 불평등 지수</a></div>
        <div class="menu-box"><a href="#regional_clustering">지역 클러스터링</a></div>
        <div class="menu-box"><a href="#policy_matrix">정책 우선순위</a></div>
        <div class="menu-box"><a href="#total_analysis">데이터 전체 분석</a></div>
        <div class="menu-box"><a href="#suggestion">제안</a></div>
    """, unsafe_allow_html=True)

# 인트로
st.markdown("<a name='intro'></a>", unsafe_allow_html=True)
try:
    st.image("images/intro_banner.png", use_container_width=True)
except:
    st.info("이미지를 불러올 수 없습니다. images/intro_banner.png 파일을 확인해주세요.")
st.markdown("<h1 style='color:#0F172A; font-size:40px;'>건강 불평등 조사 프로젝트</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #F97316; margin-top: 0.2rem; margin-bottom: 0.8rem;'>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7280; font-size:18px;'>Health Inequality Research Project</p>", unsafe_allow_html=True)
st.markdown("""
지역·경제적 격차에 따라 달라지는 건강 수준을 다양한 지표를 통해 분석합니다.  
본 프로젝트는 다음과 같은 세 가지 핵심 요소를 중심으로,  
대한민국의 **건강 불균형 현상**을 시각화합니다.

- **지역별 건강 지표**: 기대수명, 만성질환 유병률, 건강검진 수검률 등 지역 간 건강 수준을 비교합니다.  
- **의료 접근성**: 지역별 의료시설 분포, 병상 수, 의료인력 밀도 등을 바탕으로 의료 이용의 편의성을 분석합니다.  
- **사회·경제적 지표**: 소득 수준, 교육 수준, 고용률, 주거 환경 등 건강에 영향을 미치는 사회경제 요인을 고려합니다.
""", unsafe_allow_html=True)

# 📍 지역별 건강 지표 섹션
st.markdown("<a name='region_health'></a>", unsafe_allow_html=True)
st.markdown("## 지역별 건강 지표", unsafe_allow_html=True)

drinking_data = health_charts.load_data('data/health_region/drinking_2020_2024_kr.csv')
obesity_data = health_charts.load_data('data/health_region/obesity_2020_2024_kr.csv')
smoking_data = health_charts.load_data('data/health_region/smoking_2020_2024_kr.csv')
activity_data = health_charts.load_data('data/health_region/activity_2020_2024_kr.csv')

# 기존 차트 코드 수정:

st.subheader('음주율 (Drinking Rates)')
fig1 = health_charts.plot_bar_chart(drinking_data, 'Drinking Rates (2020-2024)', 0)
st.pyplot(fig1)
insights1 = health_charts.analyze_data(drinking_data, 'Drinking')
health_charts.display_analysis(insights1, 'Drinking Rates')

st.subheader('비만율 (Obesity Rates)')
fig2 = health_charts.plot_bar_chart(obesity_data, 'Obesity Rates (2020-2024)', 1)
st.pyplot(fig2)
insights2 = health_charts.analyze_data(obesity_data, 'Obesity')
health_charts.display_analysis(insights2, 'Obesity Rates')

st.subheader('흡연율 (Smoking Rates)')
fig3 = health_charts.plot_bar_chart(smoking_data, 'Smoking Rates (2020-2024)', 2)
st.pyplot(fig3)
insights3 = health_charts.analyze_data(smoking_data, 'Smoking')
health_charts.display_analysis(insights3, 'Smoking Rates')

st.subheader('신체활동 실천율 (Physical Activity Rates)')
fig4 = health_charts.plot_bar_chart(activity_data, 'Physical Activity Rates (2020-2024)', 3)
st.pyplot(fig4)
insights4 = health_charts.analyze_data(activity_data, 'Physical Activity')
health_charts.display_analysis(insights4, 'Physical Activity Rates')

# 신체활동 실천율 섹션 다음에 추가
st.markdown("---")  # 구분선
st.markdown("## 📈 상관관계 분석")

st.subheader('1. 신체활동 실천율 vs 흡연율 상관관계')
fig_corr1, corr1 = health_charts.plot_correlation_scatter(
    activity_data, smoking_data, 
    '신체활동 실천율과 흡연율의 상관관계',
    '신체활동 실천율 (%)',
    '흡연율 (%)'
)
st.pyplot(fig_corr1)
health_charts.display_correlation_analysis(corr1, '신체활동 실천율', '흡연율')

# 기존 신체활동 vs 흡연율 상관관계 다음에 추가

st.subheader('2. 음주율 vs 흡연율 상관관계')
fig_corr2, corr2 = health_charts.plot_correlation_scatter(
    drinking_data, smoking_data, 
    '음주율과 흡연율의 상관관계',
    '음주율 (%)',
    '흡연율 (%)'
)
st.pyplot(fig_corr2)
health_charts.display_correlation_analysis(corr2, '음주율', '흡연율')

st.subheader('3. 음주율 vs 비만율 상관관계')
fig_corr3, corr3 = health_charts.plot_correlation_scatter(
    drinking_data, obesity_data, 
    '음주율과 비만율의 상관관계',
    '음주율 (%)',
    '비만율 (%)'
)
st.pyplot(fig_corr3)
health_charts.display_correlation_analysis(corr3, '음주율', '비만율')

# 📍 의료 접근성 섹션
st.markdown("---")
st.markdown("<a name='accessibility'></a>", unsafe_allow_html=True)
st.markdown("## 🏥 의료 접근성", unsafe_allow_html=True)

import medical_access_charts

# 의료 데이터 로드
hospitals_data = medical_access_charts.load_medical_data('data/health_accessibility/hospitals_2020_2024.csv')
healthcenters_data = medical_access_charts.load_medical_data('data/health_accessibility/healthcenters_2020_2024.csv') 
doctors_data = medical_access_charts.load_medical_data('data/health_accessibility/doctors_2020_2024.csv')

# 종합 비교 차트
st.subheader('의료시설 종합 현황 (2020-2024 평균)')
fig_comparison = medical_access_charts.plot_medical_comparison(hospitals_data, healthcenters_data, doctors_data)
st.pyplot(fig_comparison)

# 개별 분석
st.subheader('병원 수')
fig_med1 = medical_access_charts.plot_medical_bar_chart(hospitals_data, '지역별 병원 수', 0)
st.pyplot(fig_med1)
insights_med1 = medical_access_charts.analyze_medical_data(hospitals_data, '병원')
medical_access_charts.display_medical_analysis(insights_med1, '병원')

st.subheader('보건소 수') 
fig_med2 = medical_access_charts.plot_medical_bar_chart(healthcenters_data, '지역별 보건소 수', 1)
st.pyplot(fig_med2)
insights_med2 = medical_access_charts.analyze_medical_data(healthcenters_data, '보건소')
medical_access_charts.display_medical_analysis(insights_med2, '보건소')

st.subheader('의사 수')
fig_med3 = medical_access_charts.plot_medical_bar_chart(doctors_data, '지역별 의사 수', 2, "명")
st.pyplot(fig_med3)
insights_med3 = medical_access_charts.analyze_medical_data(doctors_data, '의사')
medical_access_charts.display_medical_analysis(insights_med3, '의사')
# 의료 접근성 상관관계 (의사 수 분석 다음에 추가)
st.markdown("---")
st.subheader('🔗 병원 수 vs 의사 수 상관관계')
fig_med_corr, corr_med = medical_access_charts.plot_medical_correlation(hospitals_data, doctors_data)
st.pyplot(fig_med_corr)
medical_access_charts.display_medical_correlation_analysis(corr_med)

# 📍 사회경제 지표 섹션 (의료 접근성 섹션 다음에 추가)
st.markdown("---")
st.markdown("<a name='socioeconomic'></a>", unsafe_allow_html=True)
st.markdown("## 💰 사회경제 지표", unsafe_allow_html=True)

import socioeconomic_charts

# 사회경제 데이터 로드
income_data = socioeconomic_charts.load_socioeconomic_data('data/socioeconomic/소득_2020_2024.csv')
education_data = socioeconomic_charts.load_socioeconomic_data('data/socioeconomic/교육수준_2020_2024.csv')
higher_edu_data = socioeconomic_charts.load_socioeconomic_data('data/socioeconomic/고등교육이수율_2020_2024.csv')
employment_data = socioeconomic_charts.load_socioeconomic_data('data/socioeconomic/고용률_2020_2024.csv')
unemployment_data = socioeconomic_charts.load_socioeconomic_data('data/socioeconomic/실업률_2020_2024.csv')

# 종합 비교 차트
st.subheader('사회경제 지표 종합 현황 (2020-2024 평균)')
fig_socio_comparison = socioeconomic_charts.plot_socioeconomic_comparison(
    income_data, education_data, employment_data, unemployment_data, higher_edu_data
)
st.pyplot(fig_socio_comparison)

# 개별 분석
st.subheader('💰 소득 수준')
fig_socio1 = socioeconomic_charts.plot_socioeconomic_bar_chart(income_data, '지역별 소득 수준 (2020-2024 평균)', 0, "만원")
st.pyplot(fig_socio1)
insights_socio1 = socioeconomic_charts.analyze_socioeconomic_data(income_data, '소득')
socioeconomic_charts.display_socioeconomic_analysis(insights_socio1, '소득')

st.subheader('🎓 교육 수준')
fig_socio2 = socioeconomic_charts.plot_socioeconomic_bar_chart(education_data, '지역별 교육 수준 (2020-2024 평균)', 1, "%")
st.pyplot(fig_socio2)
insights_socio2 = socioeconomic_charts.analyze_socioeconomic_data(education_data, '교육수준')
socioeconomic_charts.display_socioeconomic_analysis(insights_socio2, '교육수준')

st.subheader('🏫 고등교육 이수율')
fig_socio3 = socioeconomic_charts.plot_socioeconomic_bar_chart(higher_edu_data, '지역별 고등교육 이수율 (2020-2024 평균)', 2, "%")
st.pyplot(fig_socio3)
insights_socio3 = socioeconomic_charts.analyze_socioeconomic_data(higher_edu_data, '고등교육이수율')
socioeconomic_charts.display_socioeconomic_analysis(insights_socio3, '고등교육이수율')

st.subheader('💼 고용률')
fig_socio4 = socioeconomic_charts.plot_socioeconomic_bar_chart(employment_data, '지역별 고용률 (2020-2024 평균)', 3, "%")
st.pyplot(fig_socio4)
insights_socio4 = socioeconomic_charts.analyze_socioeconomic_data(employment_data, '고용률')
socioeconomic_charts.display_socioeconomic_analysis(insights_socio4, '고용률')

st.subheader('📉 실업률')
fig_socio5 = socioeconomic_charts.plot_socioeconomic_bar_chart(unemployment_data, '지역별 실업률 (2020-2024 평균)', 4, "%")
st.pyplot(fig_socio5)
insights_socio5 = socioeconomic_charts.analyze_socioeconomic_data(unemployment_data, '실업률')
socioeconomic_charts.display_socioeconomic_analysis(insights_socio5, '실업률')

# 사회경제 지표 상관관계 분석
st.markdown("---")
st.markdown("## 📈 사회경제 지표 상관관계")

st.subheader('1. 소득 수준 vs 교육 수준 상관관계')
fig_socio_corr1, corr_socio1 = socioeconomic_charts.plot_socioeconomic_correlation(
    income_data, education_data,
    '소득 수준과 교육 수준의 상관관계',
    '소득 수준 (만원)',
    '교육 수준 (%)'
)
st.pyplot(fig_socio_corr1)
socioeconomic_charts.display_socioeconomic_correlation_analysis(corr_socio1, '소득', '교육수준')

st.subheader('2. 고용률 vs 실업률 상관관계')
fig_socio_corr2, corr_socio2 = socioeconomic_charts.plot_socioeconomic_correlation(
    employment_data, unemployment_data,
    '고용률과 실업률의 상관관계',
    '고용률 (%)',
    '실업률 (%)'
)
st.pyplot(fig_socio_corr2)
socioeconomic_charts.display_socioeconomic_correlation_analysis(corr_socio2, '고용률', '실업률')

st.subheader('3. 소득 수준 vs 고등교육 이수율 상관관계')
fig_socio_corr3, corr_socio3 = socioeconomic_charts.plot_socioeconomic_correlation(
    income_data, higher_edu_data,
    '소득 수준과 고등교육 이수율의 상관관계',
    '소득 수준 (만원)',
    '고등교육 이수율 (%)'
)
st.pyplot(fig_socio_corr3)
socioeconomic_charts.display_socioeconomic_correlation_analysis(corr_socio3, '소득', '고등교육이수율')

# 📍 건강 불평등 종합 지수 섹션
st.markdown("---")
st.markdown("<a name='inequality_index'></a>", unsafe_allow_html=True)
st.markdown("## 📈 건강 불평등 종합 지수", unsafe_allow_html=True)

inequality_index.create_inequality_dashboard()

# 📍 지역 클러스터링 분석 섹션  
st.markdown("---")
st.markdown("<a name='regional_clustering'></a>", unsafe_allow_html=True)
st.markdown("## 🗺️ 지역 클러스터링 분석", unsafe_allow_html=True)

regional_clustering.create_clustering_dashboard()

# 📍 정책 우선순위 매트릭스 섹션
st.markdown("---")
st.markdown("<a name='policy_matrix'></a>", unsafe_allow_html=True)
st.markdown("## 📊 정책 우선순위 매트릭스", unsafe_allow_html=True)

policy_matrix.create_policy_dashboard()

# 📍 데이터 전체 분석 (기존 코드 유지)
st.markdown("---")
st.markdown("<a name='total_analysis'></a>", unsafe_allow_html=True)
st.markdown("## 🔍 데이터 전체 분석", unsafe_allow_html=True)

st.markdown("### 주요 발견 사항")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    **🎯 건강 지표 분석 결과**
    • 지역 간 건강 행동 격차가 상당함
    • 신체활동 실천율과 흡연율 간 음의 상관관계 확인
    • 음주와 흡연 간 양의 상관관계 발견
    """)

with col2:
    st.info("""
    **🏥 의료 접근성 분석 결과**
    • 수도권과 지방 간 의료 인프라 격차 심각
    • 병원 수와 의사 수 간 강한 양의 상관관계
    • 농어촌 지역의 의료 접근성 개선 필요
    """)

st.warning("""
**💰 사회경제적 요인의 영향**
• 소득과 교육 수준이 건강 격차에 미치는 영향이 큼
• 고용률과 실업률이 건강 행동과 연관성 있음
• 지역균형발전을 통한 종합적 접근 필요
""")

# 📍 제안 섹션
st.markdown("---")
st.markdown("<a name='suggestion'></a>", unsafe_allow_html=True)
st.markdown("## 💡 정책 제안", unsafe_allow_html=True)

st.markdown("### 단기 개선 방안 (1-2년)")
col3, col4, col5 = st.columns(3)

with col3:
    st.info("""
    **🏥 의료 접근성 개선**
    • 농어촌 지역 이동진료소 확대
    • 원격의료 서비스 도입
    • 응급의료 시스템 강화
    """)

with col4:
    st.success("""
    **🎯 건강증진 프로그램**
    • 지역별 맞춤형 건강교육
    • 금연·금주 지원 프로그램 확대
    • 체육시설 및 운동 프로그램 확충
    """)

with col5:
    st.warning("""
    **💰 경제적 지원**
    • 저소득층 의료비 지원 확대
    • 건강검진 접근성 향상
    • 예방의료 서비스 강화
    """)

st.markdown("### 중장기 개선 방안 (3-5년)")
st.error("""
**🎯 종합적 접근 전략**
• **지역균형발전**: 수도권 집중 완화를 통한 전국적 의료 인프라 균등화
• **교육 격차 해소**: 건강 리터러시 향상을 위한 교육 프로그램 확대
• **사회안전망 강화**: 건강보험 보장성 확대 및 취약계층 지원 강화
• **데이터 기반 정책**: 지속적인 모니터링을 통한 증거 기반 정책 수립
""")

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #F3F4F6; border-radius: 10px;">
    <h3 style="color: #374151;">건강 불평등 해소를 위한 지속적인 노력이 필요합니다</h3>
    <p style="color: #6B7280;">모든 국민이 동등한 건강권을 누릴 수 있는 사회를 만들어갑시다</p>
</div>
""", unsafe_allow_html=True)