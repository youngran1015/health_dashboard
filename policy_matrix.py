import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def load_policy_data():
    """정책 매트릭스를 위한 데이터 로드"""
    try:
        # 사회경제 데이터 (2024년 기준)
        income_data = pd.read_csv('data/socioeconomic/소득_2020_2024.csv', index_col='년도').loc[2024]
        education_data = pd.read_csv('data/socioeconomic/교육수준_2020_2024.csv', index_col='년도').loc[2024]
        employment_data = pd.read_csv('data/socioeconomic/고용률_2020_2024.csv', index_col='년도').loc[2024]
        unemployment_data = pd.read_csv('data/socioeconomic/실업률_2020_2024.csv', index_col='년도').loc[2024]
        
        # 의료 접근성 데이터 (2024년 기준)
        hospitals_data = pd.read_csv('data/health_accessibility/hospitals_2020_2024.csv', index_col='지역')['2024']
        doctors_data = pd.read_csv('data/health_accessibility/doctors_2020_2024.csv', index_col='지역')['2024']
        healthcenters_data = pd.read_csv('data/health_accessibility/healthcenters_2020_2024.csv', index_col='지역')['2024']
        
        # 건강 지표 데이터 (평균)
        activity_data = pd.read_csv('data/health_region/activity_2020_2024_kr.csv', index_col=0).mean(axis=0)
        smoking_data = pd.read_csv('data/health_region/smoking_2020_2024_kr.csv', index_col=0).mean(axis=0)
        
        # 정책 필요도 계산을 위한 데이터 결합
        policy_df = pd.DataFrame({
            '소득': income_data,
            '교육수준': education_data,
            '고용률': employment_data,
            '실업률': unemployment_data,
            '병원수': hospitals_data,
            '의사수': doctors_data,
            '보건소수': healthcenters_data,
            '신체활동률': activity_data,
            '흡연율': smoking_data
        })
        
        return policy_df
        
    except Exception as e:
        st.error(f"정책 데이터 로딩 오류: {str(e)}")
        return None

def calculate_policy_priorities(data):
    """지역별 정책 우선순위 계산"""
    
    # 정책 영역별 필요도 계산 (낮을수록 높은 우선순위)
    policy_matrix = pd.DataFrame(index=data.index)
    
    # 1. 경제 정책 필요도 (소득, 고용률 기반)
    income_rank = data['소득'].rank(ascending=False)  # 소득이 낮을수록 높은 순위
    employment_rank = data['고용률'].rank(ascending=False)
    unemployment_rank = data['실업률'].rank(ascending=True)  # 실업률이 높을수록 높은 순위
    
    policy_matrix['경제정책'] = ((income_rank + employment_rank + unemployment_rank) / 3).round(1)
    
    # 2. 교육 정책 필요도
    education_rank = data['교육수준'].rank(ascending=False)
    policy_matrix['교육정책'] = education_rank.round(1)
    
    # 3. 의료 정책 필요도 (병원, 의사, 보건소 기반)
    hospital_rank = data['병원수'].rank(ascending=False)
    doctor_rank = data['의사수'].rank(ascending=False)
    healthcenter_rank = data['보건소수'].rank(ascending=False)
    
    policy_matrix['의료정책'] = ((hospital_rank + doctor_rank + healthcenter_rank) / 3).round(1)
    
    # 4. 건강증진 정책 필요도
    activity_rank = data['신체활동률'].rank(ascending=False)
    smoking_rank = data['흡연율'].rank(ascending=True)  # 흡연율이 높을수록 높은 순위
    
    policy_matrix['건강증진정책'] = ((activity_rank + smoking_rank) / 2).round(1)
    
    # 5. 종합 우선순위 (가중평균)
    policy_matrix['종합우선순위'] = (
        policy_matrix['경제정책'] * 0.3 +
        policy_matrix['교육정책'] * 0.2 +
        policy_matrix['의료정책'] * 0.3 +
        policy_matrix['건강증진정책'] * 0.2
    ).round(1)
    
    return policy_matrix

