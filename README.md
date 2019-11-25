# RCPublications

This provides metadata about publications for the Rich Context knowledge graph,
which links publications to [datasets](https://github.com/NYU-CI/RCDatasets).

The links and other metadata that are represented here originate from
manually-curated documents provided by our community of researchers,
agencies, and other data providers.

Updates arrive in mulitple drops and the manual curation gets
performed over in that repo prior to commits:
<https://github.com/NYU-CI/RichContextMetadata/tree/master/metadata>


## Instructions for adding new publications

  1. Create a branch
  2. Prepare the data in your CSV file
  3. Generate a JSON file to add as a partition
  4. Run unit tests prior to commit


### 1. Create a branch

Create a new branch with the same name as your `metadata/`
subdirectory.

Example:
`git checkout -b 20190717_usda_wic`


### 2. Prepare the data in your CSV file

Identify the CSV within your `metadata/` subdirectory. There may be
multiple sheets in the original spreadsheet provided by the partner,
so make sure you've selected the one created by someone on our team.

If your CSV lists a publication with a DOI but no URL, construct a URL
in a new column in the CSV before proceeding: `https://www.doi.org/<doi>`

Excel code: `="https://www.doi.org/" & <doi_cell>`


Finally, your CSV file should have the minimum required fields:

  * `title` -- title of the publication
  * `dataset` -- a list of links from <https://github.com/NYU-CI/RCDatasets/datasets.json>
  * `original` -- full metadata extracted from the CSV

Remove any entries that don't have these fields.


### 3. Generate a JSON file to add as a partition

Use the `publications_export_template.ipynb` example to generate a
JSON file to add to the `partitions/` directory.

  * Navigate to your subdirectory in `RichContextMetadata/metadata` where your CSV is stored

  * Copy `publications_export_template.ipynb` from this repo

  * Optional: it's a good pratice to rename the notebook the same as the subdirectory

  * Update the `file_name` and `rcm_subfolder` variables, and no changes should be needed after that

  * You can step through the notebook, which will export your publications metdata to `/partitions`

  * If you run into any problems with the template, post a GitHub issue on this repo

Check the `RCPublications/partitions` subdirectory after you reach the
end of the notebook, to make sure that the JSON files has the required
fields and was exported properly.


### 4. Run unit tests prior to commit

Run the unit tests on your new JSON file partition prior to commit:
```
python test.py partitions/20190717_usda_wic_publications.json
```


## Caveats

  * We handle duplicate titles downstream in the graph management
