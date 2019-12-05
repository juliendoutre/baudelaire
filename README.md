# Baudelaire

A text generator trained over Baudelaire's poems.

## Install the package

Simply run:
```shell
pip3 install baudelaire
```

## Usage

```shell
baudelaire train --epochs 100 --batch_size 50
baudelaire generate --lines 10
```

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
scrapy runspider scraping/poems.py -t json -o poems.json
```

to save the poems contents and a few metadata in a `poems.json` file.

## Dataset description

You can find some metadata about the poems and the collections they are categorized in, in `data/stats.json`.
This json was generated with the `scraping/analyzer.py` script.

## Bibliography

- https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3
- https://www.analyticsvidhya.com/blog/2018/03/text-generation-using-python-nlp/
