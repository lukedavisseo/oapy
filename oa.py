import openai
import pandas as pd
import streamlit as st
from decimal import *

getcontext().prec = 4

desc_dict = {
	'Question': [],
	'Text': []
}

st.header('Welcome to oapy!')

st.subheader('oapy is an OpenAI script that generates text at scale based on its input. Great for descriptions and definitions.')

st.markdown(
	'''Please read the [available documentation](https://beta.openai.com/docs) for more info on how OpenAI works. You should also consult the pricing page before trying this script for multiple text strings. For example, using the Davinci engine (the most powerful one) costs 0.06 (USD) per 1,000 tokens so if you were to create 160 character meta descriptions for 1000 pages, the cost would be around 2.40 (USD). Feel free to use the calculator below to get an estimated price before you go wild in the AIsles!''')

# Load your API key
openai.api_key = st.text_input('Enter API key')

prompt_texts = st.text_area('Enter text, 1 prompt per line')

st.subheader('Now you can calculate the cost of your work, using the inputs below.')

token_calc = st.text_input('What is your character limit? For example, 160 characters works well for meta descriptions.')

page_total = st.text_input('How many pages are you creating text for?')

max_tokens = st.number_input(
	'Enter max token amount. 1 token is roughly 4 characters. Remember: there are associated costs so please read the pricing documentation before using this at large scale!')

calculate = st.button('Calculate cost')

if calculate:

	token_price = Decimal(token_calc) * Decimal(page_total) / 4 / 1000 * Decimal(0.06)
	
	max_token_price = (Decimal(token_calc) * Decimal(page_total) / 4) * ((max_tokens / 1000) * Decimal(0.06))

	st.write(f'Your total cost would be around ${Decimal(token_price)} but could rise to ${Decimal(max_token_price)} depending on your prompt.')

submit = st.button('Generate!')

if submit:

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

	st.download_button(label='Download CSV', data=desc_csv, file_name='desc_csv.csv', mime='text/csv')
