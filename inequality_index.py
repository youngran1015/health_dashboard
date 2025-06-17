import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_all_data():
    """모든 데이터를 로드하는 함수"""
    try:
        # 건강 지표 데이터 (첫 번째 컬럼을 인덱스로 설정)
        drinking_data = pd.read_csv('data/health_region/drinking_2020_2024_kr.csv', index_col=0)
        obesity_data = pd.read_csv('data/health_region/obesity_2020_2024_kr.csv', index_col=0)
        smoking_data = pd.read_csv('data/health_region/smoking_2020_2024_kr.csv', index_col=0)
        activity_data = pd.read_csv('data/health_region/activity_2020_2024_kr.csv', index_col=0)
        
        # 의료 접근성 데이터 (지역을 인덱스로 설정)
        hospitals_data = pd.read_csv('data/health_accessibility/hospitals_2020_2024.csv', index_col='지역')
        doctors_data = pd.read_csv('data/health_accessibility/doctors_2020_2024.csv', index_col='지역')
        healthcenters_data = pd.read_csv('data/health_accessibility/healthcenters_2020_2024.csv', index_col='지역')
        
        # 사회경제 데이터 (년도를 인덱스로 설정)
        income_data = pd.read_csv('data/socioeconomic/소득_2020_2024.csv', index_col='년도')
        education_data = pd.read_csv('data/socioeconomic/교육수준_2020_2024.csv', index_col='년도')
        employment_data = pd.read_csv('data/socioeconomic/고용률_2020_2024.csv', index_col='년도')
        
        return {
            'health': {'drinking': drinking_data, 'obesity': obesity_data, 'smoking': smoking_data, 'activity': activity_data},
            'medical': {'hospitals': hospitals_data, 'doctors': doctors_data, 'healthcenters': healthcenters_data},
            'socioeconomic': {'income': income_data, 'education': education_data, 'employment': employment_data}
        }
    except Exception as e:
        st.error(f"데이터 로딩 오류: {str(e)}")
        return None

def calculate_inequality_index(all_data):
    """건강 불평등 종합 지수 계산 (서울=100 기준)"""
    
    # 실제 지역 리스트 (데이터에서 확인된 17개 지역)
    regions = ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종', 
               '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주']
    
    try:
        # 2024년 기준 평균값 계산
        health_avg = all_data['health']['activity'].mean(axis=0)  # 신체활동 실천율 (컬럼별 평균)
        medical_avg_hospitals = all_data['medical']['hospitals']['2024']  # 2024년 병원 수
        medical_avg_doctors = all_data['medical']['doctors']['2024']  # 2024년 의사 수
        socio_income = all_data['socioeconomic']['income'].loc[2024]  # 2024년 소득
        socio_education = all_data['socioeconomic']['education'].loc[2024]  # 2024년 교육수준
        socio_employment = all_data['socioeconomic']['employment'].loc[2024]  # 2024년 고용률
        
        # 정규화 (서울=100 기준)
        def normalize_to_seoul(data):
            seoul_value = data['서울']
            return (data / seoul_value * 100).round(1)
        
        # 각 지표별 정규화
        health_norm = normalize_to_seoul(health_avg)
        medical_hospitals_norm = normalize_to_seoul(medical_avg_hospitals)
        medical_doctors_norm = normalize_to_seoul(medical_avg_doctors)
        socio_income_norm = normalize_to_seoul(socio_income)
        socio_education_norm = normalize_to_seoul(socio_education)
        socio_employment_norm = normalize_to_seoul(socio_employment)
        
        # 가중평균으로 종합 지수 계산
        # 건강행동(15%) + 의료접근성(35%) + 사회경제(50%)
        inequality_index = (
            health_norm * 0.15 +
            (medical_hospitals_norm * 0.15 + medical_doctors_norm * 0.20) +
            (socio_income_norm * 0.25 + socio_education_norm * 0.15 + socio_employment_norm * 0.10)
        ).round(1)
        
        # 데이터프레임 생성
        result_df = pd.DataFrame({
            '지역': regions,
            '건강행동지수': [health_norm[region] for region in regions],
            '병원접근성': [medical_hospitals_norm[region] for region in regions],
            '의료인력': [medical_doctors_norm[region] for region in regions],
            '소득수준': [socio_income_norm[region] for region in regions],
            '교육수준': [socio_education_norm[region] for region in regions],
            '고용수준': [socio_employment_norm[region] for region in regions],
            '종합불평등지수': [inequality_index[region] for region in regions]
        })
        
        result_df = result_df.sort_values('종합불평등지수', ascending=False).reset_index(drop=True)
        result_df.index = result_df.index + 1
        
        return result_df
        
    except Exception as e:
        st.error(f"지수 계산 오류: {str(e)}")
        return None

