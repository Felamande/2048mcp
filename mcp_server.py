from fastmcp import FastMCP
import requests
import json

mcp  = FastMCP("this is a 2048 game mcp server with max of 32768, you can play it")


BASE_API = "http://127.0.0.1:5000"


def move(direction:str)-> str:
    rsp = requests.post(f"{BASE_API}/move/{direction}")
    if rsp.status_code == 200:
        return json.dumps(rsp.json())
    else:
        jsonrsp = rsp.json()
        jsonrsp['result'] = f"fail with http {rsp.status_code}"
        return json.dumps(jsonrsp)

@mcp.tool()
def moveup() -> str:
    """move up a 2048 game's direction """
    return move('up')

@mcp.tool()
def movedown() -> str:
    """move down a 2048 game's direction"""
    return move('down')

@mcp.tool()
def moveleft() -> str:
    """move left a 2048 game's direction"""
    return move('left')

@mcp.tool()
def moveright() -> str:
    """move right a 2048 game's direction"""
    return move('right')
    
@mcp.tool()
def get_status() -> str:
    """get 2048 game status of all the tiles and current score in json format"""
    rsp = requests.get(f"{BASE_API}/status")
    if rsp.status_code == 200:
        jsonrsp = rsp.json()
        jsonrsp['result'] = f"ok"
        return json.dumps(jsonrsp)
    else:
        jsonrsp = rsp.json()
        jsonrsp['result'] = f"fail with http {rsp.status_code}"
        return json.dumps(jsonrsp)
    
if __name__ == "__main__":
    mcp.run()