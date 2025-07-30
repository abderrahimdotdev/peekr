#!/usr/bin/env python


    
import getopt
import locale
import os
import sys
import timeit
import filetype
import cv2
import pytesseract
from texttable import Texttable

class MessageDisplay:
    MESSAGES = {
        "en":{
            "prompts":{
                "pictures_directory":"Path to the pictures directory : ",
                "recursive":"You want to perform a recursive search ? [Y]es / [N]o",
                "keywords":"Type your keyword(s) separated by a comma [,]: ",
                "case-sensitive":"Do you want to perform a case-sensitive search ? [Y]es / [N]o",
                "lang":"Choose your desired language: ",
                "output":"Where would you like to copy the pictures found, if any: ",
                "valid_answers":{
                    "all": ["y", "yes", "no", "n"],
                    "yes": ["yes", "y"],
                    "no": ["no", "n"]
                }
            },
            "errors":{
                "pictures_directory_not_found_interactive":"Directory not found. Please try again.",
                "pictures_directory_not_found_batch":"Directory not found. Aborting.",
                "empty_keywords":"At lease 1 keyword is required.",
                "case-sensitive":"Invalid Answer. Type [Y] for case-sensitive search, [N] or leave blank for case-insensitive search.",
                "recursive":"Please select [Y]es or [N]o.",
                "lang":"Invalid Answer. The chosen language is not supported.",
                "output":"Directory already exists.",
                "yes_no":"Type [Y] for Yes or [N] for No.",
            },
            "labels":{
                "headline":"Summary",
                "total_pictures":"Total pictures scanned:\t\t",
                "runtime":"Estimated runtime:\t\t",
                "keyword":"Keyword",
                "keyword_found":"Found in",
                "picture":"picture",
                "pictures":"pictures",
                "pictures_found":"Found keyword \"{}\" in {} pictures.",
                "see_results":"Would you like to see the results ? [Yes/No] ",
            }
        },
        "fr":{
            "prompts":{
                "pictures_directory":"Chemin du répertoire qui contient les images ",
                "recursive":"Voulez-vous effectuer une recherche recursive ? [O]ui / [N]on",
                "keywords":"Tapez les mots-clés que vous recherchez",
                "case-sensitive":"Voulez-vous effectuer une recherche sensible à la case ? [O]ui / [N]on",
                "lang":"Language utilisé dans la recherche [fr]",
                "output":"Le répertoire du destination des images",
                "valid_answers":{
                    "all": ["oui", "non", "o", "n"],
                    "yes": ["oui", "o"],
                    "no": ["non", "n"]
                }
            },
            "errors":{
                "pictures_directory_not_found_interactive":"Chemin du dosser introuvable. Veuileez réessayer.",
                "pictures_directory_not_found_batch":"Chemin du dosser introuvable.",
                "empty_keywords":"Vous devez saisir un mot à rechercher.",
                "case-sensitive":"Réponses non valide. Tapez [O] pour une recherche sensible à la case, [N] ou laisser vide pour une rechercher non-sensible à la case .",
                "recursive":"Merci de choisir entre [O]ui ou [N]on.",
                "lang":"Réponse invalide. La langue choisi n'est pas supporté.",
                "output":"Dossier existe déja.",
                "yes_no":"Taper [O] pour Oui, [N] pour Non.",
            },
            "labels":{
                "headline":"Résultat",
                "total_pictures":"Nombre des images scanné(s):\t\t",
                "runtime":"La recherche a pris:\t\t",
                "keyword":"Mot-clé",
                "keyword_found":"Trouvé dans",
                "picture":"image",
                "pictures":"images",
                "pictures_found":"Le mot \"{}\" existe dans {} images.",
                "see_results":"Voulez-vous voir le résultat ? [Oui/Non] "
            }
        },
        
        "dr":{
            "prompts":{
                "pictures_directory":"Fin kaynin tsawrk ? ",
                "recursive":"Bghiti t9alab f wst lmilafat li ldakhl ?",
                "keywords":"3layach kat9alab ?",
                "case-sensitive":"Kayhmk lfar9 bin minuscule w majuscule ? [W]ah / [L]a",
                "lang":"Dakchi li kat9leb 3lih b achmen logha ?",
                "output":"Ila bano chi tsawr, fin bghiti ncopyhom ?",
                "valid_answers":{
                    "all": ["wah", "la", "w", "l"],
                    "yes": ["wah", "w"],
                    "no": ["la", "l"]
                }
            },
            "errors":{
                "pictures_directory_not_found_interactive":"Directory not found. Please try again.",
                "pictures_directory_not_found_batch":"Directory not found. Aborting.",
                "empty_keywords":"Makaymknch tb9a khawya, khas 3el a9al chi kelma t9lb 3liha.",
                "case-sensitive":"Invalid Answer. Type [Y] for case-sensitive search, [N] or leave blank for case-insensitive search.",
                "lang":"Invalid Answer. The chosen language is not supported.",
                "recursive":"Wah wla La ?",
                "output":"Directory already exists.",
                "yes_no":"Ktab [W] bach tgol [Wah], [L] bach tgol [La].",
            },
            "labels":{
                "headline":"Lkholasa",
                "total_pictures":"3adad dial tsawr:\t\t",
                "keyword":"Lkalima",
                "keyword_found":"Kayna f",
                "picture":"tswira",
                "pictures":"tsawr",
                "runtime":"Lmouda dial lba7t:\t\t",
                "pictures_found":"Kayna kalimat \"{}\" f {} tswira.",
                "see_results":"Bghiti tchof natija ? [Wah/La] "
            }
        }
    }
    
    @staticmethod
    def prompt(key:str):
        return MessageDisplay.MESSAGES[OPTIONS["ui-lang"]]['prompts'][key]
    @staticmethod
    def error(key:str):
        return MessageDisplay.MESSAGES[OPTIONS["ui-lang"]]['errors'][key]
    @staticmethod
    def label(key:str):
        return MessageDisplay.MESSAGES[OPTIONS["ui-lang"]]['labels'][key]


