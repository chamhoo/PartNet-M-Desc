import sys
sys.path.append('/home/leech/3d/code/PartNet-M-Desc/dev')

import re
import os
import json
from tqdm import tqdm

from llm_utils import VLMSession
# from objectlog import SafeJSONHandler


shape_path = "/home/leech/3d/code/PartNet-M-Desc/shapes"
desc_path = "/home/leech/3d/code/PartNet-M-Desc/objects"
# os.mkdir(desc_path)

full_list = os.listdir(shape_path)
exsit_list = os.listdir(desc_path)

work_list = []
for path in full_list:
    idx, suffix = path.strip().split(".")
    if f"{idx}.json" not in exsit_list:
        work_list.append(path)

print(len(full_list))
print(len(exsit_list))
print(len(work_list))


for png_path in tqdm(work_list):
    idx, suffix = png_path.strip().split(".")
    if suffix == "png":
        prompt = """
            Please generate a dictionary based on the given object image, containing the following keys and corresponding descriptions. Generate each key step by step to ensure accuracy:

            1. "base_description": Provide a brief description in one short sentence, including the object's basic information such as size, shape, color, and style.Keep it within 10 words.
            2. "part_description": Focus on the object's parts information, including details of quantity, arrangement, shape, size, and position of each part. Keep it within 50 words.
            3. "internal_interaction_description": Describe the interactions specifically between the parts within the object. Limit this to around 100 words.
            4. "external_interaction_description": Explain the interactions of the object with external elements, such as other objects or people. Limit this to around 100 words.

            **IMPORTANT:** ONLY OUTPUT THE DICT
            """
        contents = [
            {"type": "text", "text": prompt}, 
            {"type": "image", "path": f"{shape_path}/{png_path}"}
        ]
        MODEL = "gpt-4o"
        obj_id = 0
        while True:
            session = VLMSession(MODEL, max_tokens=1024, temperature=0.5)
            hiertree = session.query(contents)
            del session
            # discard the 1st and last lines
            lines = hiertree.splitlines()
            modified_lines = lines[1:-1]
            hiertree = "\n".join(modified_lines)
            try:
                # change into dict
                json_dict = json.loads(hiertree)
                # check isvalid
                json.dumps(json_dict)
                break
            except:
                obj_id += 1
                if obj_id >= 10:
                    print(f"OBJ {idx} BREAK")
                    json_dict = "none"
                    break
        # save json
        json_path = f"{desc_path}/{idx}.json"
        with open(json_path, 'w') as file:
            json.dump(json_dict, file, indent=4)