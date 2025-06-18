import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# 사회경제 지표 색상 팔레트 (차분한 주황 계열)
socioeconomic_colors = ['#D97757', '#E09274', '#E6AD91', '#ECC8AE', '#F3E3CB']

def load_socioeconomic_data(file_name):
    """사회경제 지표 CSV 파일을 로드하는 함수"""
    df = pd.read_csv(file_name)
    # 년도를 인덱스로 설정 (전치하지 않음)
    df = df.set_index('년도')
    return df

def analyze_socioeconomic_data(data, title):
    """사회경제 지표 데이터 분석 함수 - 2020-2024 평균 사용"""
    # 2020-2024년 평균값으로 분석
    mean_data = data.mean(axis=0)  # 년도별 평균
    highest = mean_data.idxmax()
    lowest = mean_data.idxmin()
    highest_val = mean_data.max()
    lowest_val = mean_data.min()
    diff = highest_val - lowest_val
    
    insights = {
        'highest': (highest, highest_val),
        'lowest': (lowest, lowest_val),
        'difference': diff,
        'average': mean_data.mean(),
        'trend': data.loc[2024].mean() - data.loc[2020].mean()  # 5년간 변화
    }
    
    return insights

def plot_socioeconomic_bar_chart(data, title, color_idx, unit="%"):
    """사회경제 지표 막대 그래프 - 2020-2024 평균값 사용"""
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # 2020-2024년 평균값 사용
    mean_data = data.mean(axis=0)  # 년도별 평균
    
    # 막대 그래프 그리기
    bars = ax.bar(mean_data.index, mean_data.values, 
                  color=socioeconomic_colors[color_idx % len(socioeconomic_colors)], 
                  edgecolor='#8B4513', linewidth=0.8, alpha=0.8)
    
    # 제목과 라벨 설정
    ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel('지역 (Region)', fontsize=10, fontweight='bold')
    ax.set_ylabel(f'수치 ({unit})', fontsize=10, fontweight='bold')
    
    # Y축 범위 조정 - 차이를 극명하게 보이도록
    min_val = mean_data.min()
    max_val = mean_data.max()
    range_val = max_val - min_val
    
    # 여백을 5%로 줄여서 차이를 더 명확하게
    margin = range_val * 0.05
    ax.set_ylim(min_val - margin, max_val + margin)
    
    # x축 라벨 회전
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig

def display_socioeconomic_analysis(insights, chart_type):
    """사회경제 지표 분석 결과를 Streamlit 컴포넌트로 표시"""
    
    # 차트 타입별 아이콘과 단위
    icons_units = {
        "소득": ("💰", "만원"),
        "교육수준": ("🎓", "%"),
        "고등교육이수율": ("🏫", "%"),
        "고용률": ("💼", "%"),
        "실업률": ("📉", "%")
    }
    
    icon, unit = icons_units.get(chart_type, ("📊", ""))
    
    # 기본 정보 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📍 최고 지역**  
        **{insights['highest'][0]}**  
        {insights['highest'][1]:.1f}{unit}
        """)
    
    with col2:
        st.error(f"""
        **📍 최저 지역**  
        **{insights['lowest'][0]}**  
        {insights['lowest'][1]:.1f}{unit}
        """)
    
    # 격차 및 해석 표시
    if "소득" in chart_type:
        st.warning(f"""
        **💰 지역 간 소득 격차: {insights['difference']:.1f}{unit}**  
        수도권과 지방 간 소득 불평등이 건강 격차의 주요 원인이 될 수 있습니다.
        """)
    elif "교육" in chart_type:
        st.success(f"""
        **🎓 교육 격차: {insights['difference']:.1f}%p**  
        교육 수준은 건강 인식과 의료 접근성에 직접적인 영향을 미칩니다.
        """)
    elif "고용률" in chart_type:
        st.success(f"""
        **💼 고용률 격차: {insights['difference']:.1f}%p**  
        안정적인 고용은 의료비 부담 능력과 건강 관리에 중요한 요소입니다.
        """)
    elif "실업률" in chart_type:
        st.error(f"""
        **📉 실업률 격차: {insights['difference']:.1f}%p**  
        높은 실업률은 스트레스 증가와 의료 접근성 저하로 이어질 수 있습니다.
        """)

def plot_socioeconomic_comparison(income_data, education_data, employment_data, unemployment_data, higher_edu_data):
    """사회경제 지표 종합 비교 차트 - 2020-2024 평균값 사용"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 10))  # 크기 대폭 증가
    axes = axes.flatten()  # 2차원 배열을 1차원으로 변환
    
    # 2020-2024년 평균값 사용
    datasets = [
        income_data.mean(axis=0),
        education_data.mean(axis=0), 
        higher_edu_data.mean(axis=0),
        employment_data.mean(axis=0),
        unemployment_data.mean(axis=0)
    ]
    
    titles = ['소득', '교육수준', '고등교육이수율', '고용률', '실업률']
    colors = socioeconomic_colors
    
    for i, (data, title, color) in enumerate(zip(datasets, titles, colors)):
        axes[i].bar(data.index, data.values, color=color, alpha=0.8, edgecolor='#8B4513')
        axes[i].set_title(title, fontsize=14, fontweight='bold')  # 제목 크기 증가
        axes[i].tick_params(axis='x', rotation=45, labelsize=10)  # 라벨 크기 증가
        axes[i].tick_params(axis='y', labelsize=10)
        axes[i].grid(True, alpha=0.3)
        
        # Y축 범위 조정 - 차이 극명하게
        min_val = data.min()
        max_val = data.max()
        range_val = max_val - min_val
        margin = range_val * 0.05
        axes[i].set_ylim(min_val - margin, max_val + margin)
    
    # 마지막 빈 서브플롯 숨기기
    axes[5].set_visible(False)
    
    plt.tight_layout(pad=3.0)  # 여백 증가
    return fig

