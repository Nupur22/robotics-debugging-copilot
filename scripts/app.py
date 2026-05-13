import os
import chromadb
import google.generativeai as genai
import gradio as gr

# 1. Configuration & AI Setup
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

class CopilotApp:
    def __init__(self):
        # Setup Vector DB (ChromaDB)
        # Assumes your data is in ../data/chroma_db relative to the scripts folder
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db"))
        self.client_db = chromadb.PersistentClient(path=db_path)
        
        try:
            self.collection = self.client_db.get_collection(name="robot_logs")
        except Exception:
            print("Error: Collection 'robot_logs' not found. Did you run indexer.py?")
            self.collection = None

    def get_ai_diagnostic(self, error_msg):
        if not self.collection:
            return "Database not initialized. Please run indexer.py first."

        # A. Search ChromaDB for relevant robot failure context
        results = self.collection.query(query_texts=[error_msg], n_results=1)
        
        if not results['documents'] or not results['documents'][0]:
            return "No matching records found in the local knowledge base."

        context = results['documents'][0][0]
        metadata = results['metadatas'][0][0]
        
        # B. Construct the RAG Prompt
        prompt = f""" 
        A ROS 2 robot encountered the following error: "{error_msg}"
        
        I found this related issue in our historical database:
        - Historical Log: {context}
        - Verified Fix: {metadata['fix']}
        
        Please provide a concise, helpful explanation of why this is happening 
        and the exact steps the student should take to fix it.
        """

        # C. Generate the Explanation using Gemini
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)}. (Ensure your GOOGLE_API_KEY is exported)"

# --- GRADIO INTERFACE SECTION ---

def launch_dashboard():
    app = CopilotApp()
    
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Robotics Debugging Copilot")
        gr.Markdown("### Phase 2: RAG-Powered Diagnostics (Gemini + ChromaDB)")
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Enter ROS 2 Error Message", 
                    placeholder="e.g., [ERROR] [camera_node]: Failed to open device /dev/video0"
                )
                submit_btn = gr.Button("Analyze Error", variant="primary")
            
            with gr.Column():
                output_text = gr.Markdown(label="AI Diagnostic")

        submit_btn.click(fn=app.get_ai_diagnostic, inputs=input_text, outputs=output_text)
        
        gr.Examples(
            examples=[
                ["Navigation goal rejected: Controller costmap error"],
                ["Lookup would require extrapolation into the past"],
                ["Lidar timeout: No data received for 5.0 seconds"]
            ],
            inputs=input_text
        )

    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    # If you run this script directly, it opens the Web Dashboard
    launch_dashboard()
