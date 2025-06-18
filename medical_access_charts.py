import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'  # Windows
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.max_open_warning'] = 0  # 경고 비활성화
plt.rcParams['agg.path.chunksize'] = 10000  # 메모리 최적화

# 의료 접근성 색상 팔레트 (차분한 블루 계열)
medical_colors = ['#3B82F6', '#60A5FA', '#93C5FD', '#DBEAFE', '#1E40AF', 
                 '#2563EB', '#6366F1', '#8B5CF6', '#A78BFA', '#C4B5FD']

def load_medical_data(file_name):
    """의료 접근성 CSV 파일을 로드하고 평균 계산하는 함수"""
    df = pd.read_csv(file_name)
    df = df.set_index(df.columns[0])  # 첫 번째 열을 인덱스로 설정
    
    # 2020-2024 평균 계산
    df['5년평균'] = df[['2020', '2021', '2022', '2023', '2024']].mean(axis=1).round(1)
    
    return df

def analyze_medical_data(data, title):
    """의료 접근성 데이터 분석 함수 - 5년 평균 기준"""
    # 5년 평균 데이터 기준으로 분석
    avg_data = data['5년평균']
    highest = avg_data.idxmax()
    lowest = avg_data.idxmin()
    highest_val = avg_data.max()
    lowest_val = avg_data.min()
    diff = highest_val - lowest_val
    
    # 연도별 전체 평균 트렌드 계산
    yearly_totals = data[['2020', '2021', '2022', '2023', '2024']].sum()
    trend_change = yearly_totals['2024'] - yearly_totals['2020']
    trend_pct = (trend_change / yearly_totals['2020']) * 100
    
    insights = {
        'highest': (highest, highest_val),
        'lowest': (lowest, lowest_val),
        'difference': diff,
        'average': avg_data.mean(),
        'trend_change': trend_change,
        'trend_pct': trend_pct,
        'std_dev': avg_data.std()  # 표준편차로 지역 간 격차 측정
    }
    
    return insights

