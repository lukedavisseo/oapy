import openai
import pandas as pd
import streamlit as st

desc_dict = {
	'Question': [],
	'Text': []
}

# Load your API key from an environment variable or secret management service
openai.api_key = st.text_input('Enter API key')

prompt_texts = st.text_area('Enter text, 1 per line')

submit = st.button('Submit')

if submit:

	lines = prompt_texts.split('\n')

	prompt_list = [line for line in lines]

	for prompt in prompt_list:

		desc_dict['Question'].append(prompt)

		response = openai.Completion.create(
			engine="text-davinci-001",
			temperature=0.7,
			prompt=prompt,
			max_tokens=400)

		desc_dict['Text'].append(response.choices[0].text)

	df = pd.DataFrame(desc_dict)

	desc_csv = df.to_csv()

	st.download_button(label='Download CSV', data=desc_csv, file_name='desc_csv.csv', mime='text/csv')