OPTIONS: dict[str,str] = {
        # Default options
        "ui-lang": locale.getlocale()[0].split("_")[0],
        "lang":"eng",
        "interacetive":False,
        "case-sensitive":False,
        "recursive":False,
        }

class InteractiveArgsHandler:

    def run(self,options:dict[str,str]):
        self.__get_images_folder(options)
        self.__get_recursive_search(options)
        self.__get_keywords(options)
        self.__is_case_sensitive(options)
        

    def __get_images_folder(self,options:dict[str,str]):
        print_headline(MessageDisplay.prompt('pictures_directory'))
        images_directory = normalize_path(input(">> ").strip("'").strip("\""))
        while len(images_directory) == 0 or not os.path.isdir(f"{images_directory}"):
            print(MessageDisplay.error('pictures_directory_not_found_interactive'))
            images_directory = input(">> ").strip(" ").strip("'").strip("\"")
        print()
        options["directory"] = images_directory

    def __get_keywords(self,options:dict[str,str]):
        print_headline(MessageDisplay.prompt('keywords'))
        keywords = input(">> ").strip(" ")
        while len(keywords) == 0:
            print(MessageDisplay.error('keywords'))
            keywords = input(">> ").strip(" ")
        keywords = keywords.split(",")
        if "" in keywords:
            keywords.remove("")
        options["keywords"] = keywords
        print()

    def __is_case_sensitive(self,options:dict[str,str]):
        print_headline(MessageDisplay.prompt('case-sensitive'))
        options["case-sensitive"] = False
        answer = input(">> ").strip(" ").lower()
        while answer not in MessageDisplay.prompt("valid_answers").get("all"):
            print(MessageDisplay.error('case-sensitive'))
            answer = input(">> ").strip(" ").lower()
        if answer in MessageDisplay.prompt("valid_answers").get("yes"):
            options["case-sensitive"] = False
        print()
        
    def __get_recursive_search(self, options:dict[str, str]):
        print_headline(MessageDisplay.prompt('recursive'))
        answer = input(">> ").strip(" ").lower()
        while answer not in MessageDisplay.prompt("valid_answers").get("all"):
            print(MessageDisplay.error('recursive'))
            answer = input(">> ").strip(" ").lower()
        if answer in MessageDisplay.prompt("valid_answers").get("yes"):
            options["recursive"] = True
        print()
    
        
    
    

def normalize_path(path:str):
    return os.path.expanduser(os.path.normpath(path))

def init_args(options:dict[str,str]):
    
    args = extract_cli_args()
    
    for opt, val in args:
        match opt:
            case "-I" | "--interactive":
                interactive_manager = InteractiveArgsHandler()
                interactive_manager.run(options)
                return
            case "-h" | "--help":
                print_help()
                sys.exit(0)
            case "-l" | "--ui-lang":
                lang = val.strip(" ").lower()
                # Check if the language is supported
                if len(lang) > 0 and MessageDisplay.MESSAGES.get(lang,None) is not None: 
                    options["ui-lang"] = lang
                else:
                    options["ui-lang"] = "en"
            case "-d" | "--directory":
                normalized_path = normalize_path(val)
                if os.path.isdir(normalized_path):
                    options["directory"] = normalized_path
                else:
                    print(MessageDisplay.error("pictures_directory_not_found_interactive"))
            case "-r" | "--recursive":
                options["recursive"] = True
            case "-k" | "--keywords":
                keywords = val.split(",")
                if "" in keywords:
                    keywords.remove("")
                options["keywords"] = keywords
            case "-o", "--output":
                normalized_path = normalize_path(val)
                if os.path.isdir(normalized_path):
                    options["output"] = normalized_path
                else:
                    MessageDisplay.error("output")
                    sys.exit(1)
            case "-L" | "--lang":
                lang = val.lower()
                if lang == 'f':
                    options["lang"] = 'fra'
                elif lang == 'a':
                    options["lang"] = 'ara'
            case "-c" | "--case-sensitive":
                options["case-sensitive"] = True
            case _:
                print("Invalid argument.")
                
