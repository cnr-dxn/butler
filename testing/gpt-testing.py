from openai import OpenAI # type: ignore
import os
import sys
import boto3
from time import sleep 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *

client = OpenAI(api_key=os.environ['ope'])

def synthesizeSpeech(text, output_file):
    # Initialize a session using Amazon Polly
    polly = boto3.client('polly')

    # Synthesize speech using Polly
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId="Matthew",
        Engine="neural"
    )

    # Save the audio stream returned by Amazon Polly to an MP3 file
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())

    print(f"Speech synthesized and saved to {output_file}")

# Pretty printing helper
def extract_message(messages):
    for m in messages:
        if (m.role).lower() == "assistant":
            return m.content[0].text.value

def wait_on_run(run, thread):
    seconds = 0
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        print(f"\rwaiting for {str(seconds).zfill(2)} seconds with status: {run.status}", end='', flush=True)
        sleep(1)
        seconds += 1
    print(f"\rwaiting for {str(seconds).zfill(2)} seconds with status: {run.status}", end='', flush=True)
    print()
    return run

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        max_completion_tokens = max_assistant_answer_tokens
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def summarize_newsletters_with_system(input_script, tokens = 1000):
    thread = client.beta.threads.create()
    run = submit_message(asst_id, thread, input_script)
    return thread, run

# Emulating concurrent user requests
thread1, run1 = summarize_newsletters_with_system(
    "Harmful Reality of Fraud-Fighting with Algorithms - In a recent video , we discussed how algorithms are driving inflation, showing how automated decision-making can have unintended economic consequences. Today, we’re discussing another controversial use of algorithms: catching tax evaders and welfare cheats. While this might sound like a tech-savvy solution to a persistent problem, it’s actually pretty bad. Governments worldwide have increasingly turned to algorithms to identify and penalize tax and welfare fraud. The idea is simple: leverage advanced data analytics to flag suspicious activity and reduce human error. However, this approach is fraught with pitfalls and almost always leads to disaster. Take, for instance, the infamous Robodebt scandal in Australia. In an attempt to crack down on welfare fraud, the Australian government introduced an automated debt recovery system. The algorithm cross-referenced income data from different sources to identify discrepancies. Sounds like a good way to catch welfare fraud without additional overhead, right? Not quite. The Robodebt algorithm generated thousands of false positives, accusing innocent people of owing money to the government. Many recipients were low-income individuals already struggling to make ends meet. The stress and anxiety caused by erroneous debt notices had severe mental health impacts, with reports of people taking their lives linked to the distress caused by the system. Public outrage and legal challenges eventually forced the government to scrap the program and issue refunds, but the damage was already done. Similar examples can be found elsewhere. In the Netherlands, an algorithm designed to detect welfare fraud disproportionately targeted low-income families , often from immigrant backgrounds. The system flagged minor discrepancies as fraudulent, leading to significant financial and emotional hardship for those wrongly accused. This program, too, faced backlash and legal scrutiny, culminating in a national scandal that eroded public trust in government institutions. In the United States, the IRS has explored using algorithms to catch tax cheats. While identifying high-risk cases might increase efficiency, there are substantial risks. Automated systems can misinterpret data, leading to wrongful accusations and financial penalties for law-abiding citizens. The complexity of tax codes means that legitimate discrepancies can easily be misread as fraudulent activity, causing undue stress and financial burdens on individuals and businesses alike. The fundamental problem with using algorithms in these contexts is their lack of nuance and inability to account for the complexities of human behavior and circumstances. Algorithms rely on data, and data can be flawed or incomplete. Moreover, automated systems lack the empathy and discretion that human judgment can provide. When it comes to something as consequential as accusing someone of fraud, the stakes are too high to leave to an unfeeling machine. Critics argue that instead of investing in automated systems, resources should be directed toward improving human oversight and support. Trained professionals can make more accurate and fair assessments, considering the broader context of each case. Additionally, enhancing transparency and accountability in government processes can build public trust and reduce the reliance on impersonal algorithms. So while the idea of using algorithms to catch tax and welfare cheats may seem appealing, the real-world implications are deeply concerning. The Robodebt scandal in Australia and similar cases worldwide highlight the risks of relying on automated systems for such sensitive tasks. The push for efficiency should not come at the expense of fairness and humanity. Governments must tread carefully, ensuring that their methods do not inflict more harm than good. Texas is Building a NYSE Competitor… Here’s Why California Couldn’t Texas is making headlines with its ambitious plans to establish the Texas Stock Exchange (TXSE), aiming to create a new hub for financial trading in the Lone Star State. The TXSE promises to capitalize on Texas's business-friendly environment, attracting companies with its regulatory advantages and fostering a new financial ecosystem. We covered this entirely in a video if you want to learn more about it. But this raises an intriguing question: why isn't California, home to some of the biggest companies in the country, pursuing a similar path? California actually does have a stock exchange, though it's not widely known. The Pacific Stock Exchange (PSE), once a significant player in San Francisco, was bought by the Archipelago Exchange in 2005. This, in turn, was acquired by the New York Stock Exchange (NYSE) later that year. Today, the PSE is known as NYSE Arca, primarily recognized as a leader in the ETF space . Despite this niche success, NYSE Arca is still much smaller compared to the NYSE and NASDAQ, which raises the question: why hasn't California's exchange grown to rival its East Coast counterparts? If someone were to start a new stock exchange in California, they'd face stiff competition from NYSE Arca. However, several factors explain why California's exchange remains relatively small and why the state isn't seen as a prime candidate for a major new exchange. Firstly, the concept of first-mover advantage cannot be understated in the world of stock exchanges. Established exchanges like the NYSE and NASDAQ benefit from being the go-to platforms where everything is consolidated and operates efficiently. There's little incentive to fragment this system with additional exchanges, especially when the existing ones meet market needs so effectively. Moreover, California offers no better regulatory freedom for companies than Texas. In fact, California's stringent regulations and bureaucratic hurdles are often seen as a deterrent for financial institutions. The regulatory landscape in California is complex and can be challenging to navigate, making it less attractive for establishing a new exchange. Time zone differences also play a crucial role. The U.S. financial world operates on Eastern Time, and changing this would be difficult. A California-based exchange would stagger the start of trading times across the country, a big inconvenience for traders and investors. Additionally, having exchanges close at different times would lead to staggered earnings call times and other logistical challenges, complicating the financial landscape unnecessarily. In essence, the lack of a major stock exchange in California isn't due to a single factor but rather a combination of historical, regulatory, and logistical reasons. The established dominance of East Coast exchanges, combined with California's regulatory environment and time zone challenges, creates a scenario where starting a new major exchange in the state is not only difficult but also unnecessary. Texas, with its more business-friendly climate and strategic initiatives, is seizing an opportunity that California, despite its economic might, hasn't been positioned to take. Why Taxes Can’t Be Fixed Enjoy early access to the latest How Money Works video Copyright (C) 2024 Works Media Group LLC. All rights reserved. You are receiving this email because you opted in via our website. Our mailing address is: Works Media Group LLC 2261 Market Street #5209 San Francisco, CA 94114 USA Want to change how you receive these emails? You can update your preferences or unsubscribe |"
)

run1 = wait_on_run(run1, thread1)
resp = extract_message(get_response(thread1))

synthesizeSpeech(resp, "hello.mp3")