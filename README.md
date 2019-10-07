# RCPublications

This repo provides `publications.json`, metadata on publications - for our publications model in our Rich Context Knowledge Graph. Metadata links publications to datasets from [`datasets.json`](https://github.com/NYU-CI/RCDatasets)

The dataset linkage (represented by `related_dataset` field - see more below) originates from manually-curated relationships documented in multiple [drops](https://github.com/NYU-CI/RichContextMetadata/tree/master/metadata) provided by a community of researchers.

# Instructions for Adding new publications
1. Prepping your csv
1. Publishing publications linkages as a partition
2. Run unit test (`test.py`)

## 1. Prepping your CSV
Your CSV file should, at a minimum, have a field for publication title and datasets (the datasets that the publicaton uses). Ideally, your csv will also have a url and a doi for the publication.

If there is a doi but no url, construct a url in a new column in the csv before converting to json as follows:
`https://www.doi.org/<doi>`

## 2. Publishing publications linkages as a partition
Convert publication linkages to a `publications.json` partition publications, working from `publications_export_template.ipynb`
* Create branch - name it like the subdirectory of `RichContextMetadata/metadata` that you were working within.
* Make a copy of `publications_export_template.ipynb` into the subdirectory  of `RichContextMetadata/metadata` that you were working within - renaming the notebook may be helpful for you.
* Step through the notebook, adjusting variable names as needed, to export your publications metdata to `/partitions`.
* Once exported, checked the json file to make sure it has the required fields.

### Required Fields
At a minimum, each record in the `publications.json` file must have
  * `title` -- name of the publication
  * `datasets` -- list of one or more `id` from [`datasets.json`](https://github.com/NYU-CI/RCDatasets/datasets.json)
If any of these fields don't exist, filter out once you read in the csv before exporting to json.

### Additional fields
* `url`  -- link to publication, preferably open-access if exists. 
* `doi` -- 
* `date` -- publication date
* `alt_ids` -- stored as a list, other unique identifiers (alternative DOIs, ids from publishers, etc.). alt_ids should be written as a `URN` e.g, if you have a pmid 28818487 from Pubmed, the entry would be  `alt_ids`: [`'pubmed:28818487'`]
* `keywords` - keywords or categories (e.g. mesh terms)
* `journal`
* `open access`
* `authors` - authors, including affiliations if available


## 3. Run unit test
Run `python test.py` - a unit test on the last edited file within `partitions/`. If there are any errors,  make changes in the csv and rerun your notebook to re-export the .json file.

### To do - dealing with orignal metadata and API metadata
original_metadata - stick authors and any other entries