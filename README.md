# Text2WiktionarySpeech
This python script converts text to speech by searching for audio examples for the words on wiktionary

# Dependencies
```
pip install urllib beautifulsoup4 ffmpeg-generator
```
ffmpeg must be present in `PATH`

# Usage
```
python main.py [-h] [-i INPUT] [-o OUTPUT] [-l LANGUAGE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the input text
  -o OUTPUT, --output OUTPUT
                        the output file
  -l LANGUAGE, --language LANGUAGE
                        primary language
```

# Limitations
currently for languages only "de" is working consistently, 
but even then it can generate acceptable output for other languages with weird pronounciation
