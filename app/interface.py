import gradio as gr
from get_video_content import GetVideoContent

demo = gr.Interface(fn=GetVideoContent, inputs="text", outputs="text")
demo.launch()