def plot_inequality_radar(inequality_data):
    """불평등 지수 레이더 차트"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    # 상위 4개 지역
    top_regions = inequality_data.head(4)
    
    categories = ['건강행동지수', '병원접근성', '의료인력', '소득수준', '교육수준', '고용수준']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    for idx, (_, row) in enumerate(top_regions.iterrows()):
        ax = axes[idx]
        
        values = [row[cat] for cat in categories]
        values += values[:1]  # 첫 번째 값을 마지막에 추가해서 차트를 닫음
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, color=colors[idx])
        ax.fill(angles, values, alpha=0.25, color=colors[idx])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 200)
        ax.set_title(f"{row['지역']} (종합지수: {row['종합불평등지수']})", 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True)
    
    plt.tight_layout()
    return fig

def plot_inequality_ranking(inequality_data):
    """불평등 지수 순위 막대 그래프"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 색상 구분 (상위권, 중위권, 하위권)
    colors = []
    for idx, score in enumerate(inequality_data['종합불평등지수']):
        if idx < 5:  # 상위 5위
            colors.append('#2E8B57')  # 짙은 녹색
        elif idx < 12:  # 중위권
            colors.append('#FFD700')  # 금색
        else:  # 하위권
            colors.append('#DC143C')  # 빨간색
    
    bars = ax.barh(range(len(inequality_data)), inequality_data['종합불평등지수'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # 지역명 설정
    ax.set_yticks(range(len(inequality_data)))
    ax.set_yticklabels(inequality_data['지역'])
    ax.invert_yaxis()
    
    # 제목과 라벨
    ax.set_xlabel('종합 불평등 지수 (서울=100 기준)', fontsize=12, fontweight='bold')
    ax.set_title('지역별 건강 불평등 종합 지수 순위', fontsize=16, fontweight='bold', pad=20)
    
    # 점수 표시
    for i, (bar, score) in enumerate(zip(bars, inequality_data['종합불평등지수'])):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                f'{score}', ha='left', va='center', fontweight='bold')
    
    # 기준선 (서울=100)
    ax.axvline(x=100, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax.text(102, len(inequality_data)/2, '서울 기준선\n(100점)', 
            fontsize=10, color='red', fontweight='bold')
    
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return fig

def display_inequality_analysis(inequality_data):
    """불평등 지수 분석 결과 표시"""
    
    st.markdown("### 📊 건강 불평등 종합 지수 분석")
    
    # 주요 통계
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("최고 지역", 
                 inequality_data.iloc[0]['지역'],
                 f"{inequality_data.iloc[0]['종합불평등지수']}점")
    
    with col2:
        st.metric("최저 지역", 
                 inequality_data.iloc[-1]['지역'],
                 f"{inequality_data.iloc[-1]['종합불평등지수']}점")
    
    with col3:
        gap = inequality_data.iloc[0]['종합불평등지수'] - inequality_data.iloc[-1]['종합불평등지수']
        st.metric("격차", f"{gap:.1f}점", "심각한 수준")
    
    with col4:
        avg_score = inequality_data['종합불평등지수'].mean()
        st.metric("전국 평균", f"{avg_score:.1f}점", "서울 대비")
    
    # 순위 테이블
    st.markdown("#### 📋 지역별 종합 순위")
    st.dataframe(inequality_data, use_container_width=True)
    
    # 레이더 차트
    st.markdown("#### 🎯 상위 4개 지역 세부 분석")
    fig_radar = plot_inequality_radar(inequality_data)
    st.pyplot(fig_radar)
    
    # 순위 막대 그래프
    st.markdown("#### 🏆 전체 지역 순위")
    fig_ranking = plot_inequality_ranking(inequality_data)
    st.pyplot(fig_ranking)
    
    # 인사이트
    st.markdown("---")
    st.markdown("### 💡 주요 인사이트")
    
    top_region = inequality_data.iloc[0]['지역']
    bottom_region = inequality_data.iloc[-1]['지역']
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.success(f"""
        **🥇 {top_region} (1위)**
        • 모든 영역에서 우수한 성과
        • 특히 의료 인프라와 사회경제 지표 우세
        • 건강 불평등 해소의 모범 사례
        """)
    
    with col6:
        st.error(f"""
        **⚠️ {bottom_region} (최하위)**
        • 전 영역에서 개선 필요
        • 의료 접근성 확충 시급
        • 사회경제적 지원 정책 필요
        """)

def create_inequality_dashboard():
    """불평등 지수 대시보드 메인 함수"""
    st.header("📈 건강 불평등 종합 지수")
    st.markdown("**모든 건강 지표를 종합한 불평등 정도를 서울=100 기준으로 분석합니다.**")
    
    # 데이터 로드
    with st.spinner("데이터를 분석하고 있습니다..."):
        all_data = load_all_data()
        
        if all_data is None:
            st.error("데이터를 불러올 수 없습니다.")
            return
        
        # 불평등 지수 계산
        inequality_data = calculate_inequality_index(all_data)
        
        if inequality_data is None:
            st.error("불평등 지수를 계산할 수 없습니다.")
            return
        
        # 분석 결과 표시
        display_inequality_analysis(inequality_data)
        
        # 다운로드 버튼
        csv = inequality_data.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 분석 결과 다운로드 (CSV)",
            data=csv,
            file_name="건강불평등종합지수.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    create_inequality_dashboard()