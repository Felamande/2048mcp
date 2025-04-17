from fastmcp import FastMCP
import requests
import json

mcp  = FastMCP("this is a 2048 game mcp server with max of 32768, you can play it")


BASE_API = "http://127.0.0.1:5000"


def move(direction:str)-> str:
    rsp = requests.post(f"{BASE_API}/move/{direction}")
    if rsp.status_code == 200:
        jsonrsp = rsp.json()
        jsonrsp['request_result'] = 'ok'
        return json.dumps(jsonrsp)
    else:
        jsonrsp = rsp.json()
        jsonrsp['request_result'] = f"fail with http {rsp.status_code}"
        return json.dumps(jsonrsp)
    

def try_move(direction:str)-> str:
    rsp = requests.post(f"{BASE_API}/try_move/{direction}")
    if rsp.status_code == 200:
        jsonrsp = rsp.json()
        jsonrsp['request_result'] = 'ok'
        return json.dumps(jsonrsp)
    else:
        jsonrsp = rsp.json()
        jsonrsp['request_result'] = f"fail with http {rsp.status_code}"
        return json.dumps(jsonrsp)

@mcp.tool()
def moveup() -> str:
    """move up a 2048 game's direction and get current status"""
    return move('up')

@mcp.tool()
def movedown() -> str:
    """move down a 2048 game's direction and get current status"""
    return move('down')

@mcp.tool()
def moveleft() -> str:
    """move left a 2048 game's direction and get current status"""
    return move('left')

@mcp.tool()
def moveright() -> str:
    """move right a 2048 game's direction and get current status"""
    return move('right')



# # try move 
# @mcp.tool()
# def try_moveup() -> str:
#     """try to move up a 2048 game's direction and get status after moving but not affect real game"""
#     return try_move('up')

# @mcp.tool()
# def try_movedown() -> str:
#     """try to move down a 2048 game's direction and get status after moving but not affect real game"""
#     return try_move('down')

# @mcp.tool()
# def try_moveleft() -> str:
#     """try to move left a 2048 game's direction and get status after moving but not affect real game"""
#     return try_move('left')

# @mcp.tool()
# def try_moveright() -> str:
#     """try to move right a 2048 game's direction and get status after moving but not affect real game"""
#     return try_move('right')

    
@mcp.tool()
def get_status() -> str:
    """get 2048 game status of all the tiles and current score in json format"""
    rsp = requests.get(f"{BASE_API}/status")
    if rsp.status_code == 200:
        jsonrsp = rsp.json()
        jsonrsp['request_result'] = 'ok'
        return json.dumps(jsonrsp)
    else:
        jsonrsp = rsp.json()
        jsonrsp['request_result'] = f"fail with http {rsp.status_code}"
        return json.dumps(jsonrsp)

# @mcp.tool()
# def reset_game() -> str:
#     """reset 2048 game status"""
#     rsp = requests.post(f"{BASE_API}/reset")
#     if rsp.status_code == 200:
#         jsonrsp = rsp.json()
#         jsonrsp['request_result'] = 'ok'
#         return json.dumps(jsonrsp)
#     else:
#         jsonrsp = rsp.json()
#         jsonrsp['request_result'] = f"fail with http {rsp.status_code}"
#         return json.dumps(jsonrsp)


if __name__ == "__main__":
    mcp.run()