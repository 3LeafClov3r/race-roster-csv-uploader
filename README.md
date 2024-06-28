To use:
1) create a google sheet (named something like race roster data) with a subsheet named the year number that the event has been going on (7 in my case)
2) look at the url to find the google sheet id. Ex. https://docs.google.com/spreadsheets/d/xxxxxxxxxxxx/edit?.... where the xxxx is the google sheet id
3) For each year in the spreadsheet look at the url and note down the gid value, Ex. edit?gid=xxxxxx#gid=xxxxxx
4) create json file named info.json file in same directory as other two python files. using the previous information format it like:
```json
{
    "sheet_name": "sheet_name_goes_here",
    "sheet_id":  "sheet_id_goes here",
    "name": [
        "numerical values only: ex .1 in increasing value order",
        "2",
        "3"
    ],
    "gid": [
        "xxxxx- make sure that the gids and the names line up",
        "xxxxx",
        "xxxxx"
    ]
}
```
6) enable both the google drive api and the google sheet api in google's developer console and add service_account.json file to the same directory as the other files
