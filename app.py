
from core import full_pipeline, suggest_project_id, search_and_save
import gradio as gr

def gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("""
        <div style='text-align:center'>
            <img src='https://i.imgur.com/4Raq5oX.jpeg' style='width:100%; max-height:180px; object-fit:contain;'><br>
            <h2>clickdreams. Media Scraper Tool</h2>
        </div>
        """)

        with gr.Tab("Keyword Scraper"):
            gr.Markdown("**Enter search term and choose media type.**")
            with gr.Row():
                search_term = gr.Textbox(label="Search Term", value="real estate logo")
                media_type = gr.Dropdown(choices=["image", "gif", "video", "music"], value="image", label="Media Type")

            output_files = gr.File(label="Downloadable Files", file_count="multiple", visible=False)
            output_text = gr.Textbox(label="Results", lines=10, visible=False)

            def wrapped(term, media):
                result = search_and_save(term, media)
                if isinstance(result, list) and all(p.endswith(('.jpg', '.gif', '.txt')) for p in result):
                    return gr.update(visible=True, value=result), gr.update(visible=False)
                else:
                    return gr.update(visible=False), gr.update(visible=True, value=result)

            btn = gr.Button("Search & Save")
            btn.click(fn=wrapped, inputs=[search_term, media_type], outputs=[output_files, output_text])

        with gr.Tab("Script to B-Roll & Assets"):
            script_input = gr.Textbox(label="📜 Paste Heygen Script", lines=20)
            project_id_input = gr.Textbox(label="🆔 Project ID", placeholder="Auto-generated", interactive=True)
            script_input.change(fn=suggest_project_id, inputs=script_input, outputs=project_id_input)

            with gr.Column():
                gr.Markdown("📄 **Brief File Link**")
                brief_output = gr.HTML()
                asset_output = gr.Textbox(label="📁 Download Log", lines=10)

                run_btn = gr.Button("✨ Generate Brief + Download Assets")
                run_btn.click(fn=full_pipeline, inputs=[script_input, project_id_input], outputs=[brief_output, asset_output])

    demo.launch()

if __name__ == "__main__":
    gradio_interface()
