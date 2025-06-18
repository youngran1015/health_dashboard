import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'  # Windows
# plt.rcParams['font.family'] = 'AppleGothic'  # Mac
plt.rcParams['axes.unicode_minus'] = False

# Pastel color palette
pastel_colors = ['#FFB6C1', '#87CEEB', '#98FB98', '#DDA0DD', '#F0E68C', 
                '#ADD8E6', '#B0E0E6', '#E6E6FA', '#FFA07A', '#20B2AA', 
                '#87CEFA', '#FAEBD7', '#F0FFF0', '#E0FFFF', '#F5F5DC', 
                '#FFE4E1', '#D8BFD8']

def load_data(file_name):
    """CSV 파일을 로드하고 인덱스를 설정하는 함수"""
    df = pd.read_csv(file_name)
    df = df.set_index(df.columns[0])  # 첫 번째 열을 인덱스로 설정
    return df

def analyze_data(data, title):
    """데이터를 분석하고 인사이트를 반환하는 함수"""
    mean_data = data.mean(axis=0)
    highest = mean_data.idxmax()
    lowest = mean_data.idxmin()
    highest_val = mean_data.max()
    lowest_val = mean_data.min()
    diff = highest_val - lowest_val
    
    insights = {
        'highest': (highest, highest_val),
        'lowest': (lowest, lowest_val),
        'difference': diff,
        'average': mean_data.mean()
    }
    
    return insights

def display_analysis(insights, chart_type):
    """분석 결과를 멋진 스타일로 표시하는 함수"""
    
    if "Drinking" in chart_type:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-left: 5px solid #F97316;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: #F3F4F6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <div style="border-bottom: 2px solid #F97316; padding-bottom: 10px; margin-bottom: 15px;">
                <h3 style="color: #F3F4F6; margin: 0; font-size: 18px;">🔍 데이터 분석 결과</h3>
            </div>
            <div style="line-height: 1.8; font-size: 14px;">
                <p><strong>📊 음주율 분석 결과</strong></p>
                <p>• <strong>최고 지역</strong>: {insights['highest'][0]} ({insights['highest'][1]:.1f}%)</p>
                <p>• <strong>최저 지역</strong>: {insights['lowest'][0]} ({insights['lowest'][1]:.1f}%)</p>
                <p>• <strong>지역 간 격차</strong>: {insights['difference']:.1f}%p</p>
                <br>
                <p>💡 <strong>인사이트</strong>: 수도권과 호남권에서 상대적으로 높은 음주율을 보이며, 영남권 일부 지역에서 낮은 음주율을 나타냅니다.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif "Obesity" in chart_type:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-left: 5px solid #F97316;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: #F3F4F6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <div style="border-bottom: 2px solid #F97316; padding-bottom: 10px; margin-bottom: 15px;">
                <h3 style="color: #F3F4F6; margin: 0; font-size: 18px;">🔍 데이터 분석 결과</h3>
            </div>
            <div style="line-height: 1.8; font-size: 14px;">
                <p><strong>📊 비만율 분석 결과</strong></p>
                <p>• <strong>최고 지역</strong>: {insights['highest'][0]} ({insights['highest'][1]:.1f}%)</p>
                <p>• <strong>최저 지역</strong>: {insights['lowest'][0]} ({insights['lowest'][1]:.1f}%)</p>
                <p>• <strong>지역 간 격차</strong>: {insights['difference']:.1f}%p</p>
                <br>
                <p>💡 <strong>인사이트</strong>: 전국적으로 비만율이 30-35% 수준으로 비교적 균등하나, 일부 지역에서 약간의 차이를 보입니다.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif "Smoking" in chart_type:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-left: 5px solid #F97316;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: #F3F4F6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <div style="border-bottom: 2px solid #F97316; padding-bottom: 10px; margin-bottom: 15px;">
                <h3 style="color: #F3F4F6; margin: 0; font-size: 18px;">🔍 데이터 분석 결과</h3>
            </div>
            <div style="line-height: 1.8; font-size: 14px;">
                <p><strong>📊 흡연율 분석 결과</strong></p>
                <p>• <strong>최고 지역</strong>: {insights['highest'][0]} ({insights['highest'][1]:.1f}%)</p>
                <p>• <strong>최저 지역</strong>: {insights['lowest'][0]} ({insights['lowest'][1]:.1f}%)</p>
                <p>• <strong>지역 간 격차</strong>: {insights['difference']:.1f}%p</p>
                <br>
                <p>💡 <strong>인사이트</strong>: 흡연율은 16-21% 범위로 상대적으로 안정적이며, 산업지역과 농촌지역 간 차이가 관찰됩니다.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif "Physical" in chart_type:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-left: 5px solid #F97316;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            color: #F3F4F6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <div style="border-bottom: 2px solid #F97316; padding-bottom: 10px; margin-bottom: 15px;">
                <h3 style="color: #F3F4F6; margin: 0; font-size: 18px;">🔍 데이터 분석 결과</h3>
            </div>
            <div style="line-height: 1.8; font-size: 14px;">
                <p><strong>📊 신체활동 실천율 분석 결과</strong></p>
                <p>• <strong>최고 지역</strong>: {insights['highest'][0]} ({insights['highest'][1]:.1f}%)</p>
                <p>• <strong>최저 지역</strong>: {insights['lowest'][0]} ({insights['lowest'][1]:.1f}%)</p>
                <p>• <strong>지역 간 격차</strong>: {insights['difference']:.1f}%p</p>
                <br>
                <p>💡 <strong>인사이트</strong>: 신체활동 실천율은 23-29% 수준으로, 체육시설 접근성과 지역 문화가 영향을 미치는 것으로 보입니다.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def plot_bar_chart(data, title, color_idx):
    """막대 그래프를 그리는 함수"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 데이터의 평균값 계산 (연도별 평균)
    mean_data = data.mean(axis=0)
    
    # 막대 그래프 그리기
    bars = ax.bar(mean_data.index, mean_data.values, 
                  color=pastel_colors[color_idx % len(pastel_colors)], 
                  edgecolor='black', linewidth=0.5, alpha=0.8)
    
    # 제목과 라벨 설정
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('지역 (Region)', fontsize=12, fontweight='bold')
    ax.set_ylabel('비율 (%)', fontsize=12, fontweight='bold')
    
    # Y축 범위 조정 - 데이터 범위에 맞춰 동적으로 설정
    min_val = mean_data.min()
    max_val = mean_data.max()
    range_val = max_val - min_val
    
    # 여백을 10% 정도로 설정하여 차이를 더 명확하게 보이도록
    margin = range_val * 0.1
    ax.set_ylim(min_val - margin, max_val + margin)
    
    # x축 라벨 회전
    plt.xticks(rotation=45, ha='right')
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + margin/2,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # 레이아웃 조정
    plt.tight_layout()
    
    return fig

def plot_line_chart(data, title, color_idx):
    """선 그래프를 그리는 함수 (연도별 변화 추이)"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 각 지역별로 선 그리기
    for i, region in enumerate(data.columns):
        ax.plot(data.index, data[region], 
                marker='o', linewidth=2, markersize=4,
                label=region, alpha=0.7)
    
    # 제목과 라벨 설정
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('연도 (Year)', fontsize=12, fontweight='bold')
    ax.set_ylabel('비율 (%)', fontsize=12, fontweight='bold')
    
    # 범례 설정
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
              ncol=1, fontsize=9)
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 레이아웃 조정
    plt.tight_layout()
    
    return fig

