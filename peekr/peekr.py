#!/usr/bin/env python


    
import getopt
import locale
import os
import sys
import timeit
import filetype

class MessageDisplay:
    MESSAGES = {
        "en":{
            "prompts":{
                "pictures_directory":"Path to the pictures directory : ",
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
                "lang":"Invalid Answer. The chosen language is not supported.",
                "output":"Directory already exists.",
                "yes_no":"Type [Y] for Yes or [N] for No.",
            },
            "summary_text":{
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
                "lang":"Réponse invalide. La langue choisi n'est pas supporté.",
                "output":"Dossier existe déja.",
                "yes_no":"Taper [O] pour Oui, [N] pour Non.",
            },
            "summary_text":{
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
        return MessageDisplay.MESSAGES[OPTIONS["ui-lang"]]['prompt'][key]
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

def init_args(options:dict[str,str]):
    
    args = extract_cli_args()
    
    for opt, val in args:
        match opt:
            case "-l" | "--ui-lang":
                lang = val.strip(" ").lower()
                # Check if the language is supported
                if len(lang) > 0 and MessageDisplay.MESSAGES.get(lang,None) is not None: 
                    options["ui-lang"] = lang
                else:
                    options["ui-lang"] = "en"
            case "-d" | "--directory":
                if os.path.isdir(val):
                    options["directory"] = val
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
                if os.path.isdir(val):
                    options["output"] = val
                else:
                    MessageDisplay.error("output")
                    sys.exit(1)
            case "-L" | "--lang":
                lang = val.lower()
                if lang == 'f':
                    options["lang"] = 'fra'
                elif lang == 'a':
                    options["lang"] = 'ara'
            case "-I" | "--interactive":
                pass
            case "-c" | "--case-sensitive":
                options["case-sensitive"] = True
            case "-h" | "--help":
                print_help()
                sys.exit(0)
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
    


if __name__ == "__main__":
    main()
