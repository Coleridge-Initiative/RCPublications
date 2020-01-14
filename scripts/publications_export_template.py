import sys
import os, errno
import csv
import datetime
import json
import pandas as pd
import re
import unicodedata
from pathlib import Path

# TODO maybe move this function to a Utils class? So it can managed from one location 
def scrub_unicode (text):
    """
    try to handle the unicode edge cases encountered in source text,
    as best as possible
    """
    x = " ".join(map(lambda s: s.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace('‚Äô', "'").replace('‚Äì',"--")
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace("`` ", '"').replace("''", '"')
    x = x.replace('…', '...').replace("\\u2026", "...")
    x = x.replace("\\u00ae", "").replace("\\u2122", "")
    x = x.replace("\\u00a0", " ").replace("\\u2022", "*").replace("\\u00b7", "*")
    x = x.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u201a", "'")
    x = x.replace("\\u201c", '"').replace("\\u201d", '"')

    x = x.replace("\\u20ac", "€")
    x = x.replace("\\u2212", " - ") # minus sign

    x = x.replace("\\u00e9", "é")
    x = x.replace("\\u017c", "ż").replace("\\u015b", "ś").replace("\\u0142", "ł")    
    x = x.replace("\\u0105", "ą").replace("\\u0119", "ę").replace("\\u017a", "ź").replace("\\u00f3", "ó")

    x = x.replace("\\u2014", " - ").replace('–', '-').replace('—', ' - ')
    x = x.replace("\\u2013", " - ").replace("\\u00ad", " - ")

    x = str(unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))

    # some content returns text in bytes rather than as a str ?
    try:
        assert type(x).__name__ == "str"
    except AssertionError:
        print("not a string?", type(x), x)

    return x

def check_linkages(linkages_csv): 
    obj_pattern = re.compile('\{.*?\}')
    if 'journal' in linkages_csv.columns.values:
        if linkages_csv['journal'].str.contains(obj_pattern).any():
            raise ValueError("Column '{}' contains invalid value/pattern: {}".format('journal', obj_pattern.pattern))


def create_pub_dict(linkages_dataframe, datasets):
    pub_metadata_fields = ['title']
    original_metadata_cols = list(set(linkages_dataframe.columns.values.tolist()) - set(pub_metadata_fields) - set(['dataset']))
    
    pub_dict_list = []
    for i, r in linkages_dataframe.iterrows():
        r['title'] = scrub_unicode(r['title'])
        ds_id_list = [f for f in [d.strip() for d in r['dataset'].split(",")] if f not in [""," "]]
        for ds in ds_id_list:
            check_ds = [b for b in datasets if b['id'] == ds]
            if len(check_ds) == 0:
                print('dataset {} isnt listed in datasets.json. Please add to file'.format(ds))
        required_metadata = r[pub_metadata_fields].to_dict()
        required_metadata.update({'datasets':ds_id_list})
        pub_dict = required_metadata
        if len(original_metadata_cols) > 0:
            original_metadata_raw = r[original_metadata_cols].to_dict()
            original_metadata_raw.update({'date_added':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            original_metadata = {k: v for k, v in original_metadata_raw.items() if not pd.isnull(v)}
            pub_dict.update({'original': original_metadata})
        pub_dict_list.append(pub_dict)
    return pub_dict_list

def export(rcm_subfolder, file_name,partition_name = None): 

    ## TODO: these paths should be refactored out into a config file
    curr_dir = Path(__file__).parent
    parent_folder = curr_dir / '..' / '..' / 'RichContextMetadata' / 'metadata'
    datasets_file_path = curr_dir / '..' / '..' / 'RCDatasets' / 'datasets.json'
    partitions_path = curr_dir / '..' / '..' / 'RCPublications' / 'partitions'

    linkages_path = parent_folder / rcm_subfolder / file_name
    if not linkages_path.is_file():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), linkages_path)
    else:
        print("Exporting File: ", linkages_path)

    linkages_csv = pd.read_csv(linkages_path, encoding='utf-8')
    print("Linkages Entries Found: {}".format(len(linkages_csv)))

    # Cleaning the Dataframe
    linkages_csv = linkages_csv.loc[pd.notnull(linkages_csv.dataset)].drop_duplicates()
    linkages_csv = linkages_csv.loc[pd.notnull(linkages_csv.title)].drop_duplicates()
    linkages_csv['title'] = linkages_csv['title'].apply(scrub_unicode)
    
    # Check for invalid values
    check_linkages(linkages_csv)

    # Get Datasets Information
    with open(datasets_file_path, encoding="utf-8") as json_file:
        datasets = json.load(json_file)

    linkage_list = create_pub_dict(linkages_csv, datasets)

    if partition_name:
        if not partition_name.endswith('.json'):
            raise ValueError("Your file name for the partition must end with '.json'")
        elif partition_name.endswith('.json'):
            json_pub_path = partitions_path / (partition_name)
        
            print("Publication File: ", json_pub_path)

            with open(json_pub_path, 'w', encoding="utf-8") as outfile:
                json.dump(linkage_list, outfile, indent=2, ensure_ascii=False)
    
    elif not partition_name:
        json_pub_path = partitions_path / (rcm_subfolder + '_publications.json')
        print("Publication File: ", json_pub_path)

        with open(json_pub_path, 'w', encoding="utf-8") as outfile:
            json.dump(linkage_list, outfile, indent=2, ensure_ascii=False)
    
    print("Done publishing.")

if __name__ == "__main__":
    """
    This script transforms CSVs in RichContextMetadata into JSON that 
    is then published to RCPublications
    :1st param: CSV directory name  
    :2nd param: CSV file name
    :return: None
    Example python publications_export_template.py csv_file_path csv_file_name
    """
 
    if len(sys.argv) == 3:
        rcm_subfolder = sys.argv[1]
        file_name = sys.argv[2]
        export(rcm_subfolder, file_name)
    if len(sys.argv) == 4:
        rcm_subfolder = sys.argv[1]
        file_name = sys.argv[2]
        partition_name = sys.argv[3]
        export(rcm_subfolder, file_name, partition_name)
    else:
        raise ValueError("Wrong number of arguments passed in.")
