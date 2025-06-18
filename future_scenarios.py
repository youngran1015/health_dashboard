import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def load_future_data():
    """미래 예측을 위한 시계열 데이터 로드"""
    try:
        # 사회경제 데이터 (2020-2024)
        income_data = pd.read_csv('data/socioeconomic/소득_2020_2024.csv').set_index('년도')
        education_data = pd.read_csv('data/socioeconomic/교육수준_2020_2024.csv').set_index('년도')
        employment_data = pd.read_csv('data/socioeconomic/고용률_2020_2024.csv').set_index('년도')
        
        # 의료 접근성 데이터
        hospitals_data = pd.read_csv('data/health_accessibility/hospitals_2020_2024.csv').set_index('지역')
        doctors_data = pd.read_csv('data/health_accessibility/doctors_2020_2024.csv').set_index('지역')
        
        return {
            'income': income_data,
            'education': education_data,
            'employment': employment_data,
            'hospitals': hospitals_data,
            'doctors': doctors_data
        }
        
    except Exception as e:
        st.error(f"미래 예측 데이터 로딩 오류: {str(e)}")
        return None

def predict_trends(data, target_year=2030):
    """선형 회귀를 이용한 트렌드 예측"""
    
    predictions = {}
    
    for category, df in data.items():
        predictions[category] = {}
        
        # 연도 데이터 (2020-2024)
        if category in ['hospitals', 'doctors']:
            years = np.array([2020, 2021, 2022, 2023, 2024]).reshape(-1, 1)
            year_cols = ['2020', '2021', '2022', '2023', '2024']
        else:
            years = df.index.values.reshape(-1, 1)
            year_cols = df.index
        
        # 각 지역별 예측
        for region in df.columns:
            if category in ['hospitals', 'doctors']:
                values = df.loc[:, region].values
            else:
                values = df[region].values
            
            # 선형 회귀 모델
            model = LinearRegression()
            model.fit(years, values)
            
            # 미래 예측
            future_years = np.array(range(2025, target_year + 1)).reshape(-1, 1)
            future_pred = model.predict(future_years)
            
            # 과거 데이터와 미래 예측 결합
            all_years = np.concatenate([years.flatten(), future_years.flatten()])
            all_values = np.concatenate([values, future_pred])
            
            predictions[category][region] = {
                'years': all_years,
                'values': all_values,
                'historical': values,
                'predicted': future_pred,
                'growth_rate': model.coef_[0],  # 연간 증가율
                'r2_score': model.score(years, values)  # 모델 정확도
            }
    
    return predictions

def create_scenario_analysis(predictions, scenario_type='current'):
    """시나리오별 분석"""
    
    scenarios = {
        'current': {'name': '현재 추세 지속', 'multiplier': 1.0, 'description': '현재 트렌드가 그대로 지속되는 경우'},
        'optimistic': {'name': '정책 개입 성공', 'multiplier': 0.7, 'description': '효과적인 정책으로 격차가 30% 감소하는 경우'},
        'pessimistic': {'name': '격차 심화', 'multiplier': 1.3, 'description': '현재보다 격차가 30% 더 벌어지는 경우'}
    }
    
    scenario_data = {}
    
    for category, regions in predictions.items():
        scenario_data[category] = {}
        
        # 2030년 예측값 추출
        for region, pred_data in regions.items():
            pred_2030 = pred_data['predicted'][-1]  # 2030년 예측값
            current_2024 = pred_data['historical'][-1]  # 2024년 실제값
            
            if scenario_type == 'current':
                adjusted_value = pred_2030
            elif scenario_type == 'optimistic':
                # 서울과의 격차를 줄이는 방향으로 조정
                seoul_2030 = regions['서울']['predicted'][-1]
                gap = seoul_2030 - pred_2030
                adjusted_value = pred_2030 + (gap * 0.3)  # 격차 30% 감소
            else:  # pessimistic
                # 격차가 더 벌어지는 방향으로 조정
                seoul_2030 = regions['서울']['predicted'][-1]
                gap = seoul_2030 - pred_2030
                adjusted_value = pred_2030 - (gap * 0.3)  # 격차 30% 증가
            
            scenario_data[category][region] = {
                'current_2024': current_2024,
                'predicted_2030': adjusted_value,
                'change_rate': ((adjusted_value - current_2024) / current_2024) * 100
            }
    
    return scenario_data, scenarios[scenario_type]

