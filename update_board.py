import argparse
import json
from datadog import initialize, api

#id = 249100

def check_board_presence(id):
  result = api.Screenboard.get(id)
  if ("errors" in result):
    print("Board not found.")
    return False
  print("Board found.")
  return True

def create_board(board_json):
  result = api.Screenboard.create(**board_json)
  #Print ID of the board
  print(result['id'])

def update_board(board_id, board_json):
  result = api.Screenboard.update(board_id, **board_json)
  #Print ID of the board
  print(result['id'])

def main():

  parser = argparse.ArgumentParser(description='Parse board name and datadog api info')
  parser.add_argument('--id', type=int, required=True)
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
    update_board(args.id, board_json)
  else:
    create_board(board_json)

if __name__ == "__main__" :
  main()