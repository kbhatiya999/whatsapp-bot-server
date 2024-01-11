from pprint import pprint
import xmltodict

# XML string to parse
xml_string = """<?xml version='1.0' encoding='UTF-8'?>
<feed
    xmlns:yt="http://www.youtube.com/xml/schemas/2015"
    xmlns="http://www.w3.org/2005/Atom">
    <link rel="hub" href="https://pubsubhubbub.appspot.com"/>
    <link rel="self" href="https://www.youtube.com/xml/feeds/videos.xml?channel_id=UCeNA8ia-eYKh7JYBfh2esGA"/>
    <title>YouTube video feed</title>
    <updated>2023-12-26T17:17:08.049169056+00:00</updated>
    <entry>
        <id>yt:video:kmm0rM5vsAU</id>
        <yt:videoId>kmm0rM5vsAU</yt:videoId>
        <yt:channelId>UCeNA8ia-eYKh7JYBfh2esGA</yt:channelId>
        <title>2</title>
        <link rel="alternate" href="https://www.youtube.com/watch?v=kmm0rM5vsAU"/>
        <author>
            <name>Kashish Bhatia</name>
            <uri>https://www.youtube.com/channel/UCeNA8ia-eYKh7JYBfh2esGA</uri>
        </author>
        <published>2023-12-26T17:09:21+00:00</published>
        <updated>2023-12-26T17:17:08.049169056+00:00</updated>
    </entry>
</feed>"""

# Parse the XML string
parsed_xml = xmltodict.parse(xml_string)
data = parsed_xml['feed']['entry']
channel_id = data.get('yt:channelId')
video_id = data.get('yt:videoId')
print(f'{channel_id=}, {video_id=}')