def plot_medical_bar_chart(data, title, color_idx, unit="개"):
    """의료 접근성 막대 그래프 - 5년 평균 기준"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 5년 평균 데이터 사용
    avg_data = data['5년평균']
    
    # 막대 그래프 그리기
    bars = ax.bar(avg_data.index, avg_data.values, 
                  color=medical_colors[color_idx % len(medical_colors)], 
                  edgecolor='navy', linewidth=0.8, alpha=0.8)
    
    # 제목과 라벨 설정
    ax.set_title(f'{title} (2020-2024 평균)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('지역 (Region)', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'평균 개수 ({unit})', fontsize=12, fontweight='bold')
    
    # x축 라벨 회전
    plt.xticks(rotation=45, ha='right')
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    return fig

def plot_medical_trend_chart(data, title, color_idx):
    """의료 접근성 연도별 변화 추이"""
    fig, ax = plt.subplots(figsize=(10, 5), dpi=80)  # 크기와 DPI 축소
    
    # 전국 평균 추이 (전체 합계 기준)
    years = ['2020', '2021', '2022', '2023', '2024']
    yearly_totals = [data[year].sum() for year in years]
    
    # 선 그래프 - 전국 총합
    ax.plot(years, yearly_totals, 
            color=medical_colors[color_idx], linewidth=4, 
            marker='o', markersize=10, label='전국 총합', alpha=0.9)
    
    # 상위 3개 지역 (5년 평균 기준)
    top3_regions = data['5년평균'].nlargest(3).index
    for i, region in enumerate(top3_regions):
        region_data = [data.loc[region, year] for year in years]
        ax.plot(years, region_data, 
                linestyle='--', alpha=0.8, linewidth=2,
                marker='s', markersize=6, label=f'{region} (상위 {i+1}위)')
    
    # 하위 1개 지역
    bottom_region = data['5년평균'].nsmallest(1).index[0]
    bottom_data = [data.loc[bottom_region, year] for year in years]
    ax.plot(years, bottom_data, 
            linestyle=':', alpha=0.8, linewidth=2, color='red',
            marker='^', markersize=6, label=f'{bottom_region} (최하위)')
    
    ax.set_title(f'{title} - 연도별 변화 추이', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('연도 (Year)', fontsize=12, fontweight='bold')
    ax.set_ylabel('개수', fontsize=12, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 추세 화살표 추가
    trend_change = yearly_totals[-1] - yearly_totals[0]
    if trend_change > 0:
        ax.annotate('', xy=(4.5, yearly_totals[-1]), xytext=(4.2, yearly_totals[-1] - abs(trend_change)*0.1),
                   arrowprops=dict(arrowstyle='->', color='green', lw=2))
        ax.text(4.6, yearly_totals[-1], f'+{trend_change:.0f}', fontsize=12, color='green', fontweight='bold')
    else:
        ax.annotate('', xy=(4.5, yearly_totals[-1]), xytext=(4.2, yearly_totals[-1] + abs(trend_change)*0.1),
                   arrowprops=dict(arrowstyle='->', color='red', lw=2))
        ax.text(4.6, yearly_totals[-1], f'{trend_change:.0f}', fontsize=12, color='red', fontweight='bold')
    
    plt.tight_layout()
    return fig

def display_medical_analysis(insights, chart_type):
    """의료 접근성 분석 결과를 Streamlit 컴포넌트로 표시 - 5년 평균 기준"""
    
    # 차트 타입별 아이콘
    icons = {
        "병원": "🏥",
        "보건소": "🏢", 
        "의사": "👩‍⚕️"
    }
    
    icon = icons.get(chart_type, "📊")
    unit = "개" if chart_type != "의사" else "명"
    
    # 메인 지표들
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label=f"📍 최다 지역 (5년 평균)",
            value=f"{insights['highest'][0]}",
            delta=f"{insights['highest'][1]:.1f}{unit}"
        )
    
    with col2:
        st.metric(
            label=f"📍 최소 지역 (5년 평균)",
            value=f"{insights['lowest'][0]}",
            delta=f"{insights['lowest'][1]:.1f}{unit}"
        )
    
    with col3:
        trend_symbol = "↗️" if insights['trend_change'] > 0 else "↘️" if insights['trend_change'] < 0 else "➡️"
        st.metric(
            label=f"5년간 전국 변화",
            value=f"{insights['trend_change']:+.0f}{unit}",
            delta=f"{insights['trend_pct']:+.1f}%"
        )
    
    # 상세 분석
    st.markdown("---")
    
    col4, col5 = st.columns(2)
    
    with col4:
        # 지역 간 격차 분석
        disparity_level = "높음" if insights['std_dev'] > insights['average'] * 0.5 else "중간" if insights['std_dev'] > insights['average'] * 0.3 else "낮음"
        disparity_color = "error" if disparity_level == "높음" else "warning" if disparity_level == "중간" else "success"
        
        getattr(st, disparity_color)(f"""
        **⚡ 지역 간 격차: {insights['difference']:.1f}{unit}**  
        **격차 수준: {disparity_level}**  
        표준편차: {insights['std_dev']:.1f}{unit}
        """)
    
    with col5:
        # 전국 평균 정보
        st.info(f"""
        **📊 전국 평균 (5년간)**  
        **{insights['average']:.1f}{unit}**  
        지역별 편차를 고려한 균형적 접근이 필요합니다.
        """)
    
    # 차트 타입별 특화 인사이트
    st.markdown("### 💡 주요 인사이트")
    
    if "병원" in chart_type:
        if insights['trend_pct'] > 0:
            st.success(f"""
            **🏥 병원 인프라 확충 중**  
            • 5년간 {insights['trend_pct']:.1f}% 증가 추세
            • 수도권 집중 현상 지속
            • 지방 의료 접근성 개선 필요
            """)
        else:
            st.warning(f"""
            **🏥 병원 수 감소 우려**  
            • 5년간 {insights['trend_pct']:.1f}% 감소
            • 의료 접근성 악화 가능성
            • 정책적 개입 필요
            """)
    
    elif "보건소" in chart_type:
        st.success(f"""
        **🏢 공공 의료 기반 시설**  
        • 상대적으로 균등한 분포
        • 기본 의료서비스 접근성 보장
        • 지역사회 건강 관리 중추 역할
        """)
    
    elif "의사" in chart_type:
        if insights['std_dev'] > insights['average'] * 0.7:
            st.error(f"""
            **🚨 의료인력 수도권 집중 심각**  
            • 지역 간 의사 수 격차 매우 큼
            • 의료 서비스 질 격차 우려
            • 지방 의료진 확보 시급
            """)
        else:
            st.warning(f"""
            **👩‍⚕️ 의료인력 분포 개선 필요**  
            • 지역 간 격차 존재
            • 균형적 의료인력 배치 필요
            """)

def plot_medical_comparison(hospitals_data, healthcenters_data, doctors_data):
    """의료 시설 종합 비교 차트 - 5년 평균 기준"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    
    # 5년 평균 데이터
    hospitals_avg = hospitals_data['5년평균']
    healthcenters_avg = healthcenters_data['5년평균'] 
    doctors_avg = doctors_data['5년평균']
    
    # 각 서브플롯 그리기
    datasets = [hospitals_avg, healthcenters_avg, doctors_avg]
    titles = ['병원 수 (5년 평균)', '보건소 수 (5년 평균)', '의사 수 (5년 평균)']
    colors = ['#3B82F6', '#60A5FA', '#93C5FD']
    
    for i, (data, title, color) in enumerate(zip(datasets, titles, colors)):
        axes[i].bar(data.index, data.values, color=color, alpha=0.8, edgecolor='navy')
        axes[i].set_title(title, fontsize=12, fontweight='bold')
        axes[i].tick_params(axis='x', rotation=45, labelsize=8)
        axes[i].tick_params(axis='y', labelsize=8)
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_medical_correlation(hospitals_data, doctors_data):
    """병원 수와 의사 수 간의 상관관계 분석 - 5년 평균 기준"""
    fig, ax = plt.subplots(figsize=(8, 5), dpi=80)  # 크기 축소
    
    # 5년 평균 데이터 사용
    hospitals_avg = hospitals_data['5년평균']
    doctors_avg = doctors_data['5년평균']
    
    # 산점도 그리기
    scatter = ax.scatter(hospitals_avg.values, doctors_avg.values, 
                        c='#3B82F6', s=150, alpha=0.7, edgecolors='navy', linewidth=2)
    
    # 지역명 라벨 추가
    for i, region in enumerate(hospitals_avg.index):
        ax.annotate(region, (hospitals_avg.iloc[i], doctors_avg.iloc[i]), 
                   xytext=(8, 8), textcoords='offset points', 
                   fontsize=11, ha='left', va='bottom', fontweight='bold')
    
    # 회귀선 추가
    import numpy as np
    z = np.polyfit(hospitals_avg.values, doctors_avg.values, 1)
    p = np.poly1d(z)
    ax.plot(hospitals_avg.values, p(hospitals_avg.values), "r--", alpha=0.8, linewidth=3)
    
    # 상관계수 계산
    correlation = np.corrcoef(hospitals_avg.values, doctors_avg.values)[0, 1]
    
    # 제목과 라벨 설정
    ax.set_title(f'병원 수와 의사 수의 상관관계 (2020-2024 평균)\n상관계수: {correlation:.3f}', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('병원 수 (5년 평균)', fontsize=14, fontweight='bold')
    ax.set_ylabel('의사 수 (5년 평균)', fontsize=14, fontweight='bold')
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 통계 정보 텍스트 박스 (scipy 없이)
    textstr = f'상관계수: {correlation:.3f}\nR² 값: {correlation**2:.3f}'
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    return fig, correlation

def display_medical_correlation_analysis(correlation):
    """병원-의사 상관관계 분석 결과 표시 - 5년 평균 기준"""
    
    # 상관관계 강도 판단
    if abs(correlation) >= 0.7:
        strength = "매우 강한"
        strength_emoji = "🔥"
        strength_color = "success"
    elif abs(correlation) >= 0.5:
        strength = "강한"
        strength_emoji = "⚡"
        strength_color = "info"
    elif abs(correlation) >= 0.3:
        strength = "중간" 
        strength_emoji = "💫"
        strength_color = "warning"
    else:
        strength = "약한"
        strength_emoji = "💨"
        strength_color = "error"
    
    direction = "양의" if correlation > 0 else "음의"
    
    # 메인 지표
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="상관계수 (5년 평균)",
            value=f"{correlation:.3f}",
            delta=f"{strength} {direction} 상관관계"
        )
    
    with col2:
        st.metric(
            label="결정계수 (R²)",
            value=f"{correlation**2:.3f}",
            delta=f"설명력 {correlation**2*100:.1f}%"
        )
    
    with col3:
        getattr(st, strength_color)(f"""
        **{strength_emoji} 관계 강도**  
        {strength} {direction} 상관관계
        """)
    
    # 상세 해석
    st.markdown("---")
    st.markdown("### 📈 상관관계 해석")
    
    if abs(correlation) >= 0.7:
        st.success(f"""
        **✅ {strength} {direction} 상관관계 확인!**  
        • 병원 수와 의사 수가 매우 밀접한 관계
        • 의료 인프라가 함께 집중되는 패턴
        • 정책적으로 통합 접근이 효과적
        """)
    elif abs(correlation) >= 0.5:
        st.info(f"""
        **⚡ {strength} {direction} 상관관계**  
        • 병원과 의사 수가 상당히 연관성 있음
        • 일부 지역에서 다른 패턴 존재
        • 지역별 특성 고려 필요
        """)
    elif abs(correlation) >= 0.3:
        st.warning(f"""
        **💫 {strength} {direction} 상관관계**  
        • 병원과 의사 수가 어느 정도 연관
        • 지역별 편차가 상당함
        • 개별 지역 특성 분석 필요
        """)
    else:
        st.error(f"""
        **💨 {strength} 상관관계**  
        • 병원 수와 의사 수가 독립적
        • 예상과 다른 패턴
        • 질적 분석 필요
        """)
    
    # 정책적 시사점
    st.markdown("---")
    st.markdown("### 💡 정책적 시사점")
    
    col4, col5 = st.columns(2)
    
    with col4:
        if abs(correlation) >= 0.5:
            st.info(f"""
            **🎯 통합적 접근**  
            • 병원과 의료진을 함께 고려한 정책 설계
            • 의료 인프라 집중 지역 효율성 극대화
            • 통합 의료 허브 구축 전략 유효
            """)
        else:
            st.warning(f"""
            **🎯 개별적 접근**  
            • 병원과 의료진을 분리하여 정책 설계
            • 지역별 맞춤형 의료 인프라 구축
            • 질적 개선에 더 집중 필요
            """)
    
    with col5:
        st.success(f"""
        **📋 향후 과제**  
        • 의료 접근성의 양적·질적 균형
        • 지역 간 의료 격차 해소
        • 효율적 의료 자원 배분 시스템 구축
        """)

