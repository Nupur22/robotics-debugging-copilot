import gradio as gr
import chromadb
import os
import time

# 1. Connect to our Vector Brain
db_path = os.path.join(os.getcwd(), "data/chroma_db")
client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection(name="robot_failures")

def robotics_copilot(user_query):
    # 2. Search for the relevant logs (RAG)
    results = collection.query(
        query_texts=[user_query],
        n_results=1
    )
    
    # Get the best match data
    log_text = results['documents'][0][0]
    fix_suggestion = results['metadatas'][0][0]['fix']
    
    # 3. Simulate Claude's thinking process (Mock AI)
    # In a real setup, we would send 'log_text' to Claude here.
    time.sleep(1) # Simulates network delay
    
    ai_response = f"""
### Analysis:
I analyzed the logs and found a matching issue in the system history.

**Detected Node:** {log_text.split('|')[0]}
**Observed Error:** {log_text.split('|')[1]}

**Diagnosis & Recommended Fix:**
{fix_suggestion}

*Note: This is a diagnostic based on historical ROS 2 data. Please check your TF tree or sensor hardware if the error persists.*
    """
    return ai_response

# 4. Create a professional Web UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Robotics Debugging Copilot")
    gr.Markdown("Describe what your TurtleBot is doing (or failing to do) below.")
    
    with gr.Row():
        input_text = gr.Textbox(label="Robot Behavior / Error Message", placeholder="e.g. The robot keeps hitting walls...")
    
    submit_btn = gr.Button("Analyze Failure", variant="primary")
    output_text = gr.Markdown(label="AI Analysis")
    
    submit_btn.click(fn=robotics_copilot, inputs=input_text, outputs=output_text)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
