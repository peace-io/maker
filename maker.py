import streamlit as st
import ssl  # 1. ssl 라이브러리 추가
from google import genai
from google.genai import types  # 2. types 추가

# 페이지 설정
st.set_page_config(
    page_title="Gemini 마케팅 메시지 추천기",
    page_icon="💬",
    layout="centered"
)

# 타이틀 및 서비스 소개
st.title("💬 Gemini 마케팅 메시지 & 발송 시점 추천기")
st.write("Google의 강력한 Gemini 3.5 Flash 모델을 활용해 맞춤형 마케팅 전략을 실시간으로 제안합니다.")
st.markdown("---")

# 사이드바에 API 키 입력창 생성
gemini_api_key = st.secrets["GEMINI_API_KEY"]

# 사용자 입력 받기
st.subheader("📋 정보를 입력해 주세요")

industry = st.text_input(
    "1. 업종을 입력하세요", 
    placeholder="예: 애견 미용실, 동네 책방, 필라테스 등"
)
purpose = st.text_input(
    "2. 메시지 발송 목적을 입력하세요", 
    placeholder="예: 비오는 날 깜짝 타임 세일, 주말 한정 10% 쿠폰"
)

# 추천 실행 버튼 및 결과 화면
st.markdown("---")
if st.button("🚀 Gemini 맞춤 추천 받기", use_container_width=True):
    # 유효성 검사
    if not gemini_api_key:
        st.warning("왼쪽 사이드바에 Gemini API Key를 입력해 주세요!")
    elif not industry or not purpose:
        st.warning("업종과 발송 목적을 모두 입력해 주세요!")
    else:
        # 로딩 스피너 작동
        with st.spinner("Gemini가 최적의 마케팅 전략을 고민하고 있습니다..."):
            try:
                # 3. 🛡️ SDK 내부 버그를 완벽하게 우회하는 커스텀 SSLContext 생성
                unverified_ssl_context = ssl.create_default_context()
                unverified_ssl_context.check_hostname = False
                unverified_ssl_context.verify_mode = ssl.CERT_NONE
                
                # 4. 클라이언트 생성 시 SSL 우회 옵션을 강제로 주입
                client = genai.Client(
                    api_key=gemini_api_key,
                    http_options=types.HttpOptions(
                        client_args={'verify': unverified_ssl_context},
                        async_client_args={'verify': unverified_ssl_context}
                    )
                )
                
                # 프롬프트 구성
                prompt = f"""
                너는 전문 카피라이터이자 빅데이터 기반 마케팅 전문가야.
                아래 조건에 맞는 [마케팅 메시지 템플릿]과 [가장 효과적인 발송 시점 및 이유]를 작성해줘.

                - 업종: {industry}
                - 발송 목적: {purpose}

                [출력 형식]
                ### 💬 추천 메시지 내용
                (여기에 실제 발송할 수 있는 매력적이고 가독성 좋은 문자 메시지 폼을 써줘. 이모지 적극 활용)

                ---
                ### ⏰ 추천 발송 시점 및 이유
                - **추천 요일/시간**: (예: 목요일 오후 3시)
                - **이유**: (왜 이 시간대가 효과적인지 소비자 심리나 행동 패턴을 분석해서 상세히 설명해줘)
                """

                # Gemini API 호출
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )
                
                # 결과를 화면에 렌더링
                result_text = response.text
                st.success("🎉 Gemini 추천이 완료되었습니다!")
                st.markdown(result_text)
                
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")