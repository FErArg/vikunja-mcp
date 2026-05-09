import sys
from vikunja_mcp.config import Config
from vikunja_mcp.api import VikunjaClient
from vikunja_mcp.tools import register_tools


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m vikunja_mcp.server <config_path>")
        sys.exit(1)

    config = Config(sys.argv[1])
    client = VikunjaClient(config.api_base_url, config.headers())

    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        print("Error: fastmcp not installed. Run: pip install fastmcp")
        sys.exit(1)

    mcp = FastMCP("vikunja-mcp")
    register_tools(mcp, client)
    mcp.run()


if __name__ == "__main__":
    main()