def create_policy_recommendations(policy_matrix, data):
    """지역별 맞춤형 정책 제안"""
    
    recommendations = {}
    
    for region in policy_matrix.index:
        region_data = policy_matrix.loc[region]
        original_data = data.loc[region]
        
        # 가장 시급한 정책 영역 찾기 (순위가 높을수록 시급)
        policy_priorities = region_data[['경제정책', '교육정책', '의료정책', '건강증진정책']].sort_values(ascending=False)
        
        top_priority = policy_priorities.index[0]
        second_priority = policy_priorities.index[1]
        
        # 정책 제안 생성
        recommendations[region] = {
            'rank': int(region_data['종합우선순위']),
            'top_priority': top_priority,
            'second_priority': second_priority,
            'suggestions': generate_policy_suggestions(region, top_priority, second_priority, original_data)
        }
    
    return recommendations

def generate_policy_suggestions(region, top_priority, second_priority, data):
    """구체적인 정책 제안 생성"""
    
    suggestions = {
        'primary': '',
        'secondary': '',
        'specific_actions': []
    }
    
    # 주요 정책 제안
    if top_priority == '경제정책':
        suggestions['primary'] = f"{region}은 소득 증대와 고용 창출이 최우선 과제입니다."
        if data['실업률'] > 4.0:
            suggestions['specific_actions'].append("🎯 청년 일자리 창출 프로그램 강화")
            suggestions['specific_actions'].append("💼 지역 특화 산업 육성")
        if data['소득'] < 4000:
            suggestions['specific_actions'].append("💰 중소기업 지원 확대")
            suggestions['specific_actions'].append("🏭 기업 유치 인센티브 제공")
    
    elif top_priority == '교육정책':
        suggestions['primary'] = f"{region}은 교육 인프라 확충과 교육 격차 해소가 시급합니다."
        if data['교육수준'] < 60:
            suggestions['specific_actions'].append("🎓 평생교육 프로그램 확대")
            suggestions['specific_actions'].append("📚 원격교육 인프라 구축")
            suggestions['specific_actions'].append("🏫 교육시설 현대화")
    
    elif top_priority == '의료정책':
        suggestions['primary'] = f"{region}은 의료 접근성 개선이 가장 중요한 과제입니다."
        if data['의사수'] < 2000:
            suggestions['specific_actions'].append("👩‍⚕️ 의료인력 확충 지원")
            suggestions['specific_actions'].append("🚁 응급의료 시스템 강화")
        if data['병원수'] < 2000:
            suggestions['specific_actions'].append("🏥 지역 의료기관 확충")
            suggestions['specific_actions'].append("🚌 의료 접근성 개선 (교통)")
    
    elif top_priority == '건강증진정책':
        suggestions['primary'] = f"{region}은 건강한 생활습관 증진이 필요합니다."
        if data['신체활동률'] < 25:
            suggestions['specific_actions'].append("🏃‍♂️ 체육시설 확충")
            suggestions['specific_actions'].append("🌳 건강걷기 프로그램 운영")
        if data['흡연율'] > 20:
            suggestions['specific_actions'].append("🚭 금연 지원 프로그램 강화")
            suggestions['specific_actions'].append("💨 금연 환경 조성")
    
    # 보조 정책 제안
    if second_priority == '경제정책':
        suggestions['secondary'] = "경제 활성화 지원이 추가로 필요합니다."
    elif second_priority == '교육정책':
        suggestions['secondary'] = "교육 기회 확대가 보완적으로 요구됩니다."
    elif second_priority == '의료정책':
        suggestions['secondary'] = "의료 서비스 개선이 동반되어야 합니다."
    elif second_priority == '건강증진정책':
        suggestions['secondary'] = "건강증진 프로그램 확대가 필요합니다."
    
    return suggestions

