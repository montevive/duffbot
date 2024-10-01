

from llama_index.llms.openai import OpenAI
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import FunctionTool
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from .tool import web_search_brave, register_tool
from config.settings import TRACE_AI


if TRACE_AI:
    import phoenix as px
    px.launch_app()
    llama_index.core.set_global_handler("arize_phoenix")

llm = OpenAI(model="gpt-4o", temperature=0)

# Create FunctionTools
web_search_tool = FunctionTool.from_defaults(
    fn=web_search_brave,
    async_fn=web_search_brave,
    name="web_search",
    description="Searches the web for information about AI tools, used to verify tool names or find general information"
)

register_tool_func = FunctionTool.from_defaults(
    fn=register_tool,
    async_fn=register_tool,
    name="register_tool",
    description="Registers an AI tool with its name, reason for user preference, and optional website"
)

# Create the OpenAIAgent with both tools
system_prompt = """Eres un asistente IA cuyo objetivo es conocer cual es la utilidad IA preferida del usuario. 
    Una vez sepas el nombre de la utilidad, el porqué es la opción preferida del usuario y la página web de la utilidad 
    (si la ha proporcionado la primera vez, sino búscala tu), debes usar la tool "register_tool" para registrar la información y terminar con la conversación.
    Consideraciones:
    - utiliza la tool "web_search" para buscar la utilidad, obtener su nombre oficial y descripción
    - responde en castellano"""

agent = OpenAIAgent.from_tools([web_search_tool, register_tool_func], llm=llm, verbose=True, system_prompt=system_prompt)

async def chat(latest_message: str, chat_history: list[ChatMessage]) -> str:
    response = await agent.achat(latest_message, chat_history=chat_history)
    return str(response)
