import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re


# AUTHENTICATION
def authenticate(credentials):
    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials, scopes=scopes)
    client = gspread.authorize(credentials)
    return client


# # USE THE AUTHENTICATION
# client = authenticate("creds.json")
# # OPEN SHEET AND DO SOME MODIFICATIONS
# sheet_url = "https://docs.google.com/spreadsheets/d/1UGhTjkslKEjoYA0mDe5l8GtS80hS39IsTe0YTE5s0a8/edit#gid=0"
# workbook = client.open_by_url(sheet_url)
# selected_tab = workbook.worksheet("Sheet1")
