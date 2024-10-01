from fastapi import APIRouter, Query
from .. import schemas
import redis.asyncio as redis
from config.settings import REDIS 
import json

router = APIRouter()
redis_client = redis.from_url(REDIS, encoding="utf-8", decode_responses=True)

@router.get("/scoreboard/", response_model=schemas.ScoreboardResponse)
async def get_scoreboard(top_n: int = Query(default=20, ge=1)):
    # Get top N tools from Redis sorted set
    top_tools = await redis_client.zrevrange('duffbot_tool_ranking', 0, top_n - 1, withscores=True)
    
    scoreboard = []
    for tool_name, score in top_tools:
        tool_data = json.loads(await redis_client.hget('duffbot_tool_data', tool_name))
        reasons = await redis_client.lrange(f'duffbot_tool_reasons:{tool_name}', 0, -1)
        
        scoreboard.append(schemas.ToolScore(
            tool_name=tool_data['tool_name'],
            description=tool_data['description'],
            website=tool_data.get('website'),
            reasons=reasons,
            score=int(score)
        ))
    
    return schemas.ScoreboardResponse(top_tools=scoreboard)
