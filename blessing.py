import pandas as pd
import random
import unicodedata
import re
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from datetime import date
from ConfigCenter import R2Config

load_dotenv()
config = R2Config()

openai_json = config.read_json(f'openai_{os.environ["OPENAI_ACCOUNT"]}.json')
openai_api_key = openai_json['OPENAI_API_KEY']
openai_base_url = openai_json['OPENAI_BASE_URL']

# 收件人邮箱
RECIPIENT_EMAIL = "i@xiaowenz.com"
SENDER_EMAIL = "support@blessing.vip"

def create_prompt(nameOfGod, region, dutyInCharge, religion, generalDescription):
    prompt = f"""You are a deity who guards humanity.

Your profile

- nameOfGod:<{nameOfGod}>
- region:<{region}>
- dutyInCharge:<{dutyInCharge}>
- religion:<{religion}>
- desc:<{generalDescription}>

your goal is to write a blessing letter to one of your devoted followers

- Immerse yourself in the role, historical background, and responsibilities
- Include a salutation and closing with today's date ({date.today().strftime("%Y-%m-%d")})
- Provide a positive and uplifting response to the prayer, using simple and easy-to-understand language
- Infuse your personal values and life philosophy
- Use a humorous and lighthearted tone, with a twist at the end
- Conclude with a haiku poem
- Word count: 500
- Write in English
- Print your output in below json format, use <p> tag for every paragraph

```json
"letter": "<p>Deer,</p><p>This is me.</p>"
```
"""
    return prompt

def create_message(prompt):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=openai_api_key, base_url=openai_base_url
    )
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        temperature=1.2, response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful writer designed to output JSON."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )
    #print(response)
    print(response.choices[0].message.content)
    data = json.loads(response.choices[0].message.content)

    return data.get('letter', None)

def replace_template(html_template_file, content, output_file):
    """
    Replace ${Content} in an HTML template file with the provided content
    and save the result to a new HTML file.

    :param html_template_file: path to the HTML template file
    :param content: the content to replace ${Content} with
    :param output_file: path to the output HTML file
    """
    with open(html_template_file, 'r') as f:
        template_content = f.read()

    replaced_content = template_content.replace('${Content}', content)

    with open(output_file, 'w') as f:
        f.write(replaced_content)


if __name__ == "__main__":
    # Read the Excel file
    df = pd.read_excel('gods_normalized.xlsx')

    # Select a random row from the dataframe
    random_row = df.sample(n=1)

    # Extract the values from the row
    nameOfGod = random_row['nameOfGod'].values[0]
    region = random_row['region'].values[0]
    dutyInCharge = random_row['dutyInCharge'].values[0]
    religion = random_row['religion'].values[0]
    generalDescription = random_row['generalDescription'].values[0]


    # Concatenate the values into a single string
    output_string = f"{nameOfGod} from {region} is in charge of {dutyInCharge} in {religion} religion. {generalDescription}"

    # Print the output string
    print(output_string)

    # Construct prompt
    prompt = create_prompt(nameOfGod, region, dutyInCharge, religion, generalDescription)
    
    print(prompt)
    
    # Write
    msg = create_message(prompt)
    #print(msg)

    # Create Email HTML
    replace_template("blessing_template.html", msg, "blessing_output.html")