import openai	
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import utils as utl
import oapy_utils

st.set_page_config(
	page_icon="https://impression-static.s3.eu-west-1.amazonaws.com/logos/impression-digital-logo-square-80.png", 
	layout="wide",
	page_title='Oapy by Impression',
	initial_sidebar_state="expanded"
)

st.markdown(f'<div class="header"><figure><embed type="image/svg+xml" src="https://impression-static.s3.eu-west-1.amazonaws.com/misc/oapy-logo.svg" /><figcaption><h1>Welcome to oapy!</h1></figcaption></figure><h3>oapy is a GPT-4 web app that generates copy at scale based on a given prompt.</h3></div>', unsafe_allow_html=True)


desc_dict = {
	'Question': [],
	'Text': []
}

max_tokens_dict = {
	'Meta title': [30, 'in 60 characters or less'],
	'Meta description': [40, 'in 160 characters or less'],
	'Category header copy': [200, 'in 800 characters or less']
}

pg_max_tokens_dict = {
	'Very short': 25,
	'Short': 50,
	'Medium': 100,
	'Long': 200,
	'Very long': 300
}

intent_selector_dict = {
	'Commercial': 'with a commercial intent',
	'Informational': 'with a informational intent',
	'Navigational': 'with a navigational intent',
	'Transactional': 'with a transactional intent'
}

with st.expander("How to use oapy 🤖", expanded=False):

	st.markdown(
		"""
		Please refer to [our dedicated guide](https://www.impression.co.uk/resources/tools/oapy/) on how to use Oapy via the Impression website.
		"""
    )

with st.expander("Credits 🏆", expanded=False):

	st.markdown(
		"""
		Oapy was created by [Luke Davis](https://lukealexdavis.co.uk/) at [Impression, a multi-award-winning SEO agency](https://www.impression.co.uk/seo/) in the UK & US.
	    """
    )

st.markdown("---")

# Model selector sidebar
model = st.sidebar.selectbox('Choose your model', ('gpt-4o', 'gpt-4', 'gpt-3.5-turbo'))

# Output sidebar
prompt_mode = st.sidebar.selectbox('Set the prompt mode', ('Playground', 'Multiple Keywords'))

# Load your API key
openai.api_key = st.text_input('Enter your API key')

if prompt_mode == 'Playground':
	prompt_text = st.text_area('Enter your prompt')
	pg_max_tokens_length = st.sidebar.slider('Maximum length', 1, 4095)
	temp_slider = st.sidebar.slider('Set the temperature of the completion. Higher values make the output more random,  lower values make it more focused.', 0.0, 1.0, 0.7)
	rep_penalty = st.sidebar.slider("Set the repetition penalty. A bigger value means more varied sentences.", 0.9, 2.0, 1.0)
else:
	output_selector = st.sidebar.selectbox('What do you want your output to be? Select from a list of presets.', ('Meta title', 'Meta description', 'Category header copy'))
	intent_selector = st.sidebar.selectbox('Choose an intent for your prompt', (intent_selector_dict.keys()))
	pg_max_tokens_length = st.sidebar.select_slider('Set the length of your output', options=['Very short', 'Short', 'Medium', 'Long', 'Very long'], value='Medium')
	temp_slider = st.sidebar.slider('Set the temperature of the completion. Higher values make the output more random,  lower values make it more focused.', 0.0, 1.0, 0.7)
	rep_penalty = st.sidebar.slider("Set the repetition penalty. A bigger value means more varied sentences.", 0.9, 2.0, 1.0)
	prompt_text = st.text_area('Enter your keywords, 1 per line')
	add_instruct = st.text_area('Add further instructions here to enhance your prompt(s)')

generate = st.button('Generate!')

if generate:

	with st.spinner('Classifying...'):

		if prompt_mode == 'Multiple Keywords':

			lines = prompt_text.split('\n')
			prompt_list = [line for line in lines]

			for prompt in prompt_list:

				prompt = f'Write a {output_selector.lower()} for {prompt} {intent_selector_dict[intent_selector]}, {max_tokens_dict[output_selector][1]}. {add_instruct}'
				desc_dict['Question'].append(prompt)
				output = oapy_utils.oapy_generator(model, temp_slider, prompt, max_tokens_dict[output_selector][0], rep_penalty)
				desc_dict['Text'].append(output)

			oapy_utils.generate_csv_output(desc_dict)

		else:

			output = oapy_utils.oapy_generator(model, temp_slider, prompt_text, pg_max_tokens_dict[pg_max_tokens_length], rep_penalty)

			st.write(f'{prompt_text} {output}')

			st.balloons()

# Loading CSS
utl.local_css("frontend.css")
utl.remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
utl.remote_css('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap')
