# Baudelaire

## Set the environment

Create a virtualenv:
```shell
python3 -m venv venv
```

Activate it:
```shell
. venv/bin/activate
```

And install the required packages:
```shell
pip3 install -r requirements.txt
```

## Get the dataset

I fetched Baudelaire's poems from this [website](https://www.poesie-francaise.fr/poemes-charles-baudelaire/) using [scrapy](https://scrapy.org/).

Run
```shell
scrapy runspider scraping/poems.py -t json -o data/poems.json
```

to save the poems contents and a few metadata in the `data/poems.json`.

## Dataset description

You can find some metadata about the poems and the collections they are categorized in, in `data/stats.json`.
This json was generated with the `scraping/analyzer.py` script.

## Tutorials

- https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
- https://www.analyticsvidhya.com/blog/2018/03/text-generation-using-python-nlp/

## TODO

- refactor the code to use classes
- add a CLI to allow control over the following operations:
    - get data
    - train the model (parameters choice) and save the weights
    - load the weights and generate some text
- create a Messenger bot that generates Baudelaire poems on demand
