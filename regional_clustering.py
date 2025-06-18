import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정
# 한글 폰트 설정
import matplotlib.font_manager as fm
import os
font_path = os.path.join(os.getcwd(), 'fonts', 'NotoSansKR-VariableFont_wght.ttf')
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans KR'
plt.rcParams['axes.unicode_minus'] = False

def load_clustering_data():
    """클러스터링을 위한 데이터 로드"""
    try:
        # 사회경제 데이터 (2024년 기준)
        income_data = pd.read_csv('data/socioeconomic/소득_2020_2024.csv', index_col='년도').loc[2024]
        education_data = pd.read_csv('data/socioeconomic/교육수준_2020_2024.csv', index_col='년도').loc[2024]
        employment_data = pd.read_csv('data/socioeconomic/고용률_2020_2024.csv', index_col='년도').loc[2024]
        
        # 의료 접근성 데이터 (2024년 기준)
        hospitals_data = pd.read_csv('data/health_accessibility/hospitals_2020_2024.csv', index_col='지역')['2024']
        doctors_data = pd.read_csv('data/health_accessibility/doctors_2020_2024.csv', index_col='지역')['2024']
        
        # 건강 지표 데이터 (평균)
        activity_data = pd.read_csv('data/health_region/activity_2020_2024_kr.csv', index_col=0).mean(axis=0)
        
        # 데이터 결합
        clustering_df = pd.DataFrame({
            '소득': income_data,
            '교육수준': education_data,
            '고용률': employment_data,
            '병원수': hospitals_data,
            '의사수': doctors_data,
            '신체활동률': activity_data
        })
        
        return clustering_df
        
    except Exception as e:
        st.error(f"클러스터링 데이터 로딩 오류: {str(e)}")
        return None

def simple_clustering(data):
    """간단한 규칙 기반 클러스터링 (sklearn 없이)"""
    
    # 정규화 (0-1 스케일)
    normalized_data = data.copy()
    for col in data.columns:
        min_val = data[col].min()
        max_val = data[col].max()
        normalized_data[col] = (data[col] - min_val) / (max_val - min_val)
    
    # 종합 점수 계산 (가중평균)
    scores = (
        normalized_data['소득'] * 0.3 +
        normalized_data['교육수준'] * 0.2 +
        normalized_data['고용률'] * 0.15 +
        normalized_data['병원수'] * 0.15 +
        normalized_data['의사수'] * 0.15 +
        normalized_data['신체활동률'] * 0.05
    )
    
    # 4개 그룹으로 분류
    clusters = pd.cut(scores, bins=4, labels=[0, 1, 2, 3])
    
    # 결과 데이터프레임 생성
    result_df = data.copy()
    result_df['클러스터'] = clusters.astype(int)
    result_df['종합점수'] = scores
    
    return result_df

def analyze_simple_clusters(clustered_data):
    """간단한 클러스터별 특성 분석"""
    
    cluster_analysis = {}
    
    for cluster_id in sorted(clustered_data['클러스터'].unique()):
        cluster_data = clustered_data[clustered_data['클러스터'] == cluster_id]
        regions = cluster_data.index.tolist()
        
        # 클러스터별 평균값
        means = cluster_data.drop(['클러스터', '종합점수'], axis=1).mean()
        
        # 클러스터 특성 분석 (점수 기반)
        avg_score = cluster_data['종합점수'].mean()
        
        if avg_score >= 0.75:  # 상위 25%
            cluster_name = "선진형"
            description = "높은 소득, 우수한 의료 인프라, 높은 교육 수준"
            color = "#FF6B6B"
        elif avg_score >= 0.5:  # 상위 50%
            cluster_name = "발전형" 
            description = "중상 수준의 소득과 의료 인프라, 안정적 고용"
            color = "#4ECDC4"
        elif avg_score >= 0.25:  # 상위 75%
            cluster_name = "성장형"
            description = "중간 수준의 발전도, 개선 여지 있음"
            color = "#45B7D1"
        else:  # 하위 25%
            cluster_name = "개발필요형"
            description = "낮은 소득과 의료 접근성, 집중적 개발 필요"
            color = "#96CEB4"
        
        cluster_analysis[cluster_id] = {
            'name': cluster_name,
            'description': description,
            'regions': regions,
            'means': means,
            'color': color,
            'count': len(regions),
            'avg_score': avg_score
        }
    
    return cluster_analysis

