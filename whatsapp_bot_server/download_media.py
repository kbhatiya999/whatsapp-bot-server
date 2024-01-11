import requests

url = "https://lookaside.fbsbx.com/whatsapp_business/attachments/?mid=1055239742395530&ext=1704975950&hash=ATs2gDdFSsoNbQa6TIM4WBqfaSp944_y3kxbnQvgq1JqtQ"

payload = {}
headers = {
  'Authorization': 'Bearer EAACkxeo4HFcBO4Hc4GCprG1h2Dsrh2ZCRqlSDFRHMw9ZBkevct6pysAiVuFzcxitReZAe3WgWoDqMNwZARfZADMQmBrZAWjHbVNCZCBZCBU7yuImLiXBZClTdipjBGJGSrpykQZBtfGBx04rLz2ke5EagkoWid6kd5ZAgBDD03ZBKpbUOLEVilaG5ZCmsK8JsEE0URoRiZBlNcOfk1yrD6MNgyTvS1'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

with open("downloaded_document.pdf", "wb") as file:
        file.write(response.content)
