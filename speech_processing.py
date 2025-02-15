import boto3
import json
import time
from django.conf import settings

# Initialize AWS Clients
s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

transcribe_client = boto3.client(
    "transcribe",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

comprehend_client = boto3.client(
    "comprehend",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

polly_client = boto3.client(
    "polly",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

def upload_audio_to_s3(file, file_name):
    """Upload audio file to AWS S3"""
    try:
        s3_client.upload_fileobj(file, settings.AWS_S3_BUCKET, file_name)
        file_url = f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"
        return file_url
    except Exception as e:
        print(f"S3 Upload Error: {e}")
        return None

def transcribe_audio(file_url):
    """Convert speech to text using Amazon Transcribe"""
    job_name = f"transcribe_{int(time.time())}"
    
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_url},
        MediaFormat="wav",
        LanguageCode="en-US",
        OutputBucketName=settings.AWS_S3_BUCKET
    )

    while True:
        status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if status["TranscriptionJob"]["TranscriptionJobStatus"] in ["COMPLETED", "FAILED"]:
            break
        time.sleep(5)

    if status["TranscriptionJob"]["TranscriptionJobStatus"] == "FAILED":
        return "Error in transcription"

    transcript_url = status["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    transcript_data = json.loads(s3_client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=transcript_url.split("/")[-1])["Body"].read())
    return transcript_data["results"]["transcripts"][0]["transcript"]

def analyze_sentiment(text):
    """Analyze sentiment using Amazon Comprehend"""
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]

def generate_audio_feedback(text):
    """Generate AI voice feedback using Amazon Polly"""
    response = polly_client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    audio_stream = response["AudioStream"].read()
    return audio_stream