def calculate_inequality_gap_2030(scenario_data):
    """2030년 예상 불평등 격차 계산"""
    
    gaps_2030 = {}
    
    for category, regions in scenario_data.items():
        seoul_value = regions['서울']['predicted_2030']
        
        # 각 지역의 서울 대비 비율 계산
        gaps_2030[category] = {}
        for region, data in regions.items():
            ratio = (data['predicted_2030'] / seoul_value) * 100
            gaps_2030[category][region] = ratio
    
    return gaps_2030

def plot_trend_predictions(predictions, selected_regions=['서울', '부산', '대구', '경기', '제주']):
    """트렌드 예측 시각화"""
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    axes = axes.flatten()
    
    categories = ['income', 'education', 'employment', 'hospitals', 'doctors']
    titles = ['소득 추이', '교육수준 추이', '고용률 추이', '병원 수 추이', '의사 수 추이']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for idx, (category, title) in enumerate(zip(categories, titles)):
        ax = axes[idx]
        
        for i, region in enumerate(selected_regions):
            pred_data = predictions[category][region]
            years = pred_data['years']
            values = pred_data['values']
            
            # 전체 라인 (연한 색)
            ax.plot(years, values, '--', alpha=0.7, color=colors[i], label=f'{region}')
            
            # 역사적 데이터 (진한 색)
            historical_years = years[:5]  # 2020-2024
            historical_values = values[:5]
            ax.plot(historical_years, historical_values, '-', linewidth=3, 
                   color=colors[i], marker='o', markersize=6)
            
            # 예측 구간 표시
            ax.axvline(x=2024.5, color='red', linestyle=':', alpha=0.7)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('연도', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8, loc='upper left')
        
        # 예측 구간 음영
        ax.axvspan(2024.5, 2030, alpha=0.1, color='gray', label='예측구간')
    
    # 마지막 subplot 제거
    fig.delaxes(axes[5])
    
    plt.tight_layout()
    return fig

