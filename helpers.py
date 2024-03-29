import re
import requests
import os
from dotenv import load_dotenv

# regex for valid address pattern
pattern = re.compile(r"""^(?=.*\d)[a-zA-Z0-9, "']+$""")

load_dotenv()
# for address validation api
google_api = os.getenv("GOOGLE_API")


def main():
    # sample data passed to the functions
    try:
        result_data = check_data(
            form_data={
                "address": "ABC Poppins Pl, Toronto, On A1A 1A1 Can",
                "rent": None,
                "years": None,
                "clean": "Dirty",
                "maintain": "Needs Improvement",
                "amenities": "Lacking",
                "neighbourhood": "Unfavorable",
                "review": "",
            }
        )
        # printing the return value
        print(result_data)
        if result_data:
            final_data = prepare_data(
                form_data={
                    "address": "ABC Poppins Pl, Toronto, On A1A 1A1 Can",
                    "rent": None,
                    "years": None,
                    "clean": "Dirty",
                    "maintain": "Needs Improvement",
                    "amenities": "Lacking",
                    "neighbourhood": "Unfavorable",
                    "review": "",
                }
            )
        # printing the return value
        print(final_data)
    except Exception as e:
        print(e)
        return False


# checking the data
def check_data(form_data):
    try:
        for key, value in (form_data).items():
            if key == "address":
                if len((form_data["address"]).strip()) <= 10:
                    return False
                elif not pattern.match(form_data[key]):
                    return False
            elif key in ("rent", "years"):
                if not form_data[key]:
                    continue
                elif float(form_data[key]) < 0:
                    return False
            elif key == "clean":
                if (form_data[key]).strip().title() not in (
                    "Dirty",
                    "Average",
                    "Clean",
                ):
                    return False
            elif key == "maintain":
                if (form_data[key]).strip().title() not in (
                    "Needs Improvement",
                    "Adequate",
                    "Well Maintained",
                ):
                    return False
            elif key == "amenities":
                if (form_data[key]).strip().title() not in ("Lacking", "Basic", "Good"):
                    return False
            elif key == "neighbourhood":
                if (form_data[key]).strip().title() not in (
                    "Unfavorable",
                    "Okay",
                    "Safe",
                ):
                    return False
            elif key == "review":
                if len(form_data["review"]) > 150:
                    return False

        return True
    except Exception as e:
        return False


def prepare_data(form_data):
    for key, value in (form_data).items():
        if key in ["rent", "years"]:
            if not form_data[key]:
                form_data[key] = ""
            else:
                form_data[key] = str(form_data[key])
    # formatting the data in a form of dictionary
    form_data = {
        "address": form_data["address"].strip().title(),
        "rent": form_data["rent"],
        "years": form_data["years"],
        "clean": form_data["clean"].strip().title(),
        "maintain": form_data["maintain"].strip().title(),
        "amenities": form_data["amenities"].strip().title(),
        "neighbourhood": form_data["neighbourhood"].strip().title(),
        "review": form_data["review"].strip().capitalize(),
    }
    return form_data


def format_address(address):
    url = (
        f"https://addressvalidation.googleapis.com/v1:validateAddress?key={google_api}"
    )

    data = {"address": {"regionCode": "CA", "addressLines": [address]}}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        formatted_address = result["result"]["address"]["formattedAddress"]
        print(1)
        print(f"formatted address is {formatted_address}")
        return formatted_address
    else:
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    main()
