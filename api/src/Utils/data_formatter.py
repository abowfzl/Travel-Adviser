from collections import defaultdict
from collections import Counter


def format_entries(retrieved_items):
    """Format the entries to combine redundant data."""

    # Dictionary to store combined entries
    combined_entries = defaultdict(lambda: {
        "n.city_name": "",
        "n.locations": [],
        "n.titles": [],
        "n.texts": [],
        "n.urls": []
    })

    # Process each entry in the provided data
    for entry in retrieved_items:
        name = entry["n.name"]

        # Combine city_name and locations
        if entry.get("n.city_name"):
            combined_entries[name]["n.city_name"] = entry["n.city_name"]
        if entry.get("n.location") and entry["n.location"] not in combined_entries[name]["n.locations"]:
            combined_entries[name]["n.locations"].append(entry["n.location"])

        # Combine titles and texts into lists
        if entry.get("n.title"):
            combined_entries[name]["n.titles"].append(entry["n.title"])
        if entry.get("n.text"):
            combined_entries[name]["n.texts"].append(entry["n.text"])

        # Handle the URLs
        if entry.get("n.url") and entry["n.url"] not in combined_entries[name]["n.urls"]:
            combined_entries[name]["n.urls"].append(entry["n.url"])

    # Resolve multiple locations/URLs if needed
    for name, details in combined_entries.items():
        if len(details["n.locations"]) > 1:
            # Example: Choose the most common location
            most_common_location = Counter(details["n.locations"]).most_common(1)[0][0]
            details["n.location"] = most_common_location
        else:
            details["n.location"] = details["n.locations"][0] if details["n.locations"] else ""
        details.pop("n.locations", None)

        if len(details["n.urls"]) > 1:
            # Example: Keep the first URL or all
            details["n.url"] = details["n.urls"][0]  # or join as string, e.g., ", ".join(details["n.urls"])
        else:
            details["n.url"] = details["n.urls"][0] if details["n.urls"] else ""
        details.pop("n.urls", None)

    final_data = [{"n.name": name, **details} for name, details in combined_entries.items()]

    return final_data
