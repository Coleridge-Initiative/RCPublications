# RCPublications

This repo provides `publications.json`, metadata on publications - for our publications model in our Rich Context Knowledge Graph. Metadata links publications to datasets from [`datasets.json`](https://github.com/NYU-CI/RCDatasets)

The dataset linkage (represented by `dataset` field - see more below) originates from manually-curated relationships documented in multiple [drops](https://github.com/NYU-CI/RichContextMetadata/tree/master/metadata) provided by a community of researchers. Most work will be done in the [RichContextMetadata](https://github.com/NYU-CI/RichContextMetadata) repository.

# Instructions for Adding new publications
1. Create a branch - and give it the same name as the metadata folder
2. Prepping your csv
3. Publishing publications linkages as a partition
4. Run unit test (`test.py`)

## 1. Create a Branch
Example:
`git checkout -b 20190717_usda_wic`

## 2. Prepping your CSV
Identify the CSV within your `metadata/` subfolder. There may be multiple sheets in there (e.g. the original linkage file sent to us by a collaborator/partner), so make sure you've selected the one created by someone on our team.

Your CSV file should, at a minimum, have a field for publication title and datasets (the datasets that the publicaton uses). 

### Required Fields
At a minimum, each record in the the csv must have (and be spelled like the below)
  * `title` -- name of the publication
  * `dataset` -- list of one or more `id` from [`datasets.json`](https://github.com/NYU-CI/RCDatasets/datasets.json)

Filter out/delete any entries that don't have these fields before proceeding. 

If your csv has a doi but no url, construct a url in a new column in the csv before proceeding, as follows:
`https://www.doi.org/<doi>`

Excel code: `="https://www.doi.org/" & <doi_cell>`

## 3. Publishing publications linkages as a partition
Convert publication linkages to a `publications.json` partition publications, working from `publications_export_template.ipynb`
* Navigate to your subdirectory in `RichContextMetadata/metadata` where your csv of linkages is stored. 
* Make a copy of `publications_export_template.ipynb` from  this repo into the subdirectory. It's not required, but good pratice to rename the notebook with the same name as the subdirectory.
* Update the `file_name` and `rcm_subfolder` variables. No changes should be needed after that. You can step through the notebook, which will export your publications metdata to `/partitions`. If you run into problems with the template, post an issue on github. 
* Once you get to the end of the notebook, check the `RCPublications/partitions` subfolder to ensure that the json has the required fields and was exported properly. The top level of the `.json` file should have only `title` and `datasets`, and may have data nested in `original`.

## 4. Run unit test
Run unit test on your new json file:
`python test.py partitions/20190717_usda_wic_publications.json`


### To do - dealing with orignal metadata and API metadata
original_metadata - stick authors and any other entries
deal with duplicate titles downstream