def create_medical_dashboard():
    """의료 접근성 종합 대시보드"""
    st.title("🏥 의료 접근성 종합 분석 대시보드")
    st.markdown("**2020-2024년 5개년 평균 데이터 기반 분석**")
    
    # 사이드바 메뉴
    st.sidebar.title("📊 분석 메뉴")
    analysis_type = st.sidebar.selectbox(
        "분석 유형 선택",
        ["전체 개요", "병원 분석", "보건소 분석", "의사 분석", "상관관계 분석", "종합 비교"]
    )
    
    # 데이터 로드
    try:
        hospitals_data = load_medical_data('hospitals_2020_2024.csv')
        healthcenters_data = load_medical_data('healthcenters_2020_2024.csv')
        doctors_data = load_medical_data('doctors_2020_2024.csv')
        
        if analysis_type == "전체 개요":
            st.header("📋 의료 접근성 전체 개요")
            
            # 주요 지표 요약
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("전국 병원 수 (평균)", f"{hospitals_data['5년평균'].sum():.0f}개")
                st.metric("지역 간 병원 격차", f"{hospitals_data['5년평균'].max() - hospitals_data['5년평균'].min():.1f}개")
            
            with col2:
                st.metric("전국 보건소 수 (평균)", f"{healthcenters_data['5년평균'].sum():.0f}개")
                st.metric("지역 간 보건소 격차", f"{healthcenters_data['5년평균'].max() - healthcenters_data['5년평균'].min():.1f}개")
            
            with col3:
                st.metric("전국 의사 수 (평균)", f"{doctors_data['5년평균'].sum():.0f}명")
                st.metric("지역 간 의사 격차", f"{doctors_data['5년평균'].max() - doctors_data['5년평균'].min():.1f}명")
            
            # 종합 비교 차트
            st.subheader("🔍 지역별 의료 인프라 종합 비교")
            fig_comparison = plot_medical_comparison(hospitals_data, healthcenters_data, doctors_data)
            st.pyplot(fig_comparison)
            
        elif analysis_type == "병원 분석":
            st.header("🏥 병원 접근성 분석")
            insights = analyze_medical_data(hospitals_data, "병원")
            display_medical_analysis(insights, "병원")
            
            fig_bar = plot_medical_bar_chart(hospitals_data, "지역별 병원 수", 0)
            st.pyplot(fig_bar)
            
            fig_trend = plot_medical_trend_chart(hospitals_data, "병원 수", 0)
            st.pyplot(fig_trend)
            
        elif analysis_type == "보건소 분석":
            st.header("🏢 보건소 접근성 분석")
            insights = analyze_medical_data(healthcenters_data, "보건소")
            display_medical_analysis(insights, "보건소")
            
            fig_bar = plot_medical_bar_chart(healthcenters_data, "지역별 보건소 수", 1)
            st.pyplot(fig_bar)
            
            fig_trend = plot_medical_trend_chart(healthcenters_data, "보건소 수", 1)
            st.pyplot(fig_trend)
            
        elif analysis_type == "의사 분석":
            st.header("👩‍⚕️ 의료진 접근성 분석")
            insights = analyze_medical_data(doctors_data, "의사")
            display_medical_analysis(insights, "의사")
            
            fig_bar = plot_medical_bar_chart(doctors_data, "지역별 의사 수", 2, "명")
            st.pyplot(fig_bar)
            
            fig_trend = plot_medical_trend_chart(doctors_data, "의사 수", 2)
            st.pyplot(fig_trend)
            
        elif analysis_type == "상관관계 분석":
            st.header("📈 병원-의사 상관관계 분석")
            fig_corr, correlation = plot_medical_correlation(hospitals_data, doctors_data)
            st.pyplot(fig_corr)
            display_medical_correlation_analysis(correlation)
            
        elif analysis_type == "종합 비교":
            st.header("🔍 의료 인프라 종합 비교")
            
            # 종합 비교 차트
            fig_comparison = plot_medical_comparison(hospitals_data, healthcenters_data, doctors_data)
            st.pyplot(fig_comparison)
            
            # 지역별 순위 테이블
            st.subheader("📊 지역별 의료 인프라 순위 (5년 평균)")
            
            ranking_df = pd.DataFrame({
                '지역': hospitals_data.index,
                '병원 수': hospitals_data['5년평균'].round(1),
                '보건소 수': healthcenters_data['5년평균'].round(1),
                '의사 수': doctors_data['5년평균'].round(1)
            })
            
            # 종합 점수 계산 (표준화 후 합산)
            for col in ['병원 수', '보건소 수', '의사 수']:
                ranking_df[f'{col}_표준화'] = (ranking_df[col] - ranking_df[col].min()) / (ranking_df[col].max() - ranking_df[col].min())
            
            ranking_df['종합점수'] = (ranking_df['병원 수_표준화'] + ranking_df['보건소 수_표준화'] + ranking_df['의사 수_표준화']).round(2)
            ranking_df = ranking_df.drop(columns=[col for col in ranking_df.columns if '_표준화' in col])
            ranking_df = ranking_df.sort_values('종합점수', ascending=False).reset_index(drop=True)
            ranking_df.index = ranking_df.index + 1
            
            st.dataframe(ranking_df, use_container_width=True)
            
            # 상위/하위 지역 하이라이트
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"""
                **🥇 의료 인프라 상위 3개 지역**
                1. {ranking_df.iloc[0]['지역']} (점수: {ranking_df.iloc[0]['종합점수']})
                2. {ranking_df.iloc[1]['지역']} (점수: {ranking_df.iloc[1]['종합점수']})
                3. {ranking_df.iloc[2]['지역']} (점수: {ranking_df.iloc[2]['종합점수']})
                """)
            
            with col2:
                st.error(f"""
                **⚠️ 의료 인프라 하위 3개 지역**
                1. {ranking_df.iloc[-1]['지역']} (점수: {ranking_df.iloc[-1]['종합점수']})
                2. {ranking_df.iloc[-2]['지역']} (점수: {ranking_df.iloc[-2]['종합점수']})
                3. {ranking_df.iloc[-3]['지역']} (점수: {ranking_df.iloc[-3]['종합점수']})
                """)
    
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. CSV 파일들이 올바른 위치에 있는지 확인해주세요.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

# 메인 실행
if __name__ == "__main__":
    create_medical_dashboard()