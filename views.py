from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from .speech_processing import upload_audio_to_s3, transcribe_audio, analyze_sentiment, generate_audio_feedback

@api_view(["POST"])
def process_speech(request):
    if "audio" not in request.FILES:
        return JsonResponse({"error": "No audio file provided"}, status=400)

    audio_file = request.FILES["audio"]
    file_name = f"user_audio_{int(time.time())}.wav"

    # Upload audio to S3
    file_url = upload_audio_to_s3(audio_file, file_name)
    if not file_url:
        return JsonResponse({"error": "Failed to upload audio to S3"}, status=500)

    # Convert speech to text
    transcript = transcribe_audio(file_url)
    if transcript == "Error in transcription":
        return JsonResponse({"error": "Failed to transcribe audio"}, status=500)

    # Analyze sentiment
    sentiment = analyze_sentiment(transcript)

    # Generate AI voice feedback
    feedback_text = f"Your speech sentiment is {sentiment}. Try improving your pace and clarity."
    feedback_audio = generate_audio_feedback(feedback_text)

    response = HttpResponse(feedback_audio, content_type="audio/mpeg")
    response["Content-Disposition"] = 'attachment; filename="feedback.mp3"'
    
    return JsonResponse({
        "transcript": transcript,
        "sentiment": sentiment,
        "feedback_audio_url": request.build_absolute_uri(response["Content-Disposition"])
    })