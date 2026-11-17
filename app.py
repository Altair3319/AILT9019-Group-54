import gradio as gr
from assistant import ask

def respond(question):
    result=ask(question)
    return result["answer"]+"\n\nCitation: "+result["citation"]

demo=gr.Interface(
    fn=respond,
    inputs="text",
    outputs="text",
    title="HKU Library Regulations Assistant",
)

demo.launch()
