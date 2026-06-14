# YouTube to Blog Converter

**Difficulty**: Beginner-Intermediate  
**Time**: 30-45 minutes  
**Learning Focus**: API integration, text processing, content repurposing  
**Module**: chat

## Overview

Create a tool that converts YouTube video transcripts into well-formatted blog posts using AI. This project helps students understand how to extract data from one format and transform it into another valuable piece of content.

## Instructions

```python
import re
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from hands_on_ai.chat import get_response

def youtube_to_blog():
    """Convert YouTube video transcripts into blog post content using AI."""
    print("=== YouTube to Blog Converter ===")
    print("This tool extracts a transcript from a YouTube video and converts it to a blog post.")
    
    # Get video URL or ID
    video_input = input("Enter YouTube video URL or video ID: ")
    
    # Extract video ID from URL if needed
    video_id = extract_video_id(video_input)
    
    if not video_id:
        print("Error: Could not extract a valid YouTube video ID.")
        return
    
    print(f"Processing video ID: {video_id}")
    
    # Get transcript
    try:
        transcript = get_transcript(video_id)
        if not transcript:
            return
    except Exception as e:
        print(f"Error getting transcript: {e}")
        return
    
    # Get video metadata if needed
    video_title = input("Enter video title (or press Enter to skip): ")
    video_author = input("Enter video creator/channel name (or press Enter to skip): ")
    
    # Get blog style preferences
    print("\nBlog Style Options:")
    print("1. Informational/Educational")
    print("2. Conversational/Casual")
    print("3. Professional/Formal")
    print("4. Tutorial/How-To")
    
    style_choice = input("Select a style (1-4): ")
    
    if style_choice == "1":
        blog_style = "informational"
    elif style_choice == "2":
        blog_style = "conversational"
    elif style_choice == "3":
        blog_style = "professional"
    elif style_choice == "4":
        blog_style = "tutorial"
    else:
        print("Invalid choice. Using informational style.")
        blog_style = "informational"
    
    # Get additional context
    topic_keywords = input("Enter 3-5 keywords related to the video (comma separated): ")
    
    # Get intended audience
    audience = input("Who is the target audience for this blog post? ")
    
    # Generate blog post with AI
    generate_blog_post(transcript, video_title, video_author, blog_style, topic_keywords, audience)

def extract_video_id(video_input):
    """Extract the YouTube video ID from a URL or return the ID if already provided."""
    # Check if it's already a video ID (simple 11-character string)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', video_input):
        return video_input
        
    # Try to extract from URL
    youtube_regex = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(youtube_regex, video_input)
    
    if match:
        return match.group(1)
    
    return None

def get_transcript(video_id):
    """Get the transcript from a YouTube video."""
    try:
        # Note: youtube-transcript-api changed its API across versions. This uses
        # the classic call; on newer versions use
        # `YouTubeTranscriptApi().fetch(video_id)` and access `snippet.text`.
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all transcript segments
        full_transcript = " ".join([item['text'] for item in transcript_list])
        
        # Print a preview
        preview_length = min(150, len(full_transcript))
        print(f"\nTranscript preview ({len(full_transcript)} characters):")
        print(f"{full_transcript[:preview_length]}...")
        
        return full_transcript
    
    except Exception as e:
        print(f"Error: Could not retrieve transcript. {str(e)}")
        print("Possible reasons:")
        print("- The video might not have closed captions/subtitles")
        print("- The video ID might be incorrect")
        print("- The video owner may have disabled transcript access")
        return None

def generate_blog_post(transcript, title, author, style, keywords, audience):
    """Generate a blog post from the transcript using AI."""
    print("\nGenerating blog post...")
    
    # Create a prompt for the AI
    prompt = f"""
    Convert this YouTube video transcript into a well-structured blog post:
    
    VIDEO INFORMATION:
    Title: {title if title else "Not provided"}
    Creator: {author if author else "Not provided"}
    Style: {style}
    Keywords: {keywords}
    Target Audience: {audience}
    
    TRANSCRIPT:
    {transcript[:4000]}  # Limit transcript length if needed
    
    Please create a complete blog post with:
    1. An engaging headline/title
    2. Introduction that hooks the reader
    3. Well-structured sections with subheadings
    4. Conclusion or call-to-action
    5. Add relevant statistics or examples where appropriate
    
    Format the post using markdown syntax for headings, lists, etc.
    The tone should be {style} and appropriate for the specified audience.
    Expand on any concepts from the video that need more explanation.
    Add 3-5 relevant tags at the end of the post.
    
    Length: Aim for ~1000-1500 words.
    """
    
    try:
        # Generate blog post using the prompt
        blog_post = get_response(prompt)
        
        # Save the blog post to a file
        filename = f"blog_post_{title.replace(' ', '_')[:30] if title else 'from_youtube'}.md"
        with open(filename, 'w') as f:
            f.write(blog_post)
        
        print(f"\nBlog post successfully generated and saved to: {filename}")
        
        # Print a preview of the blog post
        preview_lines = blog_post.split('\n')[:10]
        print("\nBlog Post Preview:")
        print("\n".join(preview_lines) + "\n...")
        
    except Exception as e:
        print(f"Error generating blog post: {e}")

if __name__ == "__main__":
    youtube_to_blog()
```

## Extension Ideas

- Add support for multiple languages and translation
- Implement a social media post generator from the same content
- Create a scheduler to process videos in batch
- Add image extraction from video thumbnails or frames
- Build a web interface with Flask or Streamlit
- Implement SEO optimisation suggestions for the generated content

---