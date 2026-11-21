# JavaScript Object Notation (JSON)

import json

people_string = '''
{
    "people": [
        {
            "name": "John Smith",
            "phone": "615-555-7164",
            "emails": [
                "johnsmith@bogusemail.com",
                "john.smith@work-place.com"
            ],
            "has_license": false
        },
        {
            "name": "Jane Doe",
            "phone": "560-555-5153",
            "emails": null,
            "has_license": true
        }
    ]
}
'''

# Convert JSON string to Python dictionary
data = json.loads(people_string)

# Print the data
print(data)

# Access each person's name
for person in data["people"]:
    print(type(person["emails"]))