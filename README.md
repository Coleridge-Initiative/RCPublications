# RCPublications

This provides metadata about publications for the Rich Context knowledge graph,
which links publications to [datasets](https://github.com/NYU-CI/RCDatasets).

The links and other metadata that are represented here originate from
manually-curated documents provided by our community of researchers,
agencies, and other data providers.

Updates arrive in mulitple drops and the manual curation gets
performed over in that repo prior to commits:
<https://github.com/NYU-CI/RichContextMetadata/tree/master/metadata>

Also, before working in this repo you must set up your *pre-commit*
hooks for Git:

```
chmod +x .githooks/pre-commit
bash .githooks/one-time-hook-setup.sh
```


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

Use the `scripts/publications_export_template.py` script to generate a
JSON file to add to the `partitions/` directory.

  * Navigate to your subdirectory in `RichContextMetadata/metadata` where your CSV is stored

  * Copy the **directory name** where your CSV is located, and Copy the **file name** of the CSV you want to export
    * Note: The directory name will become part of the new JSON file 

  * Execute `python scripts/publications_export_template.py <directory_name> <csv_file_name>` on the terminal, or on your favorite IDE.
    * This script will export your publications metadata to `/partitions`

  * If you run into any problems with the template, post a GitHub issue on this repo

Check the `RCPublications/partitions` subdirectory after the script is
done running without errors, to make sure that the JSON files has the
required fields and was exported properly.


### 4. Rebase if needed

Since our team is generally working on different partitions in parallel,
often you'll need to `rebase` prior to creating a pull request.
In other words,

```
git rebase master
git push -f origin
```

Sometimes there may be merge conflicts, which you'll need to fix
manually before you can continue.
See this 
[Git rebase tutorial](https://akrabat.com/the-beginners-guide-to-rebasing-your-pr/)
for more details.


### 5. Run unit tests prior to commit

Run the unit tests on your new JSON file partition prior to commit:
```
python test.py partitions/20190717_usda_wic_publications.json
```


## Caveats

  * We handle duplicate titles downstream in the graph management
