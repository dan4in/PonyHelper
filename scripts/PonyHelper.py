import os
import random
import datetime
import gradio as gr
from modules import script_callbacks, generation_parameters_copypaste, ui

# Directory of the current script
base_dir = os.path.dirname(__file__)
# Directory where data files are expected to be stored
data_dir = os.path.join(base_dir, 'Data')

def find_file_in_directory(filename, search_directory):
    """Recursively search for a file in a directory."""
    for root, _, files in os.walk(search_directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_tags_from_file(filename):
    # First, check in the data directory
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        # If not found, search in the entire PonyHelper directory
        pony_helper_dir = os.path.dirname(base_dir)
        filepath = find_file_in_directory(filename, pony_helper_dir)
        if not filepath:
            print(f"Warning: No such file: '{filename}' in the PonyHelper directory")
            return []
    with open(filepath, 'r') as file:
        return [tag.strip() for tag in file]

# Read tags from the text files
tags = {
    'general': read_tags_from_file('General'),
    'civitAI-Prompt': read_tags_from_file('civitAI-Prompt'),
    'characters': read_tags_from_file('Character'),
    'clothes': read_tags_from_file('clothes'),
    'accessory': read_tags_from_file('Accessory'),
    'copyright': read_tags_from_file('Copyright'),
    'artist': read_tags_from_file('Artist'),
    'nsfw': read_tags_from_file('NSFW'),
    'meta': read_tags_from_file('meta'),
    'hair': read_tags_from_file('hair'),
    'Age': read_tags_from_file('Age'),
    'Poses': read_tags_from_file('Poses'),
    'Backgrounds': read_tags_from_file('Backgrounds'),
    'Lighting': read_tags_from_file('Lighting'),
    'Quality': read_tags_from_file('Quality'),
    'Tattoos': read_tags_from_file('Tattoos'),
    'Emotions_Expressions': read_tags_from_file('Emotions_Expressions'),
    'Environment_Setting': read_tags_from_file('Environment_Setting'),
    'Season': read_tags_from_file('Season'),
    'Weather': read_tags_from_file('Weather'),
    'Themes': read_tags_from_file('Themes'),
    'Body_Types': read_tags_from_file('Body_Types'),
    'clothing_materials': read_tags_from_file('clothing_materials'),
    'Ethnicity_Nationality': read_tags_from_file('Ethnicity_Nationality'),
    'Perspective': read_tags_from_file('Perspective'),
    'Animals_Creatures': read_tags_from_file('Animals_Creatures'),
    'Props_Objects': read_tags_from_file('Props_Objects'),
}

def generate_words(num_words, category):
    return random.sample(tags[category], min(num_words, len(tags[category])))

def generate_mixed_tags(num_words, rating_safe, rating_explicit, rating_questionable, rating_realistic, undanbooru_tags, *enabled_categories):
    pony_options = {
        'rating_safe': rating_safe,
        'rating_explicit': rating_explicit,
        'rating_questionable': rating_questionable,
        'rating_realistic': rating_realistic,
        'undanbooru_tags': undanbooru_tags,
    }

    clean_tags = undanbooru_tags
    categories = [category for category, enabled in zip(tags.keys(), enabled_categories) if enabled]
    mixed_tags_result = []

    for category in categories:
        words = generate_words(num_words, category)
        if clean_tags:
            words = [word.replace('_', ' ').replace('(', ' ').replace(')', ' ').replace('{', ' ').replace('}', ' ').replace('-', ' ').replace('!?', ' ').replace('&', ' ').replace('+', ' ').replace('=', ' ').replace('@', ' ').replace('^', ' ').replace('<', ' ').replace('>', ' ') for word in words]
        mixed_tags_result.extend(words)

    if pony_options.get('Pony_score', False):
        score_string1 = 'score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up'
        score_string2 = 'score_10, score_9_up, score_8_up, score_7_up, score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up'
        current_minute = datetime.datetime.now().minute
        selected_score_string = score_string1 if current_minute % 2 == 0 else score_string2
        mixed_tags_result.append(selected_score_string)

    if pony_options.get('rating_safe', False):
        mixed_tags_result.append('rating_safe')
    if pony_options.get('rating_explicit', False):
        mixed_tags_result.append('rating_explicit')
    if pony_options.get('rating_questionable', False):
        mixed_tags_result.append('rating_questionable')
    if pony_options.get('rating_realistic', False):
        mixed_tags_result.append('score_hyper-realistic, realistic, ((Full Body:1.2))')

    for word, selected in pony_options.items():
        if word.startswith('source_') and selected:
            mixed_tags_result.append(word)

    mixed_tags_str = ', '.join(mixed_tags_result)
    return mixed_tags_str

def find_prompts(fields):
    field_prompt = [x for x in fields if x[1] == "Prompt"][0]
    field_negative_prompt = [x for x in fields if x[1] == "Negative prompt"][0]
    return [field_prompt[0], field_negative_prompt[0]]

def send_prompts(text):
    if not text:
        return "", gr.update()
    params = generation_parameters_copypaste.parse_generation_parameters(text)
    negative_prompt = params.get("Negative prompt", "")
    return params.get("Prompt", ""), negative_prompt or gr.update()

def add_tag_tab(enabled_categories):
    with gr.Blocks(css=".slider { margin: 0.5em 0; } .checkbox { margin: 0.5em 0; } .btn { margin: 1em 0; padding: 0.5em 1em; background-color: #4CAF50; color: white; border: none; cursor: pointer; }") as interface:
        with gr.Tab("Pony Helper"):
            with gr.Row():
                num_words = gr.Slider(label="Number of Tags __________________________Pony Scores- 'score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up' ", minimum=1, maximum=5, step=1, value=1)
            with gr.Row():
                rating_safe = gr.Checkbox(label="Safe", value=False)
                rating_explicit = gr.Checkbox(label="Explicit", value=False)
                rating_questionable = gr.Checkbox(label="Questionable", value=False)
                rating_realistic = gr.Checkbox(label="Realistic", value=False)
                undanbooru_tags = gr.Checkbox(label="Undanbooru Tags", value=False)
            with gr.Row():
                # Use the provided enabled_categories argument
                enabled_categories = [gr.Checkbox(label=category.replace('_', ' ').title(), value=enabled) for category, enabled in enabled_categories.items()]
            with gr.Row():
                btn_generate = gr.Button("Generate Mixed Tags", css="btn")
            with gr.Row():
                output = gr.Textbox(label="Generated Tags")
            with gr.Row():
                btn_send_txt2img = gr.Button("Send to txt2img", css="btn")
                btn_send_img2img = gr.Button("Send to img2img", css="btn")

            btn_generate.click(fn=generate_mixed_tags, inputs=[num_words, rating_safe, rating_explicit, rating_questionable, rating_realistic, undanbooru_tags] + enabled_categories, outputs=output)
            btn_send_txt2img.click(fn=lambda tags: send_prompts(tags), inputs=output, outputs=find_prompts(ui.txt2img_paste_fields))
            btn_send_img2img.click(fn=lambda tags: send_prompts(tags), inputs=output, outputs=find_prompts(ui.img2img_paste_fields))

    return [(interface, "Pony Helper", "pony-helper")]

# Use the modified add_tag_tab function as the callback for ui_tabs
script_callbacks.on_ui_tabs(lambda: add_tag_tab(tags))