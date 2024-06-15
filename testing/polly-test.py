import boto3

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

script = """Hello Everyone. 
            Welcome back to Movie Recaps. 
            Today I will show you an action movie from 2001, titled Parker is a bitch. 
            Spoilers ahead.
            Watch out, and, take care"""

synthesizeSpeech(script, "hello.mp3")