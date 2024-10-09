import feedparser
import re

result = []

TideFeed = feedparser.parse("https://www.tidetimes.co.uk/rss/folkestone-tide-times")

entry = TideFeed.entries

summary = entry[0].summary
# print(summary)

data = re.split('<br />',summary)
data.pop(0) # Remove summary data
data.pop(-1) # Remove empty value
# print(data)

for item in data:
    bits = re.split(" ",item)
    bits[1] = (bits[1].split(":"))[1]+":"+(bits[1].split(":"))[2]
    result.append({"height": bits[2], "time": bits[1]+":", "type": bits[0]})

final = {"data": result}
print(final)