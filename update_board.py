import argparse
import json
from datadog import initialize, api

id = 249100

def check_board_presence(id):
  result = api.Timeboard.get(id)
  if ("errors" in result):
    print("Board not found.")
    return False
  print("Board found.")
  return True

def create_board(title, board_json):
  description = "my board"
  result = api.Timeboard.create(title=title, description=description, graphs=board_json, read_only=True)
  #Print ID of the board
  print(result)

def update_board(board_id, title, board_json):
  description = "my board"
  result = api.Timeboard.update(board_id, title=title, description=description, graphs=board_json, read_only=True)
  #Print ID of the board
  print(result)

def main():

  parser = argparse.ArgumentParser(description='Parse board name and datadog api info')
  parser.add_argument('--id', type=int, required=True)
  parser.add_argument('--name', required=True)
  parser.add_argument('--apikey', required=True)
  parser.add_argument('--appkey', required=True)
  parser.add_argument('--json', required=True)
  args = parser.parse_args()

  options = {
    'api_key': args.apikey,
    'app_key': args.appkey
  }

  initialize(**options)

  #Check if board exists
  board_exists = check_board_presence(args.id)
  
  #Get JSON
  board_json = json.load(open(args.json))

  #Create or Update depending on the reuslt of the last check
  if (board_exists):
    update_board(args.id, args.name, board_json)
  else:
    create_board(args.name, board_json)

if __name__ == "__main__" :
  main()