import aiohttp
import json
from back.infrastructure.config.naver_config import NaverSettings

class TrendRepository:
    naver_settings = NaverSettings()
    BASE_URL = naver_settings.NAVER_API_URL
    CLIENT_ID = naver_settings.NAVER_API_CLIENT_ID
    CLIENT_SECRET = naver_settings.NAVER_API_CLIENT_SECRET

    async def get_trends(self, start_date, end_date, keyword):

        body = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "date",
            "keywordGroups": [{"groupName": keyword, "keywords": [keyword]}],
        }

        headers = {
            "X-Naver-Client-Id": self.CLIENT_ID,
            "X-Naver-Client-Secret": self.CLIENT_SECRET,
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.BASE_URL, headers=headers, json=body) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"Naver API error: {resp.status}, {text}")
                res_json = await resp.json()

                result = res_json.get("results", [])
                data = []
                for item in result:
                    for d in item.get("data", []):
                        date = d.get("period")
                        value = d.get("ratio")
                        data.append({"date": date, "value": value})

                json.dumps(data)
                return data