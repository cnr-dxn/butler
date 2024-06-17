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
def extract_message(messages):
    for m in messages:
        if (m.role).lower() == "assistant":
            return m.content[0].text.value

def wait_on_run(run, thread):
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

def submit_message(assistant_id, thread, user_message):
    openai_client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        max_completion_tokens = max_assistant_answer_tokens
    )

def get_response(thread):
    return openai_client.beta.threads.messages.list(thread_id=thread.id, order="asc")

def summarize_newsletters_with_system(input_script, tokens = 1000):
    thread = openai_client.beta.threads.create()
    run = submit_message(asst_id, thread, input_script)
    return thread, run

#-------------------------------------------------------------------------------------------------
# ChatGPT Functions
def turnToGPTResponse(raw_input: str, real: bool = False) -> str:
    if ~real:
        print("not real")
        reversed = raw_input[::-1]
        return reversed[:500]
    else:
        print("real")
        summarize_newsletters_with_system(raw_input)

def createGreeting():
    return "Good morning. its whatever day it is"

def breakFunction():
    print("ill get to this later")
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
# MySQL Functions
def selectMailBySender(sender: str, connection = main_connection):
    query = """
        SELECT sender, subject, received_date 
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
    print(results)
#-------------------------------------------------------------------------------------------------

'''
Could not process parameters: str(news@compoundeddaily.com), it must be of type list, tuple or dict
'''