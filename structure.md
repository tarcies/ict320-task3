```
main/
├── README.md                  # setup + run instructions
├── requirements.txt
├── .env                       # connection strings
├── .gitignore
├── run.py                     # local entry point: python run.py
├── cli.py                     # CLI: sql/mongo load, summary, fetch, user
│
├── app/                       # main application package
│   ├── __init__.py            # create_app() factory, registers blueprints
│   ├── config.py              # loads env vars (Mongo/SQL conn, key)
│   │
│   ├── db/                    # connection layer only, no business logic
│   │   ├── __init__.py
│   │   ├── check.py           # Basic MongoDB/SQL database connection check
│   │   ├── load.py            # loads .json/.sql files to MongoDB/SQL
│   │   ├── mongo.py           # get_db(), collection accessors, index setup
│   │   └── sql.py             # get_connection() context manager
│   │
│   ├── models/                # validation + document builders
│   │   ├── __init__.py        # validate surveys, equipment, and partners
│   │   ├── survey.py
│   │   ├── equipment.py
│   │   └── partner.py
│   │
│   ├── services/              # all business logic lives here
│   │   ├── __init__.py
│   │   ├── survey_service.py      # create survey (decrement stock, insert, rollback)
│   │   ├── equipment_service.py   # CRUD, safe decrement, low-stock query
│   │   ├── partner_service.py     # CRUD
│   │   ├── summary_service.py     # aggregation pipelines + write to Azure SQL
│   │   ├── report_service.py      # PDF generation (reportlab)
│   │   └── auth_service.py        # users, password hashing, role checks
│   │
│   ├── routes/                # thin Flask blueprints that call services
│   │   ├── __init__.py
│   │   ├── main.py            # dashboard / home
│   │   ├── surveys.py         # list, new survey form, survey PDF
│   │   ├── equipment.py
│   │   ├── partners.py
│   │   ├── summaries.py       # view, generate, summary PDF
│   │   └── auth.py            # login / logout
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py      # @login_required, @role_required("admin")
│   │   ├── ids.py             # ID generators + prefix
│   │   ├── datetime.py        # date formatting/validation
│   │   └── errors.py          # custom exceptions (InsufficientStock, DuplicateSummary)
│   │
│   ├── templates/
│   │   ├── base.html          # layout, nav, flash messages
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── surveys/{list,new}.html
│   │   ├── equipment/list.html
│   │   ├── partners/list.html
│   │   └── summaries/{list,detail}.html
│   │
│   └── static/
│       ├── css/style.css
│       └── js/survey_form.js  # event listener for new survey form
│
├── sql/                       # required "SQL scripts for schema creation"
│   ├── 01_create_tables.sql   # DailySummary + Users
│   └── 02_sample_summaries.sql
│   └── 03_sample_users.sql
│
└── data/
    └── seed_data.json         # 10+ equipment, 3+ partners, researchers, surveys
```