def extract_cli_args():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hIcrd:k:l:L:o:", ["directory=", "keyword=", "case-sensitive", "interactive","recursive" ,"lang=", "output=", "ui-lang="])
        if len(opts) == 0:
            print_help()
            sys.exit(0)
        else:
            return opts
    except getopt.GetoptError:
        print("Invalid usage.",file = sys.stderr)
        print_help()
        sys.exit(1)

def get_images_in_dir(folder: str,recursive:bool=False):
    image_files = []
    with os.scandir(folder) as images_folder:
        for entry in images_folder:
            if not os.path.isdir(entry) and not entry.name.startswith("."):
                ft = filetype.guess(entry.path)
                if ft.extension in ("png", "jpg", "jpeg", "gif"):
                    image_files.append(entry.path)
            elif os.path.isdir(entry) and recursive:
                for img in get_images_in_dir(entry.path):
                    image_files.append(img)
                
    return image_files

def get_text_in_image(image_path: str, lang: str):
    img = cv2.imread(image_path)
    text_inside_image = pytesseract.image_to_string(img, lang=lang)
    return text_inside_image

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=26, fill='█', print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r\033[1;32m{prefix} |{bar}| {percent}% {suffix}\033[0m', end=print_end, flush=True)

def print_summary(data:dict):
    print("\n\n\033[1;33m=========================================\033[0m")
    print(f"\033[1;33m{MessageDisplay.label('headline')}\033[0m")
    print("\033[1;33m=========================================\033[0m")
    print(f"\033[1;33m{MessageDisplay.label('total_pictures')}{data.get('total_images')}\033[0m")
    print(f"\033[1;33m{MessageDisplay.label('runtime')}{data['runtime']}\033[0m")
    print()
    
    table = Texttable()
    table.add_rows([[MessageDisplay.label("keyword"), MessageDisplay.label("keyword_found")]])
    found_something = False
    for keyword in data.get("keywords"):
        if data.get(keyword).get("count") > 0:
            found_something = True
        table.add_row([keyword,f"{data.get(keyword).get('count')} {MessageDisplay.label("pictures") if data.get(keyword).get('count') > 1 else MessageDisplay.label("picture")}"])
    
    print(f"\033[1;33m{table.draw()}\033[0m")
    if found_something:
        print(f"\033[1;33m{MessageDisplay.label('see_results')}\033[0m", end="")
        answer = input("\033[1;33m>>\033[0m ").strip(" ").lower()
        while answer not in MessageDisplay.prompt("valid_answers").get("all"):
            print(MessageDisplay.error("yes_no"))
            answer = input("\033[1;33m>>\033[0m ").strip(" ").lower()
        if answer in MessageDisplay.prompt("valid_answers").get("yes"):
            for keyword in data.get("keywords"):
                    if data.get(keyword).get("count") > 0:
                        for image_path in data.get(keyword).get("paths"):
                            print(f"\033[1;33mOpening {image_path}...\033[0m")
            
def print_headline(msg: str):
    print(f"\033[1;32m{len(msg) * '='}\033[0m")
    print(f"\033[1;32m{msg}\033[0m")
    print(f"\033[1;32m{len(msg) * '='}\033[0m")

def print_help():
    print("""
    Search text in multiple images using tesseract (an OCR — Optical Character Recognition — tool powered by Google.

    Usage:
        peekr.py [options]

    Options:
        -h, --help  display this help
        -I, --interactive   Run in interactive mode
        -d, --directory Specify the target directory to be searched
        -c, --case-sensitive  Perform a case-sensitive search
        -L, --lang  Specify the language to be used in search (Default is English)
        -l, --ui-lang Specify the language to use when displaying messages
        -r, --recursive Recursively search subdirectories
        -o, --output    Create a folder in the specified location and copy the pictures found into it  
        -k, --keyword A keyword to search for 
    """)
            
def main():
    init_args(OPTIONS)
    summary = {}
    images = get_images_in_dir(OPTIONS["directory"],OPTIONS["recursive"])
    number_of_images = len(images)
    summary["total_images"] = number_of_images
    summary["start_time"] = timeit.default_timer()
    summary["keywords"] = OPTIONS["keywords"]
    for keyword in OPTIONS["keywords"]:
        summary[keyword] = {}
        summary[keyword]["count"] = 0
        summary[keyword]["paths"] = []
    for index, image_file_path in enumerate(images):
        image_text = get_text_in_image(image_file_path, "eng")
        for keyword in OPTIONS["keywords"]:
            if OPTIONS["case-sensitive"] is True:
                result = keyword in image_text
            else:
                result = keyword.lower() in image_text.lower()
            if result:
                summary[keyword]["paths"] += [image_file_path]
                summary[keyword]["count"] += 1

            print_progress_bar(index + 1, number_of_images, prefix="Progress:", suffix="Complete")

    summary["end_time"] = timeit.default_timer()
    summary["runtime"] = f"{int(summary.get('end_time') - summary.get('start_time'))} seconds"

    print_summary(summary)
    


if __name__ == "__main__":
    main()