def plot_policy_heatmap(policy_matrix):
    """정책 우선순위 히트맵"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 데이터 준비 (순위를 역순으로 변환하여 색상 표현)
    heatmap_data = policy_matrix[['경제정책', '교육정책', '의료정책', '건강증진정책']].copy()
    
    # 순위를 역순으로 변환 (높은 순위 = 높은 우선순위)
    max_rank = heatmap_data.max().max()
    heatmap_data = max_rank + 1 - heatmap_data
    
    # 히트맵 생성 (더 밝은 색상으로 변경)
    im = ax.imshow(heatmap_data.values, cmap='OrRd', aspect='auto', alpha=0.8)
    
    # 축 설정
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns, fontsize=12, fontweight='bold')
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index, fontsize=11)
    
    # 값 표시 (검은색으로 변경하고 크기 증가)
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            # 배경 색상에 따라 텍스트 색상 조정
            value = heatmap_data.iloc[i, j]
            text_color = 'white' if value > (max_rank * 0.6) else 'black'
            ax.text(j, i, f'{value:.1f}',
                   ha="center", va="center", color=text_color, 
                   fontweight='bold', fontsize=11)
    
    ax.set_title('지역별 정책 우선순위 매트릭스\n(높은 값 = 높은 우선순위)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('정책 영역', fontsize=12, fontweight='bold')
    ax.set_ylabel('지역', fontsize=12, fontweight='bold')
    
    # 컬러바
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('정책 우선순위', rotation=270, labelpad=15, fontsize=12)
    
    plt.tight_layout()
    return fig

def plot_priority_ranking(policy_matrix):
    """종합 우선순위 순위 차트"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 종합 우선순위로 정렬 (높은 순위 = 높은 우선순위)
    sorted_data = policy_matrix.sort_values('종합우선순위', ascending=False)
    
    # 더 밝은 색상으로 변경
    colors = []
    for i, region in enumerate(sorted_data.index):
        if i < 5:  # 상위 5개 지역 (가장 시급)
            colors.append('#FF6B6B')  # 밝은 빨간색
        elif i < 10:  # 중간 5개 지역
            colors.append('#FFB347')  # 밝은 주황색
        else:  # 하위 지역들
            colors.append('#90EE90')  # 밝은 녹색
    
    bars = ax.barh(range(len(sorted_data)), sorted_data['종합우선순위'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # 지역명 설정
    ax.set_yticks(range(len(sorted_data)))
    ax.set_yticklabels(sorted_data.index, fontsize=11)
    ax.invert_yaxis()
    
    # 제목과 라벨
    ax.set_xlabel('종합 정책 우선순위 (높을수록 시급)', fontsize=12, fontweight='bold')
    ax.set_title('지역별 정책 개입 우선순위 순위', fontsize=16, fontweight='bold', pad=20)
    
    # 점수 표시 (검은색으로 변경)
    for i, (bar, score) in enumerate(zip(bars, sorted_data['종합우선순위'])):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{score:.1f}', ha='left', va='center', fontweight='bold', 
                color='black', fontsize=10)
    
    # 범례 (더 밝은 색상으로)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#FF6B6B', label='최우선 지역 (1-5위)'),
        Patch(facecolor='#FFB347', label='우선 지역 (6-10위)'),
        Patch(facecolor='#90EE90', label='안정 지역 (11위 이하)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return fig

def plot_policy_spider(policy_matrix, top_regions=6):
    """상위 지역 정책 우선순위 스파이더 차트"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    # 상위 지역들 선택
    sorted_data = policy_matrix.sort_values('종합우선순위', ascending=False).head(top_regions)
    
    categories = ['경제정책', '교육정책', '의료정책', '건강증진정책']
    colors = ['#DC143C', '#FF8C00', '#FFD700', '#32CD32', '#4169E1', '#8A2BE2']
    
    for idx, (region, row) in enumerate(sorted_data.iterrows()):
        ax = axes[idx]
        
        # 순위를 역순으로 변환 (높은 값 = 높은 우선순위)
        max_rank = policy_matrix[categories].max().max()
        values = [max_rank + 1 - row[cat] for cat in categories]
        values += values[:1]  # 차트를 닫기 위해
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]
        
        ax.plot(angles, values, 'o-', linewidth=3, color=colors[idx])
        ax.fill(angles, values, alpha=0.25, color=colors[idx])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, max_rank + 1)
        ax.set_title(f"{region}\n(종합순위: {row['종합우선순위']:.1f})", 
                    fontsize=12, fontweight='bold', pad=20)
        ax.grid(True)
    
    plt.tight_layout()
    return fig

def display_policy_recommendations(recommendations):
    """정책 제안 표시"""
    
    st.markdown("### 📋 지역별 맞춤형 정책 제안")
    
    # 우선순위 순으로 정렬
    sorted_regions = sorted(recommendations.items(), key=lambda x: x[1]['rank'], reverse=True)
    
    for region, rec in sorted_regions[:10]:  # 상위 10개 지역만 표시
        
        # 우선순위에 따른 색상 구분
        if rec['rank'] <= 5:
            border_color = "red"
            priority_text = "🚨 최우선"
        elif rec['rank'] <= 10:
            border_color = "orange" 
            priority_text = "⚠️ 우선"
        else:
            border_color = "green"
            priority_text = "✅ 일반"
        
        with st.container():
            st.markdown(f"""
            <div style="border-left: 5px solid {border_color}; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
                <h4>{priority_text} | {region} (순위: {rec['rank']}위)</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**🎯 주요 정책**: {rec['suggestions']['primary']}")
                st.markdown(f"**➕ 보조 정책**: {rec['suggestions']['secondary']}")
                
                if rec['suggestions']['specific_actions']:
                    st.markdown("**구체적 실행 방안**:")
                    for action in rec['suggestions']['specific_actions']:
                        st.markdown(f"• {action}")
            
            with col2:
                st.markdown(f"**최우선 영역**: {rec['top_priority']}")
                st.markdown(f"**2순위 영역**: {rec['second_priority']}")

def create_policy_dashboard():
    """정책 매트릭스 대시보드 메인 함수"""
    st.header("📊 정책 우선순위 매트릭스")
    st.markdown("**지역별 정책 필요도를 분석하여 맞춤형 정책 제안을 제공합니다.**")
    
    # 데이터 로드 및 분석
    with st.spinner("정책 우선순위를 분석하고 있습니다..."):
        policy_data = load_policy_data()
        
        if policy_data is None:
            st.error("정책 데이터를 불러올 수 없습니다.")
            return
        
        # 정책 우선순위 계산
        policy_matrix = calculate_policy_priorities(policy_data)
        recommendations = create_policy_recommendations(policy_matrix, policy_data)
        
        # 결과 표시
        st.markdown("### 🎯 정책 우선순위 분석 결과")
        
        # 주요 통계
        most_urgent = policy_matrix.sort_values('종합우선순위', ascending=False).index[0]
        least_urgent = policy_matrix.sort_values('종합우선순위', ascending=False).index[-1]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("최우선 지역", most_urgent, 
                     f"순위: {policy_matrix.loc[most_urgent, '종합우선순위']:.1f}")
        
        with col2:
            st.metric("안정 지역", least_urgent,
                     f"순위: {policy_matrix.loc[least_urgent, '종합우선순위']:.1f}")
        
        with col3:
            avg_priority = policy_matrix['종합우선순위'].mean()
            st.metric("전국 평균", f"{avg_priority:.1f}", "정책 우선순위")
        
        # 히트맵
        st.markdown("#### 🔥 정책 우선순위 히트맵")
        fig_heatmap = plot_policy_heatmap(policy_matrix)
        st.pyplot(fig_heatmap)
        
        # 순위 차트
        st.markdown("#### 🏆 종합 정책 우선순위 순위")
        fig_ranking = plot_priority_ranking(policy_matrix)
        st.pyplot(fig_ranking)
        
        # 스파이더 차트
        st.markdown("#### 🕷️ 상위 6개 지역 정책 프로필")
        fig_spider = plot_policy_spider(policy_matrix)
        st.pyplot(fig_spider)
        
        # 정책 제안
        display_policy_recommendations(recommendations)
        
        # 다운로드
        st.markdown("---")
        col_dl1, col_dl2 = st.columns(2)
        
        with col_dl1:
            csv_matrix = policy_matrix.to_csv(encoding='utf-8-sig')
            st.download_button(
                label="📥 정책 매트릭스 다운로드 (CSV)",
                data=csv_matrix,
                file_name="정책우선순위매트릭스.csv",
                mime="text/csv"
            )
        
        with col_dl2:
            # 정책 제안을 DataFrame으로 변환
            recommendations_list = []
            for region, rec in recommendations.items():
                recommendations_list.append({
                    '지역': region,
                    '종합순위': rec['rank'],
                    '최우선정책': rec['top_priority'],
                    '2순위정책': rec['second_priority'],
                    '주요정책제안': rec['suggestions']['primary']
                })
            
            rec_df = pd.DataFrame(recommendations_list)
            csv_rec = rec_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 정책 제안서 다운로드 (CSV)",
                data=csv_rec,
                file_name="지역별정책제안서.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    create_policy_dashboard()