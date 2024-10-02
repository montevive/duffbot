from typing import List, Tuple
import os
import gradio as gr
import requests


API_URL = os.getenv("API_URL", "http://localhost:8000")

current_dir = os.path.dirname(os.path.abspath(__file__))


def chatbot(message: str, history: List[Tuple[str, str]]) -> str:
    flattened_history = [msg for pair in history for msg in pair]
    messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": msg} 
                for i, msg in enumerate(flattened_history)]
    messages.append({"role": "user", "content": message})
    
    response = requests.post(f"{API_URL}/api/chat/", json={"history_messages": messages})
    
    if response.status_code == 200:
        return response.json()["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


with gr.Blocks(title="Duffbot") as demo:
    gr.Markdown("# Duffbot: AI Tool Preference Collector")
    gr.Image(os.path.join(current_dir, "duffbot_logo.webp"), show_label=False)
    with gr.Tab("Chatbot"):
        gr.ChatInterface(
            chatbot,
            chatbot=gr.Chatbot(height=300, placeholder="Hola! ¿Cuál es para ti la mejor app de IA que te ayuda a ser más productivo/a en tu día a día?"),
            textbox=gr.Textbox(placeholder="Escribe tu mensaje aquí...", container=False, scale=7),
            title="Chatbot de IA",
            description="Cuentame cual es tu app de IA favorita para ser más productivo/a (...además de ChatGPT)"
        )
    
    

demo.launch(server_name="0.0.0.0", server_port=8001)
