# cleanvtt

A tiny Python script to convert .vtt transcripts into clean .txt files; removes timestamps, hashes, and redundant speaker labels, collapsing multi-line turns into single paragraphs for better accessibility.

## Usage
`python cleanvtt.py "transcript.vtt"`

> [!NOTE] This was built specifically using MS Teams output. VTT formats from other sources (e.g., Zoom) might require small regex adjustments to handle different speaker tag styles
