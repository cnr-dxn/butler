from openai import OpenAI # type: ignore
import os

client = OpenAI(api_key=os.environ['ope'])

def summarize_newsletters_with_system(newsletters, system_instructions):
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": "Summarize the following newsletters and identify good investment opportunities:"},
        {"role": "user", "content": "\n\n".join(newsletters)}
    ]

    response = client.chat.completions.create(
        assistant="butler",
        messages=messages
    )

    return response.choices[0].message.content.strip()

# Example usage with system instructions and a list of newsletter texts
f = open("./example-text/newsletter1.txt", "r")
file = f.read().replace("\n", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ")

newsletters = [
    file
]

summary = summarize_newsletters_with_system(newsletters, system_instructions)
print(summary)