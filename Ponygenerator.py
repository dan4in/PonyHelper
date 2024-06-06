from flask import Flask, render_template, request, jsonify
import random
import datetime


app = Flask(__name__)

def read_tags_from_file(filename):
    with open('data/' + filename, 'r') as file:  # Prepend 'data/' to the filename
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

tag_counts = {category: len(tags_list) for category, tags_list in tags.items()}
total_tags = sum(tag_counts.values())
# Sort the tag_counts dictionary by count in descending order
sorted_tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))

def generate_words(num_words, pony_options, category, clean_tags=False):
    selected_words = random.sample(tags[category], min(num_words, len(tags[category])))
    
    # If "Undanbooru Tags" is selected or clean_tags is True, replace certain characters with a space in the tags
    if pony_options.get('undanbooru_tags', False) or clean_tags:
        selected_words = [word.replace('_', ' ').replace('(', ' ').replace(')', ' ').replace('{', ' ').replace('}', ' ').replace('-', ' ').replace('!?', ' ').replace('&', ' ').replace('+', ' ').replace('=', ' ').replace('@', ' ').replace('^', ' ').replace('<', ' ').replace('>', ' ') for word in selected_words]
    
    result = ', '.join(selected_words)
    
    # Include score if selected
    if pony_options.get('Pony_score', False):
        # Define the two score strings
        score_string1 = 'score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up'
        score_string2 = 'score_10, score_9_up, score_8_up, score_7_up, score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up'
        
        # Use the current minute to decide which score string to use
        current_minute = datetime.datetime.now().minute
        selected_score_string = score_string1 if current_minute % 2 == 0 else score_string2
        
        result = selected_score_string + ', ' + result
    
    # Include selected rating options
    if pony_options.get('rating_safe', False):
        result += ', rating_safe'
    if pony_options.get('rating_explicit', False):
        result += ', rating_explicit'
    if pony_options.get('rating_questionable', False):
        result += ', rating_questionable'
    if pony_options.get('rating_realistic', False):
        result += ', score_hyper-realistic, realistic, ((Full Body:1.2))'
    
    # Include selected source options
    for word, selected in pony_options.items():
        if word.startswith('source_') and selected:
            result += ', ' + word
    
    return result
    
def static_image(filename):
    return url_for('static', filename=f'images/{filename}.png')

app.jinja_env.globals.update(static_image=static_image)

@app.route('/generate-tags/<category>', methods=['POST'])
def generate_tags(category):
    num_words = int(request.form['num_words'])
    pony_options = {key: True if request.form.get(key) == 'on' else False for key in request.form.keys()}
    tags_result = generate_words(num_words, pony_options, category)
    return jsonify(tags_result=tags_result)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    characters_result = ''
    form_values = {}
    mixed_tags_result = {}
    
    if request.method == 'POST':
        num_words = int(request.form['num_words'])
        pony_options = {key: True if request.form.get(key) == 'on' else False for key in request.form.keys()}
        
        if 'num_words_characters' in request.form:
            characters_result = generate_words(1, pony_options, 'characters')
        else:
            result = generate_words(num_words, pony_options, 'general')
        
        form_values = request.form

    sorted_tag_counts = dict(sorted(tag_counts.items(), key=lambda item: item[1], reverse=True))

    return render_template('index.html', result=result, characters_result=characters_result, form_values=form_values, tags=tags, mixed_tags_result=mixed_tags_result, tag_counts=sorted_tag_counts, total_tags=total_tags)
   
@app.route('/generate-random-values', methods=['GET'])
def generate_random_values():
    # Generate random values for cfg and steps
    cfg = random.randint(3, 12)
    steps = random.randint(20, 60)
    
    # Return the values as JSON
    return jsonify(cfg=cfg, steps=steps)

@app.route('/generate-characters', methods=['POST'])
def generate_characters():
    num_words = request.form.get('num_words', '1')
    pony_options = {key: True if request.form.get(key) == 'on' else False for key in request.form.keys()}
    clean_tags = pony_options.get('undanbooru_tags', False)
    print("Received pony_options:", pony_options)
    print("Clean tags flag:", clean_tags)
    characters_result = generate_words(1, pony_options, 'characters', clean_tags=clean_tags)
    return jsonify(characters_tags_result=characters_result, num_words=num_words, form_values=request.form)

@app.route('/generate-mixed-tags', methods=['POST'])
def generate_mixed_tags():
    mixed_tags_options = {key: int(value) for key, value in request.form.items() if int(value) > 0}
    print("Mixed Tags Options:", mixed_tags_options)
    if mixed_tags_options.get('undanbooru_tags', False):
        mixed_tags_options['undanbooru_tags'] = 1  # Ensure undanbooru_tags is set to 1 if selected
    clean_tags = mixed_tags_options.get('undanbooru_tags', False)  # Check if clean_tags should be True
    mixed_tags_result = {category: generate_words(value, mixed_tags_options, category, clean_tags=clean_tags) for category, value in mixed_tags_options.items() if category in tags}
    return jsonify(mixed_tags_result=mixed_tags_result)  # Return mixed_tags_result

@app.route('/')
def static_image():
    return render_template('index.html', mixed_tags_result=cleaned_tags_result, form_values=request.form, tags=tags, tag_counts=sorted_tag_counts, total_tags=total_tags)


if __name__ == '__main__':
    app.run(debug=True)
