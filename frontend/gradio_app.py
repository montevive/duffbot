from typing import List, Tuple
import os
import gradio as gr
import requests


API_URL = os.getenv("API_URL", "http://localhost:8000")

current_dir = os.path.dirname(os.path.abspath(__file__))

# def submit_preference(tool_name, category, rating):
#     response = requests.post(f"{API_URL}/preferences/", json={
#         "tool_name": tool_name,
#         "category": category,
#         "rating": float(rating)
#     })
#     if response.status_code == 200:
#         return f"Preference for {tool_name} submitted successfully!"
#     else:
#         return f"Error submitting preference: {response.text}"

# def get_scoreboard():
#     response = requests.get(f"{API_URL}/scoreboard/")
#     if response.status_code == 200:
#         top_tools = response.json()["top_tools"]
#         return "\n".join([f"{tool}: {rating:.2f}" for tool, rating in top_tools])
#     else:
#         return f"Error fetching scoreboard: {response.text}"

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
    # with gr.Tab("Submit Preference"):
    #     tool_name = gr.Textbox(label="AI Tool Name")
    #     category = gr.Dropdown(["Productivity", "Coding", "Design", "Other"], label="Category")
    #     rating = gr.Slider(minimum=1, maximum=5, step=0.1, label="Rating")
    #     submit_btn = gr.Button("Submit")
    #     result = gr.Textbox(label="Result")
        
    #     submit_btn.click(submit_preference, inputs=[tool_name, category, rating], outputs=result)
    
    # with gr.Tab("View Scoreboard"):
    #     scoreboard_btn = gr.Button("Refresh Scoreboard")
    #     scoreboard = gr.Textbox(label="Top AI Tools")
        
    #     scoreboard_btn.click(get_scoreboard, inputs=[], outputs=scoreboard)
    
    

demo.launch(server_name="0.0.0.0", server_port=8001)
