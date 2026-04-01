import re
import sys
import os

def clean_vtt(input_path):
    """
    converts VTT (optimized for ms teams) to plain text:
    - Retains speakers
    - Removes timestamps, IDs, and tags
    - Collapses multi-line turns from the same speaker
    """
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    output = []
    current_speaker = None
    current_speech = []

    # patterns
    timestamp_pattern = re.compile(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}')
    speaker_tag_pattern = re.compile(r'<v ([^>]+)>(.*)')
    any_tag_pattern = re.compile(r'<[^>]+>')
    id_pattern = re.compile(r'^[a-f0-9\-]+/\d+-\d+$')

    def flush(speaker, speech_list):
        if speaker and speech_list:
            text = " ".join(speech_list).strip()
            # redundant merge spaces
            text = re.sub(r'\s+', ' ', text)
            if text:
                output.append(f"{speaker}: {text}")

    for line in lines:
        line = line.strip()
        
        # metadata/formatting
        if not line or line == 'WEBVTT' or timestamp_pattern.match(line) or id_pattern.match(line):
            continue

        speaker_match = speaker_tag_pattern.search(line)
        if speaker_match:
            new_speaker = speaker_match.group(1)
            text = speaker_match.group(2)
            text = any_tag_pattern.sub('', text).strip()
            
            if new_speaker == current_speaker:
                if text:
                    current_speech.append(text)
            else:
                flush(current_speaker, current_speech)
                current_speaker = new_speaker
                current_speech = [text] if text else []
        else:
            # continuation line
            text = any_tag_pattern.sub('', line).strip()
            if text:
                current_speech.append(text)

    flush(current_speaker, current_speech)

    output_path = os.path.splitext(input_path)[0] + ".txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output))
    
    print(f"Cleaned output saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python cleanvtt.py <file.vtt>")
    else:
        clean_vtt(sys.argv[1])