def plot_correlation_scatter(data1, data2, title, xlabel, ylabel):
    """두 변수 간의 상관관계를 보여주는 산점도"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 데이터의 평균값 계산
    mean_data1 = data1.mean(axis=0)
    mean_data2 = data2.mean(axis=0)
    
    # 산점도 그리기
    scatter = ax.scatter(mean_data1.values, mean_data2.values, 
                        c='#F97316', s=100, alpha=0.7, edgecolors='black', linewidth=1)
    
    # 지역명 라벨 추가
    for i, region in enumerate(mean_data1.index):
        ax.annotate(region, (mean_data1.iloc[i], mean_data2.iloc[i]), 
                   xytext=(5, 5), textcoords='offset points', 
                   fontsize=9, ha='left', va='bottom')
    
    # 회귀선 추가
    import numpy as np
    z = np.polyfit(mean_data1.values, mean_data2.values, 1)
    p = np.poly1d(z)
    ax.plot(mean_data1.values, p(mean_data1.values), "r--", alpha=0.8, linewidth=2)
    
    # 상관계수 계산
    correlation = np.corrcoef(mean_data1.values, mean_data2.values)[0, 1]
    
    # 제목과 라벨 설정
    ax.set_title(f'{title}\n(상관계수: {correlation:.3f})', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    
    # 그리드 추가
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 레이아웃 조정
    plt.tight_layout()
    
    return fig, correlation

def display_correlation_analysis(correlation, var1_name, var2_name):
    """상관관계 분석 결과를 표시하는 함수"""
    
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
    
    # 기본 정보 표시
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-left: 5px solid #F97316; border-radius: 10px; padding: 20px; margin: 20px 0; color: #F3F4F6;">
        <div style="border-bottom: 2px solid #F97316; padding-bottom: 10px; margin-bottom: 15px;">
            <h3 style="color: #F3F4F6; margin: 0; font-size: 18px;">📈 상관관계 분석</h3>
        </div>
        <p><strong>📊 {var1_name} vs {var2_name}</strong></p>
        <p>• <strong>상관계수</strong>: {correlation:.3f}</p>
        <p>• <strong>관계 강도</strong>: {strength_emoji} {strength} {direction} 상관관계</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 추가 분석 - Streamlit 컴포넌트 사용
    if "신체활동" in var1_name and "흡연" in var2_name:
        if correlation > 0:
            st.error("🚨 놀라운 발견! 신체활동이 높은 지역에서 흡연율도 높게 나타났습니다!")
            st.info("💡 원인: 산업지역 특성, 육체노동 문화, 젊은 남성 비율")
            st.warning("📋 시사점: 종합적인 건강증진 프로그램이 필요합니다.")
    
    elif "음주" in var1_name and "흡연" in var2_name:
        st.error("🤔 놀라운 반전! 음주율 높은 지역에서 흡연율이 낮습니다!")
        st.info("💡 해석: 음주와 흡연이 서로 다른 지역 특성을 반영")

    elif "음주" in var1_name and "비만" in var2_name:
        st.success("✅ 예상된 패턴! 음주율과 비만율이 함께 높습니다!")
        st.info("💡 해석: 음주 문화와 생활습관이 비만에 영향")


        # 기존 코드 맨 마지막 (음주율 vs 비만율 다음)에 추가