def plot_socioeconomic_correlation(data1, data2, title, xlabel, ylabel):
    """두 사회경제 지표 간의 상관관계 - 2020-2024 평균값 사용"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 2020-2024년 평균값 사용
    data1_mean = data1.mean(axis=0)
    data2_mean = data2.mean(axis=0)
    
    # 산점도 그리기
    scatter = ax.scatter(data1_mean.values, data2_mean.values, 
                        c='#D97757', s=120, alpha=0.7, edgecolors='#8B4513', linewidth=1.5)
    
    # 지역명 라벨 추가
    for i, region in enumerate(data1_mean.index):
        ax.annotate(region, (data1_mean.iloc[i], data2_mean.iloc[i]), 
                   xytext=(5, 5), textcoords='offset points', 
                   fontsize=9, ha='left', va='bottom')
    
    # 회귀선 추가
    z = np.polyfit(data1_mean.values, data2_mean.values, 1)
    p = np.poly1d(z)
    ax.plot(data1_mean.values, p(data1_mean.values), "r--", alpha=0.8, linewidth=2)
    
    # 상관계수 계산
    correlation = np.corrcoef(data1_mean.values, data2_mean.values)[0, 1]
    
    # 제목과 라벨 설정
    ax.set_title(f'{title}\n(상관계수: {correlation:.3f})', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig, correlation

def display_socioeconomic_correlation_analysis(correlation, var1_name, var2_name):
    """사회경제 지표 상관관계 분석 결과 표시"""
    
    # 상관관계 강도 판단
    if abs(correlation) >= 0.7:
        strength = "강한"
        strength_emoji = "🔥"
    elif abs(correlation) >= 0.3:
        strength = "중간" 
        strength_emoji = "⚡"
    else:
        strength = "약한"
        strength_emoji = "💨"
    
    direction = "양의" if correlation > 0 else "음의"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="상관계수",
            value=f"{correlation:.3f}",
            delta=f"{strength} {direction} 상관관계"
        )
    
    with col2:
        st.info(f"""
        **{strength_emoji} 관계 강도**  
        {strength} {direction} 상관관계
        """)
    
    # 해석
    if "소득" in var1_name and "교육" in var2_name:
        if correlation > 0.5:
            st.success("""
            **✅ 예상된 양의 상관관계!**  
            소득이 높은 지역일수록 교육 수준도 높습니다. 사회경제적 요인들이 서로 연관되어 있음을 보여줍니다.
            """)
        else:
            st.warning("""
            **🤔 예상보다 약한 상관관계**  
            소득과 교육 수준이 완전히 일치하지 않는 지역들이 있습니다.
            """)
    
    elif "고용률" in var1_name and "실업률" in var2_name:
        if correlation < -0.7:
            st.success("""
            **✅ 예상된 강한 음의 상관관계!**  
            고용률이 높은 지역일수록 실업률이 낮습니다. 정상적인 패턴을 보여줍니다.
            """)
        else:
            st.warning("""
            **⚡ 예상보다 약한 음의 상관관계**  
            일부 지역에서 고용률과 실업률이 예상과 다른 패턴을 보입니다.
            """)
    
    # 건강 불평등과의 연관성
    st.markdown("---")
    st.markdown("**💡 건강 불평등과의 연관성**")
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("""
        **🎯 직접적 영향**  
        사회경제적 격차는 의료 접근성과 건강 행동에 직접적인 영향을 미칩니다.
        """)
    
    with col4:
        st.warning("""
        **📋 정책적 접근**  
        건강 불평등 해소를 위해서는 사회경제적 격차 해소가 선행되어야 합니다.
        """)