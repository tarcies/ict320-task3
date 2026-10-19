# ReefWatch Marine Conservation

A Flask proof of concept for one monitoring station. Surveys, equipment and partners are stored in
Azure Cosmos DB (MongoDB API); daily summaries and user accounts in Azure SQL.

## Requirements

- Python 3.12 or newer
- An Azure Cosmos DB (MongoDB API) account and an Azure SQL database (free tier is fine)

## Setup

Run everything from the project root folder.

```bash
pip install -r requirements.txt
```

## Create and fill the databases

Start the setup menu:

```bash
python cli.py
```

Then choose these options in order:

| Option | Input                         | What it does                                                       |
| ------ | ----------------------------- | ------------------------------------------------------------------ |
| 1      | `sql/01_create_tables.sql`    | Creates the `DailySummaries` and `Users` tables                    |
| 1      | `sql/02_sample_summaries.sql` | Adds 5 sample daily summaries                                      |
| 2      | `data/seed_data.json`         | Loads 12 equipment items, 5 partners and 18 surveys into Cosmos DB |
| 7      | username, password, role      | Creates a login (`admin` or `field`)                               |

Create at least one `admin` so you can generate summaries. Options 3 to 6 print stored summaries,
surveys, equipment and partners. Press Ctrl+C to quit.

## Run the web app

```bash
python run.py
```

Open <http://127.0.0.1:5000> and sign in. Admins can generate daily summaries; field staff can
enter surveys and download survey PDFs.

> ### Note:
>
> You can use an existing admin account with username `admin` and password `admin`

The first request after the Azure SQL database has been idle may take up to a minute while it
wakes from auto-pause.

## Tests

```bash
pip install pytest mongomock
pytest -v
```

These run without touching Azure. `pytest -m integration` runs one test against the real databases.
