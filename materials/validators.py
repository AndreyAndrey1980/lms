from rest_framework import serializers


def validate_video_url(url):
    if "https://www.youtube.com" not in url:
        raise serializers.ValidationError("url must be from youtube video")
