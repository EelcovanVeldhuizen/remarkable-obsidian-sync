import json
import os
import re
import base64
import argparse
from io import BytesIO
from PIL.PngImagePlugin import PngImageFile
import dataclasses

# pip install pdf2image
import pdf2image

# pip install rmscene
from rmscene.scene_stream import read_blocks

# pip install rmc
from rmc.exporters.excalidraw import blocks_to_excalidraw
from rmc.exporters.excalidraw import ExcalidrawImageElement, ExcalidrawFile
from rmc.exporters.obsidian import excalidraw_to_obsidian

@dataclasses.dataclass()
class RemarkableTablet:
    SCREEN_WIDTH = 1404
    SCREEN_HEIGHT = 1872

def convert_image_to_base64_image(image: PngImageFile) -> str:
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_base64_str = base64.b64encode(buff.getvalue()).decode('ascii')

    return "data:image/png;base64,{image}".format(image=img_base64_str)

def convert_to_obsidian(remarkable_file:dict, excalidrawFileForBackground:ExcalidrawFile) -> str:
    with open(remarkable_file['remarkable'], 'rb') as f:
        blocks = read_blocks(f)
        excalidrawDocument = blocks_to_excalidraw(blocks)

        if excalidrawFileForBackground:
            # Add the file to document
            excalidrawDocument.addFile(excalidrawFileForBackground)

            # Set the dimensions and positions
            imageElement = ExcalidrawImageElement()
            imageElement.y = 60
            imageElement.x = -750
            imageElement.width = RemarkableTablet.SCREEN_WIDTH
            imageElement.height = RemarkableTablet.SCREEN_HEIGHT
            imageElement.fileId = excalidrawFileForBackground.id

            # Add the image to list of elements.
            # Background Elements need to be first in the elements list
            excalidrawDocument.elements.insert(0, imageElement)

        return excalidraw_to_obsidian(excalidrawDocument)

def clean_up_file_content(content: str) -> str:
    content = content.strip() # Pagedata sometimes have a lot of blank lines
    if content == "Blank": content = "" # Pagedata sometimes have the word Blank in them
    return content

def read_contents(filepath: str) -> dict:
    content = json.loads("{}")

    if os.path.isfile(filepath):
        f = clean_up_file_content(open(filepath, 'r').read())
        if f: content = json.loads(f)
    return content

def find_remarkables_files(uuid: str, remarkables_directory) -> list[str]:
    path = "{remarkables_directory}/{uuid}".format(remarkables_directory=remarkables_directory, uuid=uuid)
    files = [os.path.join(path, file) for file in os.listdir(path)]

    remarkable_files = filter(lambda d: d.endswith(".rm"), files)

    return list(remarkable_files)

def connect_name_to_remarkable_drawing(metadata: dict) -> str:
    return metadata["visibleName"]

def pagenumber_of_remarkable_drawing(content: dict, drawing: str) -> int:
    if "cPages" in content.keys():
        pages = [p['id'] for p in content['cPages']['pages']]
    else:
        pages = content["pages"]
    try:
        pagenumber = pages.index(os.path.basename(drawing).split(".")[0]) + 1
    except ValueError:
        print("Couldn't connect a name to remarkable file. Remarkable file: "+ drawing)
        pagenumber = None
    return pagenumber

def remarkable_has_background(content: dict) -> bool:
    return "pdf" in content['fileType']

def get_background_for_remarkable(remarkable: dict, directory: str, fileType="pdf") -> PngImageFile:


    path_to_pdf = "{remarkables_directory}/{filename}.{filetype}".format(remarkables_directory=directory,
                                                                          filename=remarkable['parent_uuid'],
                                                                          filetype=fileType)
    page_number = remarkable["pagenumber"]

    return pdf2image.convert_from_path(path_to_pdf, fmt="png",
                            first_page=page_number,
                            last_page=page_number,
                            size=(RemarkableTablet.SCREEN_WIDTH, RemarkableTablet.SCREEN_HEIGHT))[0]



def remarkables_to_convert(uuids: list[str], remarkables_directory: str) -> list[dict]:
    remarkables_to_convert = []

    for uuid in uuids:
        content = read_contents("{remarkables_directory}/{filename}.content".format(remarkables_directory=remarkables_directory, filename=uuid))
        metadata = read_contents("{remarkables_directory}/{filename}.metadata".format(remarkables_directory=remarkables_directory, filename=uuid))
        #pagedata = read_contents("{filename}.pagedata".format(filename=uuid)) # Seems to be useless files (for now)

        remarkable_drawings = find_remarkables_files(uuid, remarkables_directory)

        for drawing in remarkable_drawings:
            remarkable = dict()

            remarkable['filename'] = connect_name_to_remarkable_drawing(metadata)
            remarkable['pagenumber'] = pagenumber_of_remarkable_drawing(content, drawing)
            remarkable['background'] = remarkable_has_background(content)
            remarkable['remarkable'] = os.path.abspath(drawing)
            remarkable['parent_uuid'] = uuid

            remarkables_to_convert.append(remarkable)

    return remarkables_to_convert

def get_uuids_to_process(directory:str = "." ) -> list:
    # Get a list of directories
    directories = filter(lambda d: not d.endswith(".thumbnails"), [x[0] for x in os.walk(directory)])
    # Get the uuids and drop the "." at the beginning of the list
    uuids = [os.path.basename(x) for x in directories][1:]
    # Filter out any possible invalid files / directories that are not a uuid
    uuids = filter(lambda d: re.search(r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$', d), uuids)

    return list(uuids)

def get_ExcalidrawFile_to_use_as_background(remarkable: dict, remarkables_directory: str) -> ExcalidrawFile:
    background_image = get_background_for_remarkable(remarkable, remarkables_directory)
    return ExcalidrawFile(mimeType="image/png", dataURL= convert_image_to_base64_image(background_image))

def app(remarkables_directory, vault_directory) -> None:
    uuids = get_uuids_to_process(remarkables_directory)

    remarkables = remarkables_to_convert(uuids, remarkables_directory)

    for remarkable in remarkables:
        ExcalidrawFileAsBackground = None

        print("reading: "+remarkable['remarkable'])

        if remarkable["background"] and remarkable["pagenumber"]:
            ExcalidrawFileAsBackground = get_ExcalidrawFile_to_use_as_background(remarkable, remarkables_directory)

        obsidian_markdown = convert_to_obsidian(remarkable, ExcalidrawFileAsBackground)

        file_path = "{vault_directory}/{filename}-page-{pagenumber}.md".format(vault_directory = vault_directory,
                                                                             filename=remarkable["filename"],
                                                                             pagenumber=remarkable["pagenumber"])
        with open(file_path, 'w') as f:
            print("writing: "+file_path)
            f.write(obsidian_markdown)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Remarkable To Obsidian Synchronization',
                    description='Creates Excalidraw Markdown files to be used in Obsidian')
    parser.add_argument('-i', '--input-dir', type=str, default="/app/remarkables", dest='input_dir')
    parser.add_argument('-o', '--output-dir', type=str, default="/app/vault", dest='output_dir')
    args = parser.parse_args()

    app(args.input_dir, args.output_dir)

