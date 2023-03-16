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

st.markdown(f'<div class="header"><figure><embed type="image/svg+xml" src="https://impression-static.s3.eu-west-1.amazonaws.com/misc/oapy-logo.svg" /><figcaption><h1>Welcome to oapy!</h1></figcaption></figure><h3>oapy is an OpenAI script that generates copy at scale based on a given prompt.</h3></div>', unsafe_allow_html=True)


desc_dict = {
	'Question': [],
	'Text': []
}

max_tokens_dict = {
	'Meta title': [30, 'in 60 characters or less'],
	'Meta description': [40, 'in 160 characters or less'],
	'Category header copy': [200, 'in 800 characters or less']
}

intent_selector_dict = {
	'Commercial': 'with a commercial intent',
	'Informational': 'with a informational intent',
	'Navigational': 'with a navigational intent',
	'Transactional': 'with a transactional intent'
}

with st.expander("What is Oapy and how can it be used? 🤔", expanded=False):

	st.markdown(
	"""
	Oapy is a ChatGPT script that can generate SEO content at scale. Depending on the prompt mode you select on the left sidebar, you can create:
	* Responses to custom prompts (using the Playground mode)
	* Meta titles
	* Meta description
	* Category header copy

	""")

with st.expander("What are the prompt modes? 📝", expanded=False):

	st.markdown(
		"""
		There are two prompt modes available:
		* Playground - this runs similar to OpenAI’s Playground tool, allowing you to generate outputs based on custom prompts. This is good for varied prompt engineering that you don't need to scale.
		* Multiple Keywords - this allows you to build a more prescriptive output based on multiple search terms. Here, you can create meta titles, meta descriptions, and category header copy by further configuring the output on the left sidebar. You can also determining your search intent and include additional instructions to enhance your prompts.

	    """
    )

with st.expander("How to use oapy 🤖", expanded=False):

	st.markdown(
		"""
		1. Set the prompt mode on the left sidebar, determining whether you want to work in Playground or Multiple Keywords mode.
		2. Enter your API key in the field below. You can find your Secret API key when you log into your OpenAI account, under [User settings](https://beta.openai.com/account/api-keys). (Check out their [Best Practices for API Key Safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) page to learn how you can keep your API key safe.
		3. Based on your prompt selection in step 1, write your prompt(s) or the keyword(s) you wish to target in the field provided.
		4. Click 'Generate' and wait for Oapy to work its magic. Once completed, it will display the prompt and its output (in Playground mode) or a Download button for you to download the data as a CSV file (Multiple Keywords mode).
	    """
    )

with st.expander("Credits 🏆", expanded=False):

	st.markdown(
		"""
		Oapy was created by [Luke Davis](https://lukealexdavis.co.uk/) at [Impression, a multi-award-winning SEO agency](https://www.impression.co.uk/seo/) in the UK & US.
	    """
    )

st.markdown("---")

# Output sidebar
prompt_mode = st.sidebar.selectbox('Set the prompt mode', ('Playground', 'Multiple Keywords'))

# Load your API key
openai.api_key = st.text_input('Enter your API key')

if prompt_mode == 'Playground':
	prompt_text = st.text_area('Enter your prompt(s)')
	temp_slider = st.sidebar.slider('Set the temperature of the completion. Higher values make the output more random,  lower values make it more focused.', 0.0, 1.0, 0.7)
	rep_penalty = st.sidebar.slider("Set the repetition penalty. A bigger value means more varied sentences.", 0.9, 2.0, 1.0)
else:
	output_selector = st.sidebar.selectbox('What do you want your output to be? Select from a list of presets.', ('Meta title', 'Meta description', 'Category header copy'))
	intent_selector = st.sidebar.selectbox('Choose an intent for your prompt', (intent_selector_dict.keys()))
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
				output = oapy_utils.oapy_generator('gpt-3.5-turbo', temp_slider, prompt, max_tokens_dict[output_selector][0], rep_penalty)
				desc_dict['Text'].append(output)

				st.write(f'{prompt}\n\n{output}')

			oapy_utils.generate_csv_output(desc_dict)

		else:

			output = oapy_utils.oapy_generator('gpt-3.5-turbo', temp_slider, prompt, max_tokens_dict[output_selector][0], rep_penalty)

			st.write(f'{prompt_text} {output}')

			st.balloons()

# Loading CSS
utl.local_css("frontend.css")
utl.remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
utl.remote_css('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700&display=swap')
