from zeep import Client
from dotenv import load_dotenv
import os
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any
from send_email import send_email

# Load environment variables
load_dotenv()
BASE_URL = os.getenv("PLUNET_BASE_URL")
USER = os.getenv("PLUNET_API_USER")
PASSWORD = os.getenv("PLUNET_API_PASSWORD")

# WSDL endpoint setup
endpoints = {
    "PlunetAPI": Client(BASE_URL + "PlunetAPI?wsdl").service,
    "Customer": Client(BASE_URL + "DataCustomer30?wsdl").service,
    "Resource": Client(BASE_URL + "DataResource30?wsdl").service,
    "Quote": Client(BASE_URL + "DataQuote30?wsdl").service,
}


def login() -> str:
    """Logs into Plunet and returns the session UUID."""
    try:
        return endpoints["PlunetAPI"].login(USER, PASSWORD)
    except Exception as e:
        raise RuntimeError(f"Login failed: {e}")


def get_all_quotes(uuid: str) -> List[int]:
    """Retrieves all quote IDs from the past year with status 'Preparation' (status 9)."""
    try:
        start_date = datetime.today().replace(year=datetime.today().year - 1)
        time_frame = {
            "dateFrom": start_date.strftime('%Y-%m-%d'),
            "dateRelation": 1,
            "dateTo": datetime.today().strftime('%Y-%m-%d')
        }
        search_filter = {
            "languageCode": "EN",
            "quoteStatus": 9,
            "timeFrame": time_frame
        }
        result = endpoints["Quote"].search(uuid, search_filter)
        return result.data if result.returnCode == 0 else []
    except Exception as e:
        print(f"Failed to retrieve quotes: {e}")
        return []


def get_quote_details(quote_id: int, uuid: str) -> Dict[str, Any]:
    """Fetches all relevant metadata for a given quote ID."""
    try:
        quote = endpoints["Quote"].getQuoteObject(uuid, quote_id).data
        creation_date = endpoints["Quote"].getCreationDate(uuid, quote_id).data
        category = endpoints["Quote"].getProjectCategory(uuid, "EN", quote_id).data
        customer_id = endpoints["Quote"].getCustomerID(uuid, quote_id).data
        customer_name = endpoints["Customer"].getFullName(uuid, customer_id).data
        project_manager_id = endpoints["Quote"].getProjectmanagerID(uuid, quote_id).data
        project_manager_email = endpoints["Resource"].getEmail(uuid, project_manager_id).data
        currency = endpoints["Quote"].getCurrency(uuid, quote_id).data

        return {
            "Retrieval Date": datetime.today().strftime('%Y-%m-%d'),
            "Quote ID": int(quote["quoteID"]),
            "Quote Number": str(quote["quoteNumber"]),
            "Project Name": str(quote["projectName"]),
            "Project Subject": str(quote["subject"]),
            "Status": quote["status"],
            "Creation Date": creation_date,
            "Category": category,
            "Customer": customer_id,
            "Customer Name": customer_name,
            "Project Manager": project_manager_id,
            "Project Manager email": project_manager_email,
            "Currency": currency
        }
    except Exception as e:
        print(f"Failed to retrieve details for quote ID {quote_id}: {e}")
        return {}


def group_quotes_by_manager(quotes: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Groups quotes by the project manager's email address."""
    grouped = defaultdict(list)
    for quote in quotes:
        email = quote.get("Project Manager email")
        if email:
            grouped[email].append(quote)
        else:
            print(f"Warning: Quote {quote.get('Quote Number')} has no project manager email.")
    return grouped


def format_email_body(quotes: List[Dict[str, Any]]) -> str:
    """Generates a readable email body listing all quotes."""
    lines = []
    for q in quotes:
        quote_number = q.get("Quote Number", "N/A")
        project_name = q.get("Project Name", "N/A")
        creation = q.get("Creation Date")
        creation_str = creation.strftime("%Y-%m-%d %H:%M") if isinstance(creation, datetime) else str(creation)
        customer_name = q.get("Customer Name", "N/A")
        lines.append(f"- {quote_number} | {project_name} | {creation_str} | {customer_name}")

    return (
        f"Hello,\n\nHere is the list of your quotes as of today ({datetime.now().strftime('%Y-%m-%d')}):\n\n"
        + "\n".join(lines)
        + "\n\nBest regards,\nYour Friendly Quote Bot"
    )


def send_summary_email(recipient_email: str, quotes: List[Dict[str, Any]]):
    """Sends an email to a single recipient with their assigned quotes."""
    subject = f"[Quote Summary] {len(quotes)} quotes are still in Preparation for you"
    body = format_email_body(quotes)
    try:
        send_email(recipient_email=recipient_email, body=body, subject=subject)
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")


def main():
    """Main execution flow."""
    uuid = login()
    quote_ids = get_all_quotes(uuid)

    list_of_quotes: List[Dict[str, Any]] = []
    for quote_id in quote_ids:
        quote = get_quote_details(quote_id, uuid)
        if quote:
            list_of_quotes.append(quote)

    grouped_quotes = group_quotes_by_manager(list_of_quotes)

    for email, quotes in grouped_quotes.items():
        send_summary_email(email, quotes)


if __name__ == "__main__":
    main()
