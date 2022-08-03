# Automate New Book Display Collection for Primo VE/Alma
Small Python script that can be used to automate maintaining a New Book collection in Alma for display to patrons in Primo VE

# You will need:
- A Collection set up where your new books will live (You will need the Collection ID)
- Reports in Alma Analytics for your new materials (in my case, we have Print and Electronic titles for a single Library, fitered to the last 30 days), the report *must* contain the MMSIDs for each title you want to add to the collection
- API keys from the ExLibris Developers Network for Bibs (Read/Write) and Analytics (Read-only)
