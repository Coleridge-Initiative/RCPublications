# RCPublications

This repo provides `publications.json`, metadata on publications - for our publications model in our Rich Context Knowledge Graph. Metadata links publications to datasets from [`datasets.json`](https://github.com/NYU-CI/RCDatasets)

The dataset linkage (represented by `related_dataset` field - see more below) originates from manually-curated relationships documented in multiple [drops](https://github.com/NYU-CI/RichContextMetadata/tree/master/metadata) provided by a community of researchers.

# Instructions for Adding new publications
1. Add publications, working from `publications_export_template.ipynb`
2. Run unit test (`test.py`)

## 1. Adding publications 
* Create branch - name it like the subdirectory of `RichContextMetadata/metadata` that you were working within.
* Make a copy of `publications_export_template.ipynb` into the subdirectory `/publishing_partitions` and rename the notebook.
* Step through the notebook, adjusting variable names as needed, to export your publications metdata to `/partitions`.
* Once exported, checked the json file to make sure it has all fields.

### Required Fields
At a minimum, each record in the `publications.json` file must have
  * `title` -- name of the publication
  * `related_dataset` -- list of one or more `id` from [`datasets.json`](https://github.com/NYU-CI/RCDatasets/datasets.json)
  * `url` OR 'doi' -- link to publication, preferably open-access if exists. Must have a `doi` if no `url`

### Additional fields
* `date` - publication date
* `alt_ids` -- stored as a list, other unique identifiers (alternative DOIs, ids from publishers, etc.). alt_ids should be written as a `URN` e.g, if you have a pmid 28818487 from Pubmed, the entry would be  `alt_ids`: [`'pubmed:28818487'`]
* `keywords` - keywords or categories (e.g. mesh terms)
* `journal`
* `publisher`
* `open access`
* `authors` - authors, including affiliations if available
* `funder`
* `# of citations`


## 2. Run unit test
Run `python test.py` - a unit test on the last edited file within `partitions/`. If there are any errors,  make changes in the csv and rerun your notebook to re-export the .json file.