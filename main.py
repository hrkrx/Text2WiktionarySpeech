import ffmpeg
import argparse
import urllib.request
from bs4 import BeautifulSoup

wiktionaryUrl = "wiktionary.org/wiki/"

def main(args):
    if args.input is None:
        words = ["no", "data", "this", "is", "a", "Test"]
    else:
        words = args.input.split()
    print(words)
    
    links = []

    for word in words:
        print("Searching for", word)
        link = get_wiktionary_audio(word, args.language)
        print(link)
        links.append(link)

    curStream = None
    streams = []
    for link in links:
        if link == "" or link == None:
            continue
        if curStream == None:
            curStream = ffmpeg.input(link)
        else:
            streams.append(ffmpeg.input(link))

    curStream.concat(*streams, v=0, a=1).silenceremove(1, 0, "-20dB").output(args.output).run()

def get_wiktionary_audio(word, lang):
    lowerCaseWord = word.lower()
    capCaseWord = word.lower().capitalize()

    usedWord = word

    wiktionaryBaseUrl = "https://" + lang + "." + wiktionaryUrl

    try:
        lowerResponse = urllib.request.urlopen(wiktionaryBaseUrl + usedWord)
        content = lowerResponse.read()
        soup = BeautifulSoup(content, "html.parser")
        links = soup.find_all("a", "internal")
        if len(links) < 1:
            raise Exception("no audio link found") 
    except:
        try:
            lowerResponse = urllib.request.urlopen(wiktionaryBaseUrl + lowerCaseWord)
            content = lowerResponse.read()
            usedWord = lowerCaseWord
            soup = BeautifulSoup(content, "html.parser")
            links = soup.find_all("a", "internal")
            if len(links) < 1:
                raise Exception("no audio link found")
        except:
            try:
                capResponse = urllib.request.urlopen(wiktionaryBaseUrl + capCaseWord)
                content = capResponse.read()
                usedWord = capCaseWord
                soup = BeautifulSoup(content, "html.parser")
                links = soup.find_all("a", "internal")
            except:
                print(word, " could not be found")
                return None

    chosenLink = next(f for f in links if "ogg" in f["href"])
    return "https:" + chosenLink["href"]
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=False, help="the input text" )
    parser.add_argument("-o", "--output", type=str, required=False, default="out.ogg", help="the output file" )
    parser.add_argument("-l", "--language", type=str, required=False, default="de", help="primary language" )
    args = parser.parse_args()

    main(args)