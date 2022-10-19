from memsource.memsource import Memsource
import json

memsourceAccount = Memsource("andraz_aikwit", "@9RiUIo8Jja&")

project_payload = {
        "name": "andraz test",
        "targetLangs": ["en", "de"]
    }

resp = memsourceAccount.create_project_from_template("6LXpNqyapZGbeJP8MCZ0r0", json.dumps(project_payload))
print(resp.text)