import openai
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

desc_dict = {
	'Question': [],
	'Text': []
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
		0. Use the calculator on the left sidebar to get an estimate of how much your work may cost. Using the [Davinci engine](https://beta.openai.com/docs/models/overview) costs 0.06 (USD) per 1,000 tokens so if you were to create meta descriptions at around 160 characters each for 1000 pages, the cost would be around 2.40 (USD).
		1. Enter your API key which you can find on the [View API Keys](https://beta.openai.com/account/api-keys) page when you log into OpenAI.
		2. Enter your prompt(s), one per line. This is where you tell OpenAI what you want it to write. For tips on writing prompts, check out [OpenAI's examples page](https://beta.openai.com/examples).
		3. Enter your max tokens amount. If you've used the calculator, that's roughly your character limit divided by 4.
		4. Click 'Generate' and wait for OpenAI to work its magic. Once completed, it will display a Download button for you to download the data in CSV format.
	    """
    )

with st.expander("To do list 📝", expanded=False):

	st.markdown(
		"""
		- Add sliders to adjust the model's parameters.
	    """
    )

st.markdown("---")

# Load your API key
openai.api_key = st.text_input('Enter your API key')

prompt_texts = st.text_area('Enter your prompt, 1 per line')

max_tokens = st.number_input(
	'Enter your max token amount. As 1 token is roughly 4 characters, you can divide your character limit by 4 to get a good estimate.')

st.sidebar.subheader('Calculate the cost of your work using the inputs below.')

token_calc = st.sidebar.text_input('What is your character limit? For example, 160 characters works well for meta descriptions.')

page_total = st.sidebar.text_input('How many pages are you creating text for?')

calculate = st.sidebar.button('Calculate cost')

if calculate:

	token_price = int(token_calc) * int(page_total) / 4 / 1000 * 0.06

	st.sidebar.write(f'Your total cost would be around ${token_price:.2f}.')

submit = st.button('Generate!')

if submit:

	with st.spinner('Classifying...'):

		st.image('road-runner-coyote.gif')

		lines = prompt_texts.split('\n')

		prompt_list = [line for line in lines]

		for prompt in prompt_list:

			desc_dict['Question'].append(prompt)

			response = openai.Completion.create(
				engine="text-davinci-001",
				temperature=0.7,
				prompt=prompt,
				max_tokens=int(max_tokens))

			desc_dict['Text'].append(response.choices[0].text)

	df = pd.DataFrame(desc_dict)

	desc_csv = df.to_csv()

	st.balloons()
	st.success('Completed!')

	st.download_button(label='Download CSV', data=desc_csv, file_name='desc_csv.csv', mime='text/csv')
