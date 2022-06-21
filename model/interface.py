import gradio as gr
from main import main
demo = gr.Interface(
    fn = main, 
    inputs="text", 
    outputs=["text","text","text"],
    title="YouTube Gaming Recommendation")
demo.launch()