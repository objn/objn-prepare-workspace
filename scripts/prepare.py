
from re import S
import struct
from modules import scripts, script_callbacks, shared
import os
import gradio as gr

def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as aesthetic_interface:
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                gr.HTML(value="Prepare your workspace")

                workspace_name = gr.Textbox(label="Workspace Name", placeholder="Enter workspace name")
                workspace_path = gr.Textbox(label="Workspace Path", placeholder="Enter workspace folder path")
                Phase_folder_num = gr.Slider(minimum=1, maximum=64, step=1, label="Number of Phase folder", value=3)

                generate_btn = gr.Button(value="Generate", variant='primary')
                

            with gr.Column():
                output = gr.Text(value="", show_label=False)
        
        def check_exists(Path_folder):
            if os.path.exists(os.path.join(Path_folder)):
                print("workspace : created " + os.path.join(Path_folder))
            else:
                print("workspace : not exists " + os.path.join(Path_folder))

        def generate_workspace(workspace_name,workspace_path,Phase_folder_num):
            workspace_path = os.path.join(workspace_path, workspace_name)
            os.makedirs(workspace_path, exist_ok=True)
            os.makedirs(os.path.join(workspace_path, "_RAW"), exist_ok=True)
            check_exists(os.path.join(workspace_path, "_RAW"))
                         
            stru_folder = ["Extra","Inpaint","Outpaint","Retouch"]

            for phase in range(1, Phase_folder_num + 1):
                phase_folder = os.path.join(workspace_path, f"phase{phase:02d}")
                os.makedirs(phase_folder, exist_ok=True)
                check_exists(phase_folder)
                for stru in stru_folder:
                    os.makedirs(os.path.join(phase_folder, stru), exist_ok=True)
                    check_exists(os.path.join(phase_folder, stru))

            output = "Workspace: " + workspace_name + "\nPath: " + workspace_path + "\nPhase: " + str(Phase_folder_num)
            return output

        generate_btn.click(
            fn=generate_workspace,
            inputs=[
                workspace_name,
                workspace_path,
                Phase_folder_num
            ],
            outputs=[
                output
            ]
        )

    return [(aesthetic_interface, "OBJ Prepare workspace", "prepare_workspace_interface")]

script_callbacks.on_ui_tabs(on_ui_tabs)
