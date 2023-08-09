import os
import subprocess
import plantuml
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.requests import Request
import openai
from plantuml import PlantUML
import time
import os


openai.api_key_path = r'D:\Rawdata\apikey.txt'

# prompt=f"Generate a PlantUML Entity Relationship diagram:{s}"


# Create an instance of the FastAPI class
app = FastAPI()


def get_completion(prompt, model="gpt-3.5-turbo-0613"):
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

        model=model,

        messages=messages,

        temperature=0,

    )

    return response.choices[0].message["content"]


def generatediagram(query,content):
    prompt = f"Generate a PlantUML {query} diagram:{content}"
    res = get_completion(prompt)
    return res

def generatecontent(query,content):
    prompt = f"{query}:{content}"
    text = get_completion(prompt)
    return text


@app.get("/codeanalysis")
def generate_class_diagram(query, source_folder: str, out_path: str):
    # response=""
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".cs"):
                class_name = os.path.splitext(file)[0]
                f = open(os.path.join(root, file), "r")
                s = f.read()
                if "Class" in query or "UML" in query or "Sequence" in query:
                    response = generatediagram(query, s)
                    output_path = f"{out_path}\\{class_name}{query}.puml"
                    with open(output_path, "w") as image:
                        image.write(response)
                    subprocess.run(["java", "-jar", r'D:\plantml\plantuml-jar-gplv2-1.2023.7\plantuml.jar', output_path],
                        check=True)
                    image_path = f"{out_path}\\{class_name}{query}.png"
                else:
                    prompt = f"{query}:{s}"
                    content = generatecontent(query, s)
                    output_path = f"{out_path}\\{class_name}{query}.txt"
                    with open(output_path, "w") as text:
                        text.write(content)

            # Replace with the actual path to your image
    # return FileResponse(image_path, media_type="image/jpeg")
    return{"response": {"content generated"}}
