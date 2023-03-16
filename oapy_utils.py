import openai
import pandas as pd
import streamlit as st

# Generate CSV output
def generate_csv_output(prompt_output_dict):
	df = pd.DataFrame(prompt_output_dict)
	prompt_output_csv = df.to_csv()
	st.balloons()
	st.success('Completed!')
	st.download_button(label='Download CSV', data=prompt_output_csv, file_name='prompt_output.csv', mime='text/csv')

def oapy_generator(model, temperature, prompt, tokens, frequency_penalty):
	response = openai.ChatCompletion.create(
			model=model,
			messages=[
				{
					"role": "user",
					"content": prompt
				}
			],
			temperature=temperature,
			max_tokens=tokens,
			frequency_penalty=frequency_penalty
		)

	output = response['choices'][0]['message']['content']

	return output