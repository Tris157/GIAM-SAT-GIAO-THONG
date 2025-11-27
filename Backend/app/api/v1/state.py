# LAZY IMPORT: Không import ở module level để tránh blocking khi import state
# Chỉ import khi thật sự cần (bên trong function)

# Global state variables - Khởi tạo lazy để tránh block khi import
analyzer = None
agent = None

def init_analyzer():
    """
    Khởi tạo analyzer - gọi từ startup event
    Không khởi tạo ngay khi import để tránh block server
    """
    global analyzer, agent

    if analyzer is None:
        # LAZY IMPORT: Import chỉ khi cần, không block khi import module state
        from app.services.road_services.AnalyzeOnRoadForMultiProcessing import AnalyzeOnRoadForMultiprocessing

        print("⏳ Đang khởi tạo Analyzer (YOLO model)...")
        analyzer = AnalyzeOnRoadForMultiprocessing(show=False,
                                                   show_log=False,
                                                   is_join_processes=False)
        print("⏳ Đang khởi động các process phân tích video...")
        analyzer.run_multiprocessing()
        print("✅ Analyzer đã sẵn sàng!")

    if agent is None:
        # LAZY IMPORT: Import chỉ khi cần
        from app.services.chat_services.ChatBotAgent import ChatBotAgent

        print("⏳ Đang khởi tạo ChatBot Agent...")
        agent = ChatBotAgent()
        print("✅ ChatBot Agent đã sẵn sàng!")

