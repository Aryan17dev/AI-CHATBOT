from dotenv import load_dotenv
import os


load_dotenv()


AGREEMENT_CONFIGS = {
    "partnership": {
        "template_id": "16AtEgmRL0cAbNAZMP6BKXvGXEj9XVmSxOB1xJbJLpbM",
        "sheet_id": "1VSk14AgajE7swdoFcvdIYPHxRfl0cjpqHYWTnEo9ZnI"
    },
    "ip": {
        "template_id": "1K2IB45ONrzJq4z0yB79RLEe7ijp34a8m9plkLj-eTHM",
        "sheet_id": "1J7VQTRXYzOZJzXC67qmCsfwYgJiZhw5NWUfZXXGAOQ4"
    },
    "nda" : {
        "template_id": "16HfS7Ju-V8uAwWERIf57dmMbV35STk4PON-pNlMoe-w",
        "sheet_id": "1sS5eN9ILQ1GuGkYXcYlgzN6hdbYb8jf6uUnZu84SOpI"
    }

}

SENDER_EMAIL = os.getenv("GMAIL_SENDER")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
