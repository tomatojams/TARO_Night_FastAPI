from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

import os
from dotenv import load_dotenv

memory_key = "chat_history"
input_key = "input"
output_key = "out_text"

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
    temperature=1,
    max_tokens=500,
)
memory = ConversationBufferMemory(
    memory_key=memory_key, input_key=input_key, output_key=output_key
)

