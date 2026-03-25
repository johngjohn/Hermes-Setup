mcp_servers:
  obsidian:
    url: "http://127.0.0.1:${VPS_REMOTE_PORT}/mcp"
    headers:
      Authorization: "Bearer $${OBSIDIAN_API_KEY}"
    timeout: 30
    connect_timeout: 10
    tools:
      prompts: false
      resources: false
