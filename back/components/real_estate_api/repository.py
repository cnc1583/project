'''import aiohttp
from back.infrastructure.config.real_estate_config import RealEstateSettings

class RealEstateRepository:
    def __init__(self):
        real_estate_settings = RealEstateSettings()
        self.BASE_URL = real_estate_settings.REAL_ESTATE_API_URL
        self.CLIENT_KEY = real_estate_settings.REAL_ESTATE_API_KEY
        self.session = aiohttp.ClientSession()

    async def get_apartment_trades(self, region_code, ym, page_no: int = 1, num_of_rows: int = 100):
        params = {
            "serviceKey": self.CLIENT_KEY,
            "LAWD_CD": region_code,
            "DEAL_YMD": ym,
            "numOfRows": num_of_rows,
            "pageNo": page_no,
            "_type":"json"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"API 호출 실패 {resp.status}: {text}")

                data = await resp.json()

        items = data["response"]["body"]["items"]
        return items'''