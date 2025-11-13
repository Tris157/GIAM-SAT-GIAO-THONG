import dotenv
from app.services.chat_services.tool_func import (
    get_frame_road,
    get_info_road,
    get_camera_live_frame,
    get_camera_live_detections
)
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from typing import List
from app.utils.chatbot_utils import pre_model_hook

class ChatResponse(BaseModel):
    text: str = Field(..., description="Phản hồi của trợ lý AI")
    image: List[str] = Field(default_factory=list, description="Danh sách URL hình ảnh")

prompt = """BẠN LÀ TRỢ LÝ AI TƯ VẤN GIAO THÔNG THÔNG MINH.
NHIỆM VỤ CHÍNH:
- Phân tích câu hỏi của người dùng để hiểu ý định cụ thể
- Nếu hỏi thông tin về tuyến đường nào đó thì buộc phải đưa đầy đủ thông tin về số lượng và tốc độ của oto lẫn xe máy
- Đưa ra lời khuyên và phân tích dựa trên dữ liệu giao thông
- Khi cần thiết, sử dụng tools để lấy thông tin và hình ảnh thực tế
- HỆ THỐNG CÓ CAMERA LIVE (camera_live) kết nối RTSP trực tiếp với phát hiện YOLO real-time
  + Khi người dùng hỏi về "camera live", "camera trực tiếp", "camera RTSP", hãy sử dụng get_camera_live_frame và get_camera_live_detections
  + Camera này hiển thị phát hiện xe ô tô và xe máy với bounding boxes
NGUYÊN TẮC PHÂN LOẠI:
   - Nhiều xe + vận tốc < 12 km/h → Ùn tắc
   - Nhiều xe + vận tốc 12-30 km/h → Đông
   - Vận tốc >= 30 km/h → Thông thoáng
   - Ít xe + vận tốc thấp → Chậm nhưng không tắc
KHI TRẢ LỜI:
- Luôn cung cấp thông tin chi tiết và chính xác
- Đưa ra lời khuyên cụ thể dựa trên dữ liệu thực tế, có thể hỏi vài câu quan tâm như là đi ăn, đi chơi, đi làm ...
- Khi người dùng hỏi về camera live, hãy mô tả số lượng xe được phát hiện và cung cấp hình ảnh
"""

dotenv.load_dotenv()

class ChatBotAgent:
    def __init__(self):
        self.prompt = prompt
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6)
        self.checkpointer = InMemorySaver()
        self.agent = create_react_agent(model= self.llm,
                                        tools= [get_frame_road, get_info_road, get_camera_live_frame, get_camera_live_detections],
                                        prompt= prompt,
                                        response_format= ChatResponse,
                                        pre_model_hook= pre_model_hook,
                                        checkpointer= self.checkpointer)
        self.config = {"configurable": {"thread_id": "1"}}

    
    def get_response(self, user_input: str) -> dict:
        """Lấy phản hồi từ Agent dựa trên đầu vào của người dùng.

        Args:
            user_input (str): Nội dung tin nhắn của người dùng.

        Returns:
            dict: Phản hồi từ Agent, bao gồm hình ảnh và văn bản.
        """
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            self.config
        )
        return response['structured_response'].model_dump()

if __name__ == "__main__":
    chat = ChatBotAgent()
    res = chat.get_response("cho tôi xin thông tin về Văn Phú và Văn Quán, cả ảnh nữa nhé")
    print(len(res['image']))
    print(res['text'])