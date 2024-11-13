import feedparser
import re

def tidetimesUK():
    result = []

    #TideFeed = feedparser.parse("https://www.tidetimes.co.uk/rss/folkestone-tide-times")
    # RSS feed in XML
    TideFeed = feedparser.parse("https://www.tidetimes.org.uk/folkestone-tide-times.rss")

    entry = TideFeed.entries

    summary = entry[0].description #.summary
    # print(summary)

    data = re.split('<br />',summary)
    print(data)
    data.pop(0) # Remove summary data
    data.pop(-1) # Remove empty value
    # print(data)

    for item in data:
        bits = re.split(" ",item)
        bits[1] = (bits[1].split(":"))[1]+":"+(bits[1].split(":"))[2]
        result.append({"height": bits[2], "time": bits[1]+":", "type": bits[0]})

    final = {"data": result}
    return final

if __name__ == "__main__":
    print(tidetimesUK())