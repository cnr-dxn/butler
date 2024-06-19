import requests # type: ignore
import os
import sys
from typing import *
import datetime
from bs4 import BeautifulSoup
from openai import OpenAI # type: ignore
import boto3
from time import sleep 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *
from MainFunctions import *

#-------------------------------------------------------------------------------------------------
# Direct OpenAI Functions
def synthesizeSpeech(text, output_file):
    # Initialize a session using Amazon Polly
    polly = boto3.openai_client('polly')

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
def extractMessage(messages):
    for m in messages:
        if (m.role).lower() == "assistant":
            return m.content[0].text.value

def waitOnRun(run, thread):
    seconds = 0
    while run.status == "queued" or run.status == "in_progress":
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        print(f"\rwaiting for {str(seconds).zfill(2)} seconds with status: {run.status}", end='', flush=True)
        sleep(1)
        seconds += 1
    print(f"\rwaiting for {str(seconds).zfill(2)} seconds with status: {run.status}", end='', flush=True)
    print()
    return run

def submitMessage(assistant_id, thread, user_message, tokens = max_assistant_answer_tokens):
    openai_client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        max_completion_tokens = tokens
    )

def getResponse(thread):
    return openai_client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def summarizeNewslettersWithSystem(input_script, tokens = max_assistant_answer_tokens):
    thread = openai_client.beta.threads.create()
    run = submitMessage(asst_id, thread, input_script)
    return thread, run

def createGreeting():
    thread = openai_client.beta.threads.create()
    run = submitMessage(greeter_id, thread, "go")
    return thread, run


#-------------------------------------------------------------------------------------------------
# Connor's ChatGPT Functions
def retrieveSummary(raw_input: str, real: bool = False) -> str:
    if ~real:
        print("not real")
        reversed = raw_input[::-1]
        return reversed[:500]
    else:
        print("real")
        thread1, run1 = summarizeNewslettersWithSystem(raw_input)
        run1 = waitOnRun(run1, thread1)
        return extractMessage(getResponse(thread1)).replace("Summary:\n", "")

def retrieveGreeting(real: bool = False):
    if ~real:
        print("not real")
        return "Good morning. It's whatever day it is. Let's dive into whatever we're going to dive into."
    else:
        print("real")
        thread1, run1 = createGreeting()
        run1 = waitOnRun(run1, thread1)
        return extractMessage(getResponse(thread1))

def breakFunction():
    print("ill get to this later")
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# MySQL Functions
def selectMailBySender(sender: str, connection = main_connection):
    query = """
        SELECT sender, subject, body, received_date 
            FROM entries 
            WHERE sender = %s
            AND used = false;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (sender, ))
            results = cursor.fetchall()
    except Exception as e:
        breakLine(False)
        print(f"[ERROR] get_recent_ids: unsuccessful due to {e}")
        breakLine()
        return []
#-------------------------------------------------------------------------------------------------

def mainLoop():
    master_script = ""
    '''
    master script should be something like:
    "Hello there! Today is {}. You have {} messages today, let's break them down.
    From Radio Free Mobile: {connor-generated-name}:
    <summary>
    From How Money Works: {connor-generated-name}:
    <summary>
    No new messages from Connor Dixon recently
    Have an excellent day sir!
    '''
    print(retrieveGreeting())

'''
Could not process parameters: str(news@compoundeddaily.com), it must be of type list, tuple or dict
'''