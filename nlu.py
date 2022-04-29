from __future__ import unicode_literals, print_function

import json
from pathlib import Path

from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN

SAMPLE_DATASET_PATH = Path(__file__).parent / "data.json"

with SAMPLE_DATASET_PATH.open(mode= "r",encoding="utf8") as f:
    sample_dataset = json.load(f)

try:
    nlu_engine = SnipsNLUEngine.from_path("model")

except:
    print("Model not found. Creating new one")
    nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
    nlu_engine.fit(sample_dataset)

    nlu_engine.persist("model")

def classify(text):
    parsing = nlu_engine.parse(text)
    intent=parsing["intent"]["intentName"]
    
    if intent is None:
        intent=""
        
    try:
        slot= parsing["slots"][0]["value"]["value"]
    except:
        slot=""
    print("Intent: "+intent+", Slot: "+slot)

    
    return [intent,slot]