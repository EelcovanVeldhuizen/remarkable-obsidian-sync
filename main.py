import json
import os
import re

from rmscene.scene_stream import read_blocks
from rmc.exporters.excalidraw import blocks_to_excalidraw
from rmc.exporters.obsidian import excalidraw_to_obsidian


def convert_to_obsidian(remarkable_file) -> str:
    with open(remarkable_file['remarkable'], 'rb') as f:
        blocks = read_blocks(f)
        excalidrawDocument = blocks_to_excalidraw(blocks)
        
        return excalidraw_to_obsidian(excalidrawDocument)

def clean_up_file_content(content: str) -> str:
    content = content.strip() # Pagedata sometimes have a lot of blank lines
    if content == "Blank": content = "" # Pagedata sometimes have the word Blank in them
    return content

def read_contents(filepath: str) -> dict:
    content = json.loads("{}")
    print(filepath)
    if os.path.isfile(filepath):
        f = clean_up_file_content(open(filepath, 'r').read())
        if f: content = json.loads(f)
    return content

def find_remarkables_files(uuid: str, remarkables_directory) -> list[str]:
    path = "{remarkables_directory}/{uuid}".format(remarkables_directory=remarkables_directory, uuid=uuid)
    files = [os.path.join(path, file) for file in os.listdir(path)]
    
    remarkable_files = filter(lambda d: d.endswith(".rm"), files)
    
    return list(remarkable_files)

def connect_name_to_remarkable_drawing(content: dict, metadata: dict, remarkables: list) -> list[dict]:
    remarkable_files_to_process = []
    
    filename =  metadata["visibleName"]
    
    if "cPages" in content.keys():
        pages = [p['id'] for p in content['cPages']['pages']]
    else:
        pages = content["pages"]

        
    for remarkable in remarkables:
        file_to_process = dict()
        
        pagenumber = pages.index(os.path.basename(remarkable).split(".")[0]) + 1
        
        file_to_process["filename"] = "{filename}-page-{pagenumber}.md".format(filename=filename, pagenumber=pagenumber)
        file_to_process["remarkable"] = os.path.abspath(remarkable)
        
        remarkable_files_to_process.append(file_to_process)

    return remarkable_files_to_process



def remarkables_to_convert(uuids: list[str], remarkables_directory: str):
    rms_to_convert = []
    
    for uuid in uuids:
        content = read_contents("{remarkables_directory}/{filename}.content".format(remarkables_directory=remarkables_directory, filename=uuid))
        metadata = read_contents("{remarkables_directory}/{filename}.metadata".format(remarkables_directory=remarkables_directory, filename=uuid))
        #pagedata = read_contents("{filename}.pagedata".format(filename=uuid)) # Seems to be useless files (for now)
        
        remarkable_drawings = find_remarkables_files(uuid, remarkables_directory)
        remarkables = connect_name_to_remarkable_drawing(content, metadata, remarkable_drawings)
        # Flatten the list
        for r in remarkables:
            rms_to_convert.append(r)
    
    return rms_to_convert

def get_uuids_to_process(directory:str = "." ) -> list:
    # Get a list of directories     
    directories = filter(lambda d: not d.endswith(".thumbnails"), [x[0] for x in os.walk(directory)])
    # Get the uuids and drop the "." at the beginning of the list
    uuids = [os.path.basename(x) for x in directories][1:]
    # Filter out any possible invalid files / directories that are not a uuid
    uuids = filter(lambda d: re.search(r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$', d), uuids)

    return list(uuids)

def app(remarkables_directory="/app/remarkables", vault_directory="/app/vault"):
    uuids = get_uuids_to_process(remarkables_directory)
    
    remarkables = remarkables_to_convert(uuids, remarkables_directory)
    
    for rm in remarkables:
        print("reading: "+rm['remarkable'])
        obsidian_markdown = convert_to_obsidian(rm)
        with open("{vault_directory}/{filename}".format(vault_directory = vault_directory, filename=rm["filename"]), "w") as f:
            print("writing: "+rm["filename"])
            f.write(obsidian_markdown)


if __name__ == "__main__":
    app()
