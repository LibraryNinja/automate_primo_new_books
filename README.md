# Automate New Book Display Collection for Primo VE/Alma
Small Python script that can be used to automate maintaining a New Book collection in Alma for display to patrons in Primo VE

(I'm still a novice programmer so I'm sure there's better ways to do some of these processes...but it works??)

I set this up to run with the Task Scheduler in Windows to run once a week

# You will need:
- A Collection set up where your new books will live (You will need the Collection ID)
- Reports in Alma Analytics for your new materials (in my case, we have Print and Electronic titles for a single Library, fitered to the last 30 days), the report *must* contain the MMSIDs for each title you want to add to the collection. The report must also be in a Shared folder at the Institution level.
- API keys from the ExLibris Developers Network for Bibs (Read/Write) and Analytics (Read-only)


