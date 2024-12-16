#!/usr/bin/env python

import argparse
from jinja2 import Environment, FileSystemLoader
import yaml
import os


def main(settings_yml_path :str):
    if not os.path.exists(settings_yml_path):
        print(f"File {settings_yml_path} does not exist")
        return

    with open(settings_yml_path, 'r') as fr:
        settings = yaml.safe_load(fr)

    # get the directory of settings_yml_path
    templates_dir = os.path.dirname(settings_yml_path)

    # Create the Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)

    # Load the template
    template = env.get_template(settings['root_template'])

    top_level_keys = []
    for tool_key in settings['globals']:
        top_level_keys.append(tool_key)

    for target_key in settings['targets']:
        target = settings['targets'][target_key]

        for tlk in top_level_keys:
            if tlk not in target:
                target[tlk] = settings['globals'][tlk]

        # Render the template with the data
        rendered_template = template.render(target)

        if settings['generate_output_path']:
            os.makedirs(os.path.dirname(target["targetfilepath"]), exist_ok=True)

        with open(target["targetfilepath"], "w") as fw:
            fw.write(rendered_template)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='dockertempl')
    parser.add_argument("-t", '--templ', type=str, help='template yaml file', default="dockerfiles.yaml")
    args = parser.parse_args()
    """
    infile = ""
    if len(sys.argv) < 2:
        if os.path.exists("dockerfiles.yaml"):
            print("using default file dockerfiles.yaml")
            infile = "dockerfiles.yaml"
        else:
            print("give me one argument with a yaml file, please")
            sys.exit(1)
    else:
        infile = sys.argv[1]
    """
    main(args.templ)
