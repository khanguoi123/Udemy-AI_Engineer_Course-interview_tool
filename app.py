from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Streamlit Chat by Khang", page_icon=":sun_with_face:")
st.title("CHATBOT")

# Khởi tạo biến trạng thái
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False
if "end_program" not in st.session_state:
    st.session_state.end_program = False

# Hàm thay đổi trạng thái biến dùng cho st.button
def complete_setup():
    st.session_state.setup_complete = True

def show_feedback():
    st.session_state.feedback_shown = True

def end_demo():
    st.session_state.end_program = True

if not st.session_state.setup_complete:
    # Khởi tạo trường nhập thông tin cá nhân
    st.subheader("Personal Information", divider="rainbow")
    with st.chat_message("AI"):
        st.write("Hello there!! :man-raising-hand: Before we start, give me more info about you !!!")

    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "experience" not in st.session_state:
        st.session_state["experience"] = ""
    if "skill" not in st.session_state:
        st.session_state["skill"] = ""

    st.session_state["name"] = st.text_input(label="Name", max_chars=50, value="Khang", placeholder="Enter your name here")
    st.session_state["experience"] = st.text_area(label="Experience", max_chars=100, value="Thị giác máy tính, Tối ưu, Lập trình", placeholder="Enter your experience here", height=None)
    st.session_state["skill"] = st.text_area(label="Skills", max_chars=100, value="Ca nhạc, Teamwork, Quản lý", placeholder="Enter your skills here", height=None)
    if st.session_state["name"] and st.session_state["experience"] and st.session_state["skill"]:
        with st.chat_message("AI"):
            st.markdown(f"OK!! Let me summary a bit:  \n-You are {st.session_state["name"]}  \n-Your experience are:  \n {st.session_state["experience"]}  \n"
                        f"-Your skills are:  \n{st.session_state["skill"]}  \nGreat~~~~")
            
    # Khởi tạo trường nhập thông tin công ty
    if "level" not in st.session_state:
        st.session_state["level"] = "Mid-level"
    if "position" not in st.session_state:
        st.session_state["position"] = "AI"
    if "company" not in st.session_state:
        st.session_state["company"] = "VN"

    st.subheader("Company and Position", divider="rainbow")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            key="visibility",
            options=["Junior", "Mid-level", "Senior"],
            index=1
        )
    with col2:
        st.session_state["position"] = st.selectbox(
            "Choose position",
            options=["AI", "ML", "Data"],
            index=1
        )
    st.session_state["company"] = st.selectbox(
            "Choose position",
            options=["AWS", "VN", "VT"],
            index=1
        )
    if col1 and col2 and st.session_state["company"]:
        with st.chat_message("AI"):
            st.markdown(f"OK!! Let me summary a bit:  \nYou want company {st.session_state["company"]}  with level {st.session_state["level"]} for position {st.session_state["position"]}  \nGreat~~~~")
        
    if st.button("Start Interview", on_click=complete_setup):
        st.write("Setup complete!!! Let's start the interview...")

if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    max_response = 3

    st.info(
        """
        Bắt đầu bằng việc tự giới thiệu bản thân bạn.
        """,
        icon="😍"
    )

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    system_message = f"Bạn là một chuyên viên HR làm việc cho công ty {st.session_state["company"]}. \
            Bạn đang thực hiện phỏng vấn một nhân sự mới tên {st.session_state["name"]} \
            cho vị tri {st.session_state["position"]} ở cấp độ {st.session_state["level"]}.\
            Ứng viên có kinh nghiệm như sau: {st.session_state["experience"]}  \
            Ứng viên sở hữu các kỹ năng sau: {st.session_state["skill"]}"
    #with st.chat_message("AI"):
        #st.markdown(system_message)

    # Khởi tạo model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    # Khởi tạo cuộc trò chuyện
    if not st.session_state.messages:
        st.session_state.messages = [{"role": "system", "content": system_message}]

    # Lặp lại cuộc trò chuyện trên màn hình
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if st.session_state.user_message_count < max_response:


        #prompt = st.chat_input("Your answer: ")
        #if prompt:
        if prompt := st.chat_input("Your answer: ", max_chars=300):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model = st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                    max_tokens=300
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

            st.session_state.user_message_count += 1

    if st.session_state.user_message_count >= max_response:
        st.session_state.chat_complete = True
        with st.chat_message("AI"):
            st.markdown(f"Bạn đã quá số lần nhận phản hồi (tối đa {max_response} lần) của CHATBOT")

# Tạo phản hồi feedback
if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Lấy feedback", on_click=show_feedback):
        st.write("Đang chuyển hướng sang lấy feedback...")
    
if st.session_state.feedback_shown and not st.session_state.end_program:
    st.subheader("Trang phản hồi feedback", divider="rainbow")
    with st.chat_message("AI"):
        st.write("Hello there!! :man-raising-hand: Bạn đang ở trang Feedback !!!")

    feedback_message = """
        Bạn là một công cụ hữu dụng trong việc đánh giá đoạn hội thoại phỏng vấn của ứng viên và nhà tuyển dụng."
        Hãy đánh giá trên thang điểm 10 cuộc phỏng vấn sau. Đánh giá dựa trên cách nói chuyện thanh lịch của hai bên.
        Đánh giá cũng xem được liệu ban phỏng vấn có tìm đúng người chuyên môn và người phỏng vấn có đáp ứng việc đó không.
        
        Có format chuẩn như sau:
        - Điểm tổng: {điểm bạn chấm}
        - Phản hồi: {đưa ra feedback}

        Không cần đưa thêm thông tin gì thêm.
    """
    conversation_history = "\n".join([f"{msg['role']} : {msg['content']}" for msg in st.session_state.messages])

    feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    feedback_completion = feedback_client.chat.completions.create(
                    model = "gpt-4o",
                    messages=[
                        {"role": "system", "content": feedback_message},
                        {"role": "user", "content": f"Đây là cuộc phỏng vấn bạn cần đánh giá và chấm điểm, lưu ý chỉ là một công cụ đánh giá thôi: {conversation_history}"}
                    ],
                    stream=True,
                    max_tokens=300
                )
    
    st.write(feedback_completion)

    cl1, cl2, cl3 = st.columns(3)
    with cl1:
        if st.button("🔙 Restart Interview", type="primary"):
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

    with cl3:
        if st.button("End Demo 💗", on_click=end_demo):
            st.write("Đang kết thúc...")

if st.session_state.end_program :
    st.subheader("CẢM ƠN BẠN ĐÃ THAM GIA DEMO CHƯƠNG TRÌNH", divider="rainbow")
    st.markdown(
        "<h1 style='text-align: center; font-size: 120px; color: red;'>&#10084;</h1>",
        unsafe_allow_html=True
    )