def plot_scenario_comparison(scenario_results):
    """시나리오 비교 차트"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    scenarios = ['current', 'optimistic', 'pessimistic']
    scenario_names = ['현재 추세 지속', '정책 개입 성공', '격차 심화']
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    categories = ['income', 'education', 'hospitals', 'doctors']
    category_names = ['소득', '교육수준', '병원 수', '의사 수']
    
    for idx, (category, cat_name) in enumerate(zip(categories, category_names)):
        ax = axes[idx]
        
        # 지역별 2030년 예측값 비교
        regions = ['서울', '부산', '대구', '인천', '광주', '대전', '제주']
        
        x = np.arange(len(regions))
        width = 0.25
        
        for i, (scenario, s_name, color) in enumerate(zip(scenarios, scenario_names, colors)):
            values = []
            for region in regions:
                values.append(scenario_results[scenario][category][region]['predicted_2030'])
            
            ax.bar(x + i*width, values, width, label=s_name, color=color, alpha=0.8)
        
        ax.set_title(f'2030년 {cat_name} 예측 비교', fontsize=14, fontweight='bold')
        ax.set_xlabel('지역', fontsize=10)
        ax.set_xticks(x + width)
        ax.set_xticklabels(regions, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

def plot_inequality_gap_evolution(predictions):
    """불평등 격차 변화 추이"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    axes = axes.flatten()
    
    categories = ['income', 'education', 'hospitals', 'doctors']
    category_names = ['소득 격차', '교육 격차', '병원 수 격차', '의사 수 격차']
    
    # 대표 지역들
    comparison_regions = ['부산', '대구', '광주', '강원', '제주']
    colors = ['#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#34495e']
    
    for idx, (category, cat_name) in enumerate(zip(categories, category_names)):
        ax = axes[idx]
        
        # 서울 대비 비율 계산 (2020-2030)
        seoul_data = predictions[category]['서울']
        years = seoul_data['years']
        seoul_values = seoul_data['values']
        
        for i, region in enumerate(comparison_regions):
            region_data = predictions[category][region]
            region_values = region_data['values']
            
            # 서울 대비 비율 (백분율)
            ratios = (region_values / seoul_values) * 100
            
            ax.plot(years, ratios, '-', linewidth=2, marker='o', 
                   color=colors[i], label=region, markersize=4)
        
        # 2024년 기준선
        ax.axvline(x=2024.5, color='red', linestyle=':', alpha=0.7, label='예측 시작')
        ax.axhline(y=100, color='black', linestyle='--', alpha=0.5, label='서울 기준선')
        
        ax.set_title(f'{cat_name} 변화 추이 (서울=100 기준)', fontsize=12, fontweight='bold')
        ax.set_xlabel('연도', fontsize=10)
        ax.set_ylabel('서울 대비 비율 (%)', fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        
        # 예측 구간 음영
        ax.axvspan(2024.5, 2030, alpha=0.1, color='gray')
    
    plt.tight_layout()
    return fig

def plot_regional_development_index(scenario_results):
    """지역 발전 종합 지수 (2030년 예측)"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    scenarios = ['current', 'optimistic', 'pessimistic']
    scenario_names = ['현재 추세', '정책 개입', '격차 심화']
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    # 종합 발전 지수 계산 (소득 + 교육 + 의료 인프라)
    regions = list(scenario_results['current']['income'].keys())
    
    for i, (scenario, s_name, color) in enumerate(zip(scenarios, scenario_names, colors)):
        development_indices = []
        
        for region in regions:
            # 서울 대비 비율로 정규화
            income_ratio = scenario_results[scenario]['income'][region]['predicted_2030'] / scenario_results[scenario]['income']['서울']['predicted_2030']
            education_ratio = scenario_results[scenario]['education'][region]['predicted_2030'] / scenario_results[scenario]['education']['서울']['predicted_2030']
            hospital_ratio = scenario_results[scenario]['hospitals'][region]['predicted_2030'] / scenario_results[scenario]['hospitals']['서울']['predicted_2030']
            doctor_ratio = scenario_results[scenario]['doctors'][region]['predicted_2030'] / scenario_results[scenario]['doctors']['서울']['predicted_2030']
            
            # 가중평균 (소득 40%, 교육 20%, 병원 20%, 의사 20%)
            dev_index = (income_ratio * 0.4 + education_ratio * 0.2 + 
                        hospital_ratio * 0.2 + doctor_ratio * 0.2) * 100
            development_indices.append(dev_index)
        
        x = np.arange(len(regions))
        width = 0.25
        
        ax.bar(x + i*width, development_indices, width, label=s_name, 
               color=color, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # 서울 기준선
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='서울 기준선')
    
    ax.set_title('2030년 지역 발전 종합 지수 예측 (서울=100 기준)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('지역', fontsize=12, fontweight='bold')
    ax.set_ylabel('종합 발전 지수', fontsize=12, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(regions, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

def display_scenario_insights(scenario_results):
    """시나리오별 주요 인사이트 표시"""
    
    st.markdown("### 💡 2030년 시나리오별 주요 인사이트")
    
    # 3개 시나리오 탭
    tab1, tab2, tab3 = st.tabs(["📈 현재 추세 지속", "✅ 정책 개입 성공", "⚠️ 격차 심화"])
    
    with tab1:
        st.markdown("#### 📈 현재 추세 지속 시나리오")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **🎯 예상 결과**
            • 서울-지방 간 격차가 현재 수준으로 유지
            • 의료 인프라는 점진적으로 개선
            • 전반적인 생활 수준 향상
            """)
        
        with col2:
            st.warning("""
            **⚠️ 주의사항**
            • 근본적인 격차 해소는 어려움
            • 청년층 수도권 집중 지속
            • 농어촌 지역 의료 접근성 한계
            """)
    
    with tab2:
        st.markdown("#### ✅ 정책 개입 성공 시나리오")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **🎯 정책 효과**
            • 지역 간 소득 격차 30% 감소
            • 의료 인프라 균등 배치
            • 지방 대학 경쟁력 강화
            • 청년 인구 지방 정착 증가
            """)
        
        with col2:
            st.info("""
            **📋 필요한 정책**
            • 지역균형발전 특별법 강화
            • 의료진 지방 근무 인센티브
            • 지역 혁신도시 확대
            • 원격의료 인프라 구축
            """)
    
    with tab3:
        st.markdown("#### ⚠️ 격차 심화 시나리오")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("""
            **🚨 우려사항**
            • 수도권-지방 격차 30% 확대
            • 지방 소멸 가속화
            • 의료 사각지대 확산
            • 사회적 갈등 증가
            """)
        
        with col2:
            st.warning("""
            **📉 예상 영향**
            • 청년층 대규모 유출
            • 고령화 심화
            • 지역경제 침체
            • 건강 불평등 고착화
            """)

def create_future_dashboard():
    """미래 시나리오 대시보드 메인 함수"""
    st.header("🔮 미래 예측 시나리오")
    st.markdown("**2030년 건강 불평등 변화를 3가지 시나리오로 예측합니다.**")
    
    # 데이터 로드 및 예측
    with st.spinner("미래 시나리오를 분석하고 있습니다..."):
        future_data = load_future_data()
        
        if future_data is None:
            st.error("미래 예측 데이터를 불러올 수 없습니다.")
            return
        
        # 트렌드 예측
        predictions = predict_trends(future_data, 2030)
        
        # 시나리오별 분석
        scenario_current, _ = create_scenario_analysis(predictions, 'current')
        scenario_optimistic, _ = create_scenario_analysis(predictions, 'optimistic')
        scenario_pessimistic, _ = create_scenario_analysis(predictions, 'pessimistic')
        
        scenario_results = {
            'current': scenario_current,
            'optimistic': scenario_optimistic,
            'pessimistic': scenario_pessimistic
        }
        
        # 결과 표시
        st.markdown("### 📊 트렌드 예측 분석")
        
        # 지역 선택
        regions = list(predictions['income'].keys())
        selected_regions = st.multiselect(
            "분석할 지역 선택 (최대 5개)",
            regions,
            default=['서울', '부산', '대구', '경기', '제주']
        )
        
        if len(selected_regions) > 5:
            st.warning("최대 5개 지역까지 선택 가능합니다.")
            selected_regions = selected_regions[:5]
        
        # 트렌드 예측 차트
        st.markdown("#### 📈 2020-2030년 변화 추이 예측")
        fig_trends = plot_trend_predictions(predictions, selected_regions)
        st.pyplot(fig_trends)
        
        # 시나리오 비교
        st.markdown("#### 🎯 2030년 시나리오별 비교")
        fig_scenarios = plot_scenario_comparison(scenario_results)
        st.pyplot(fig_scenarios)
        
        # 불평등 격차 변화
        st.markdown("#### ⚖️ 불평등 격차 변화 추이")
        fig_inequality = plot_inequality_gap_evolution(predictions)
        st.pyplot(fig_inequality)
        
        # 종합 발전 지수
        st.markdown("#### 🏆 2030년 지역 발전 종합 지수")
        fig_development = plot_regional_development_index(scenario_results)
        st.pyplot(fig_development)
        
        # 시나리오별 인사이트
        display_scenario_insights(scenario_results)
        
        # 주요 통계 요약
        st.markdown("---")
        st.markdown("### 📋 2030년 예측 요약")
        
        col1, col2, col3 = st.columns(3)
        
        # 현재 추세에서 가장 개선될 지역
        income_changes = {region: data['change_rate'] for region, data in scenario_current['income'].items()}
        best_region = max(income_changes.items(), key=lambda x: x[1])
        
        with col1:
            st.metric("가장 개선될 지역", best_region[0], f"+{best_region[1]:.1f}%")
        
        # 격차가 가장 클 것으로 예상되는 영역
        seoul_income_2030 = scenario_current['income']['서울']['predicted_2030']
        jeju_income_2030 = scenario_current['income']['제주']['predicted_2030']
        income_gap_2030 = ((seoul_income_2030 - jeju_income_2030) / jeju_income_2030) * 100
        
        with col2:
            st.metric("서울-제주 소득격차", f"{income_gap_2030:.1f}%", "2030년 예상")
        
        # 정책 개입 효과
        policy_effect = abs(scenario_optimistic['income']['제주']['predicted_2030'] - 
                          scenario_current['income']['제주']['predicted_2030'])
        
        with col3:
            st.metric("정책 개입 효과", f"+{policy_effect:.0f}만원", "제주 소득 개선")
        
        # 다운로드 버튼
        st.markdown("---")
        
        # 예측 결과를 DataFrame으로 변환
        results_list = []
        for region in regions:
            results_list.append({
                '지역': region,
                '2024_소득': scenario_current['income'][region]['current_2024'],
                '2030_소득_현재추세': scenario_current['income'][region]['predicted_2030'],
                '2030_소득_정책개입': scenario_optimistic['income'][region]['predicted_2030'],
                '2030_소득_격차심화': scenario_pessimistic['income'][region]['predicted_2030'],
                '소득증가율_현재추세': scenario_current['income'][region]['change_rate'],
                '2024_병원수': scenario_current['hospitals'][region]['current_2024'],
                '2030_병원수_예측': scenario_current['hospitals'][region]['predicted_2030']
            })
        
        results_df = pd.DataFrame(results_list)
        csv_results = results_df.to_csv(index=False, encoding='utf-8-sig')
        
        st.download_button(
            label="📥 2030년 예측 결과 다운로드 (CSV)",
            data=csv_results,
            file_name="2030년_건강불평등_예측결과.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    create_future_dashboard()