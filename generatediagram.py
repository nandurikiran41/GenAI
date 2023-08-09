import os
from plantuml import PlantUML

def generate_class_diagram(source_folder, output_file):
    uml_code = "@startuml\n"
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".cs"):
                class_name = os.path.splitext(file)[0]
                uml_code += f"class {class_name} {{}}\n"
                print(uml_code)

    uml_code += "@enduml\n"

    plantuml = PlantUML()
    plantuml.processes_file(uml_code, output_file)

if __name__ == "__main__":
    source_folder = "D:\Rawdata\sample_csharp-main\API"
    output_file = "class_diagram.png"
    generate_class_diagram(source_folder, output_file)
