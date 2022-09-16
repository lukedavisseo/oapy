import openai	
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

desc_dict = {
	'Question': [],
	'Text': []
}

max_tokens_dict = {
	'Meta title': 15,
	'Meta description': 40,
	'Category header copy': 200
}

tone_selector_dict = {
	'Friendly': 'in a friendly tone',
	'Professional': 'in a professional tone',
	'Persuasive': 'in a persuasive tone'
}

st.header('Welcome to oapy!')

st.subheader('oapy is an OpenAI script that generates copy at scale based on a given prompt.')

st.markdown("---")

with st.expander("What is oapy good for? 🤔", expanded=False):

	st.markdown(
	"""
	From an SEO perspective, OpenAI works well for things like:
	* Meta descriptions
	* Text summarisation
	* Some factual definitions
	""")

with st.expander("How to use oapy 🤖", expanded=False):

	st.markdown(
		"""
		0. Use the calculator on the left sidebar to get an estimate of how much your work may cost. Using the [Davinci engine](https://beta.openai.com/docs/models/overview) costs 0.02 (USD) per 1,000 tokens so if you were to create meta descriptions at around 160 characters each for 1000 pages, the cost would be around 0.80 (USD).
		1. Enter your API key which you can find on the [View API Keys](https://beta.openai.com/account/api-keys) page when you log into OpenAI.
		2. Enter your prompt(s), one per line. This is where you tell OpenAI what you want it to write. For tips on writing prompts, check out [OpenAI's examples page](https://beta.openai.com/examples).
		3. Enter your max tokens amount. If you've used the calculator, that's roughly your character limit divided by 4.
		4. Click 'Generate' and wait for OpenAI to work its magic. Once completed, it will display a Download button for you to download the data in CSV format.
	    """
    )

with st.expander("To do list 📝", expanded=False):

	st.markdown(
		"""
		- Coming soon.
	    """
    )

st.markdown("---")

# Load your API key
openai.api_key = st.text_input('Enter your API key')

prompt_texts = st.text_area('Enter your prompt, 1 per line')

# Output sidebar

output_selector = st.sidebar.selectbox('What do you want your output to be? Select from a list of presets.', ('Meta title', 'Meta description', 'Category header copy'))

tone_selector = st.sidebar.selectbox('Choose a tone for your prompt', ('Friendly', 'Professional', 'Persuasive'))

temp_slider = st.sidebar.slider('Set the temperature of the completion', 0.0, 1.0, 0.7)

generate = st.button('Generate!')

if generate:

	with st.spinner('Classifying...'):

		st.image('road-runner-coyote.gif')

		lines = prompt_texts.split('\n')

		prompt_list = [line for line in lines]

		for prompt in prompt_list:

			prompt = f'Write a {output_selector.lower()} for {prompt} {tone_selector_dict[tone_selector]}'

			desc_dict['Question'].append(prompt)

			response = openai.Completion.create(
				engine='text-davinci-002',
				temperature=temp_slider,
				prompt=prompt,
				max_tokens=max_tokens_dict[output_selector])

			desc_dict['Text'].append(response.choices[0].text)

	df = pd.DataFrame(desc_dict)

	desc_csv = df.to_csv()

	st.balloons()

	st.success('Completed!')

	st.download_button(label='Download CSV', data=desc_csv, file_name='desc_csv.csv', mime='text/csv')