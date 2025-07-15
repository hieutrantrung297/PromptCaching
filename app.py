import streamlit as st
from banking_agent import BankingAgent
from datetime import datetime
import json
import pandas as pd
from prompt_caching import purge_cache

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Kiến thức Ngân Hàng Cơ Bản",
    page_icon="📚",
    layout="wide"
)

# Khởi tạo trạng thái phiên cho dữ liệu
if 'agent' not in st.session_state:
    st.session_state.agent = BankingAgent()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def format_timestamp(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def main():
    # Thanh bên
    with st.sidebar:
        st.title("📚 Kiến thức Ngân Hàng Cơ Bản")
        st.markdown("Hỏi bất kỳ câu gì và nhận câu trả lời đơn giản, dễ hiểu!")

        # Các nút điều khiển
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Xoá cuộc trò chuyện"):
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            if st.button("🗑️ Xoá bộ nhớ đệm"):
                purge_cache()
                st.success("Đã xoá bộ nhớ đệm!")
                st.rerun()
    # Khu vực chính
    st.title("Đặt câu hỏi của bạn")

    # Biểu mẫu nhập câu hỏi
    with st.form("question_form", clear_on_submit=True):
        user_input = st.text_input("Bạn muốn hiểu điều gì?", key="user_input")
        submitted = st.form_submit_button("Hỏi luôn")

        if submitted and user_input:
            # Nhận phản hồi từ tác tử
            response, metadata = st.session_state.agent.explain(user_input)

            # Thêm vào lịch sử trò chuyện
            st.session_state.chat_history.append({
                "question": user_input,
                "response": response,
                "metadata": metadata
            })

            # Tải lại để hiển thị
            st.rerun()

    # Hiển thị lịch sử trò chuyện
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            # Thẻ trò chuyện hiển thị câu hỏi và trả lời
            st.markdown('<div class="chat-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question">🧑 {chat["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="response">🤖 {chat["response"]}</div>', unsafe_allow_html=True)

            # Hiển thị thông tin metadata
            if chat['metadata'].get('cached', False):
                st.info(f"💾 Lấy từ bộ nhớ đệm ({format_timestamp(chat['metadata']['timestamp'])})")
            else:
                st.success(f"🤖 Tạo bởi mô hình {chat['metadata']['model_used']} (nhiệt: {chat['metadata']['temperature']})")

            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
