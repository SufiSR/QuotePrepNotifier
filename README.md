# 📨 Quote Summary Notifier for Plunet

This Python script connects to the [Plunet BusinessManager](https://www.plunet.com) SOAP API and retrieves all quotes that are currently in **Preparation** status (status ID `9`) within the last 12 months. It then sends each **project manager** an email summary of their assigned quotes.

## 📦 Features

- Connects to Plunet API using `zeep` (WSDL/SOAP client)
- Retrieves relevant quote metadata including:
  - Quote Number
  - Project Name
  - Creation Date
  - Customer Name
- Groups quotes by Project Manager
- Sends an automatic email to each project manager with their quotes

---

## 🛠️ Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
````

The following Python packages are used:

* `zeep`
* `python-dotenv`
* `smtplib` (standard lib)
* `email` (standard lib)

---

## 🔐 Configuration

Create a `.env` file in the project root and add the following:

```env
PLUNET_BASE_URL=https://your.plunet.instance.com/api30/
PLUNET_API_USER=api_user
PLUNET_API_PASSWORD=secure_password
```

Also make sure your `send_email.py` script includes your SMTP config:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use environment variables for production
```

---

## 🚀 Usage

Run the script with:

```bash
python main.py
```

You can rename the main script file if needed.

Each project manager with pending quotes will receive an email with a list like:

```
- Q-8134-01 | API Test System | 2024-05-16 14:40 | Dialogue
- Q-8135-02 | UX Localization | 2024-07-10 10:30 | Acme Corp
```

---

## ✅ Best Practices

* Use an **App Password** for Gmail or a dedicated SMTP service (e.g. SendGrid)
* Add logging or CSV output for traceability
* Run via a **cron job** or task scheduler for daily/weekly automation
* Wrap with Docker if deploying in CI/CD

---

## 🧠 Known Limitations

* Requires internet access and valid Plunet API credentials
* Only handles quotes in **Preparation** (`status=9`)
* No HTML formatting (plain text emails only)
* No deduplication or history tracking (e.g. only new quotes)

---



---

## 🧑‍💻 Author

Developed by [Sufian Reiter](mailto:sufireiter@googlemail.com)
Feel free to contribute or fork the script for internal use!

```

Let me know if you'd like this published as a GitHub repository template or need badges, changelog formatting, or license instructions.

