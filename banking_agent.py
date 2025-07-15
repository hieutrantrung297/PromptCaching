import os
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from prompt_caching import retrieve_from_cache, store_response

# Tải cấu hình từ tệp .env
load_dotenv()


def _unwrap_output(result_obj) -> str:
    """Trích xuất văn bản thuần từ kết quả trả về của Crew."""
    return str(getattr(result_obj, "raw_output", getattr(result_obj, "output", result_obj)))

class BankingAgent:
    def __init__(self):
        self.model_name = "gpt-4.1-nano"
        self.temperature_setting = 0.7
        self.api_key = os.getenv("MODEL_API_KEY")

        if not self.api_key:
            raise RuntimeError("Thiếu MODEL_API_KEY trong tệp cấu hình môi trường.")

        # Khởi tạo Agent và Crew
        self.agent = self._build_llm_agent()
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self._build_task()],
            verbose=True
        )

    def _build_llm_agent(self) -> Agent:
        llm_instance = LLM(
            model=self.model_name,
            temperature=self.temperature_setting,
            api_key=self.api_key
        )
        return Agent(
            role="Chuyên gia ngân hàng",
            goal="Biến các khái niệm ngân hàng phức tạp thành điều dễ hiểu và thú vị cho mọi người",
            backstory="Bạn là chuyên gia trong lĩnh vực ngân hàng, có khả năng giải thích những kiến thức khó theo cách đơn giản, dễ hiểu và gần gũi.",
            llm=llm_instance,
            verbose=True
        )

    def _build_task(self) -> Task:
        return Task(
            description="Chuyển câu hỏi sau: {question}, thành câu trả lời dễ hiểu, dành cho người không rành về khái niệm ngân hàng.",
            expected_output="Sử dụng từ ngữ cơ bản, ví dụ minh họa và giọng điệu vui vẻ để giải thích rõ ràng.",
            agent=self.agent
        )

    def explain(self, input_question: str) -> tuple[str, dict]:
        # Kiểm tra bộ nhớ đệm trước
        hit = retrieve_from_cache(input_question)
        if hit:
            return hit["response"], {
                "cached": True,
                "model_used": self.model_name,
                "temperature": self.temperature_setting,
                "timestamp": hit.get("timestamp")
            }

        outcome = self.crew.kickoff(inputs={"question": input_question})
        answer_text = _unwrap_output(outcome)

        response_meta = {
            "cached": False,
            "model_used": self.model_name,
            "temperature": self.temperature_setting,
            "timestamp": datetime.utcnow().isoformat()
        }

        store_response(input_question, answer_text, response_meta)

        return answer_text, response_meta
