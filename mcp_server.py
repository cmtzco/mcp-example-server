#!/usr/bin/env python3
"""Example MCP Server implementation demonstrating basic MCP functionality."""

import asyncio
import json
import sys
from typing import Any, Dict, List

# MCP server implementation
class MCPServer:
    """Basic MCP Server for demonstration purposes."""
    
    def __init__(self):
        self.name = "example-mcp-server"
        self.version = "1.0.0"
        self.tools = []
        self.resources = []
        
    def get_server_info(self) -> Dict[str, Any]:
        """Return server information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": "A Model Context Protocol server example",
            "protocol_version": "0.1.0"
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools."""
        return [
            {
                "name": "echo",
                "description": "Echo back the input text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to echo back"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "hello",
                "description": "Say hello with an optional name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name to greet (optional)"
                        }
                    }
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call."""
        if name == "echo":
            text = arguments.get("text", "")
            return {
                "content": [{
                    "type": "text",
                    "text": f"Echo: {text}"
                }]
            }
        elif name == "hello":
            name_param = arguments.get("name", "World")
            return {
                "content": [{
                    "type": "text",
                    "text": f"Hello, {name_param}!"
                }]
            }
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources."""
        return [
            {
                "uri": "example://info",
                "name": "Server Information",
                "description": "Basic server information and capabilities",
                "mimeType": "text/plain"
            }
        ]
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource."""
        if uri == "example://info":
            info = self.get_server_info()
            content = f"MCP Server: {info['name']} v{info['version']}\n"
            content += f"Description: {info['description']}\n"
            content += f"Protocol Version: {info['protocol_version']}"
            
            return {
                "contents": [{
                    "uri": uri,
                    "mimeType": "text/plain",
                    "text": content
                }]
            }
        else:
            raise ValueError(f"Unknown resource: {uri}")


def main():
    """Main entry point for the MCP server."""
    server = MCPServer()
    
    print(json.dumps({
        "status": "initialized",
        "server": server.get_server_info(),
        "tools": len(server.list_tools()),
        "resources": len(server.list_resources())
    }, indent=2))
    
    print("\nMCP Example Server is ready to accept connections.")
    print("This is a basic implementation for demonstration purposes.")
    print("\nAvailable tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\nAvailable resources:")
    for resource in server.list_resources():
        print(f"  - {resource['uri']}: {resource['description']}")


if __name__ == "__main__":
    main()