def plot_simple_cluster_comparison(clustered_data, cluster_analysis):
    """클러스터별 특성 비교 막대 차트"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    categories = ['소득', '교육수준', '고용률', '병원수', '의사수', '신체활동률']
    
    for idx, category in enumerate(categories):
        ax = axes[idx]
        
        cluster_names = []
        cluster_values = []
        cluster_colors = []
        
        for cluster_id, info in cluster_analysis.items():
            cluster_names.append(info['name'])
            cluster_values.append(info['means'][category])
            cluster_colors.append(info['color'])
        
        bars = ax.bar(cluster_names, cluster_values, color=cluster_colors, alpha=0.8)
        ax.set_title(f'{category} 비교', fontsize=12, fontweight='bold')
        ax.set_ylabel('평균값', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        # 값 표시
        for bar, value in zip(bars, cluster_values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 
                   max(cluster_values) * 0.01, f'{value:.1f}',
                   ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    return fig

def plot_cluster_ranking(clustered_data, cluster_analysis):
    """지역별 종합 점수 순위"""
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # 종합점수로 정렬
    sorted_data = clustered_data.sort_values('종합점수', ascending=True)
    
    # 클러스터별 색상 적용
    colors = []
    for region in sorted_data.index:
        cluster_id = sorted_data.loc[region, '클러스터']
        colors.append(cluster_analysis[cluster_id]['color'])
    
    bars = ax.barh(range(len(sorted_data)), sorted_data['종합점수'], 
                   color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # 지역명 설정
    ax.set_yticks(range(len(sorted_data)))
    ax.set_yticklabels(sorted_data.index)
    
    # 제목과 라벨
    ax.set_xlabel('종합 발전 점수 (0-1)', fontsize=12, fontweight='bold')
    ax.set_title('지역별 종합 발전 점수 순위', fontsize=16, fontweight='bold', pad=20)
    
    # 점수 표시
    for i, (bar, score) in enumerate(zip(bars, sorted_data['종합점수'])):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{score:.3f}', ha='left', va='center', fontweight='bold')
    
    # 범례
    from matplotlib.patches import Patch
    legend_elements = []
    for cluster_id, info in cluster_analysis.items():
        legend_elements.append(Patch(facecolor=info['color'], label=info['name']))
    ax.legend(handles=legend_elements, loc='lower right')
    
    ax.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    return fig

def display_simple_cluster_details(cluster_analysis):
    """클러스터별 상세 정보 표시"""
    
    st.markdown("### 📋 클러스터별 상세 분석")
    
    for cluster_id, info in cluster_analysis.items():
        with st.expander(f"🏷️ {info['name']} ({info['count']}개 지역) - 평균점수: {info['avg_score']:.3f}"):
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"**특성**: {info['description']}")
                st.markdown(f"**포함 지역**: {', '.join(info['regions'])}")
                st.markdown(f"**발전도 점수**: {info['avg_score']:.3f}")
            
            with col2:
                # 특성값 표시
                means_df = pd.DataFrame({
                    '지표': info['means'].index,
                    '평균값': info['means'].values.round(1)
                })
                st.dataframe(means_df, use_container_width=True)

def create_clustering_dashboard():
    """지역 클러스터링 대시보드 메인 함수 (sklearn 없는 버전)"""
    st.header("🗺️ 지역 클러스터링 분석")
    st.markdown("**유사한 특성을 가진 지역들을 그룹화하여 지역 유형을 분석합니다.**")
    
    st.info("📌 **참고**: 이 분석은 sklearn 라이브러리 없이 간단한 규칙 기반으로 수행됩니다.")
    
    # 데이터 로드 및 클러스터링
    with st.spinner("지역 클러스터링을 수행하고 있습니다..."):
        clustering_data = load_clustering_data()
        
        if clustering_data is None:
            st.error("클러스터링 데이터를 불러올 수 없습니다.")
            return
        
        # 간단한 클러스터링 수행
        clustered_data = simple_clustering(clustering_data)
        cluster_analysis = analyze_simple_clusters(clustered_data)
        
        # 결과 표시
        st.markdown("### 🎯 클러스터링 결과")
        
        # 종합 점수 순위
        st.markdown("#### 🏆 지역별 종합 발전 점수 순위")
        fig_ranking = plot_cluster_ranking(clustered_data, cluster_analysis)
        st.pyplot(fig_ranking)
        
        # 클러스터별 비교
        st.markdown("#### 📊 클러스터별 특성 비교")
        fig_comparison = plot_simple_cluster_comparison(clustered_data, cluster_analysis)
        st.pyplot(fig_comparison)
        
        # 상세 정보
        display_simple_cluster_details(cluster_analysis)
        
        # 다운로드 버튼
        st.markdown("---")
        csv_data = clustered_data.to_csv(encoding='utf-8-sig')
        st.download_button(
            label="📥 클러스터링 결과 다운로드 (CSV)",
            data=csv_data,
            file_name="지역클러스터링결과.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    create_clustering_dashboard()