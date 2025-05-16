import glob
import os.path
import re
from tqdm import tqdm
import pandas as pd
import spacy

xml_start = re.compile("<doc.id=\d{4}\..+>")
xml_end = re.compile("</doc>")

nlp = spacy.load("en_core_web_md")


def load_and_preprocess(filename):
    # open the file
    with open(filename, encoding="latin-1") as f:
        # read the text, get doc id and clean text
        text = f.read()
        text = xml_start.sub("", text)
        text = xml_end.sub("", text)
        text = text.strip()

    return text


def counts_from_doc(doc):
    noun_count = 0
    verb_count = 0
    adj_count = 0
    adv_count = 0

    for token in doc:
        if token.pos_ == "NOUN":
            noun_count += 1
        elif token.pos_ == "VERB":
            verb_count += 1
        elif token.pos_ == "ADJ":
            adj_count += 1
        elif token.pos_ == "ADV":
            adv_count += 1

    rel_noun_count = noun_count / len(doc)
    rel_verb_count = verb_count / len(doc)
    rel_adj_count = adj_count / len(doc)
    rel_adv_count = adv_count / len(doc)

    unique_per = set()
    unique_loc = set()
    unique_org = set()
    for entity in doc.ents:
        if entity.label_ == "PERSON":
            unique_per.add(entity.text)
        elif entity.label_ == "LOC":
            unique_loc.add(entity.text)
        elif entity.label_ == "ORG":
            unique_org.add(entity.text)

    unique_per_count = len(unique_per)
    unique_loc_count = len(unique_loc)
    unique_org_count = len(unique_org)

    return (rel_noun_count, rel_verb_count, rel_adj_count, rel_adv_count,
            unique_per_count, unique_loc_count, unique_org_count)


def process_folder(folder):
    data_lines = []
    # loop over files in the folder
    folder_name = os.path.basename(folder)
    files = glob.glob(folder + "/*.txt")


    for file in tqdm(files, desc=folder_name):
        text = load_and_preprocess(file)
        filename = os.path.basename(file)
        doc = nlp(text)
        counts = counts_from_doc(doc)
        data_lines.append((filename,) + counts)

    df = pd.DataFrame(
        data_lines,
        columns=["Filename", "RelFreq NOUN", "RelFreq VERB", "RelFreq ADJ", "RelFreq ADV",
                 "Unique PER", "Unique LOC", "Unique ORG"],
    )
    df.to_csv("output/" + folder_name + ".csv", index=False)


if __name__ == "__main__":
    data_folders = glob.glob("data/USEcorpus/*")

    if not os.path.exists("output/"):
        os.makedirs("output/")

    for folder_path in data_folders:
        process_folder(folder_path)
