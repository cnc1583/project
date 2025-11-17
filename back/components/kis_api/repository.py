from datetime import datetime
import requests
from back.core.kis_config import KisSettings
from back.components.kis_api.get_token import get_token

class StockRepository:
    kis_settings = KisSettings()
    BASE_URL = kis_settings.KIS_API_URL
    KIS_API_CLIENT_ID = kis_settings.KIS_API_CLIENT_ID
    KIS_API_CLIENT_SECRET = kis_settings.KIS_API_CLIENT_SECRET

    async def get_stocks(self, start_date, end_date, item_code):

        token = get_token()
        url = f"{self.BASE_URL}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {token}",
            "appkey": self.KIS_API_CLIENT_ID,
            "appsecret": self.KIS_API_CLIENT_SECRET,
            "tr_id": "FHKST03010100",
        }

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": item_code,
            "FID_INPUT_DATE_1": start_date.replace("-", ""),
            "FID_INPUT_DATE_2": end_date.replace("-", ""),
            "FID_PERIOD_DIV_CODE": "D",
            "FID_ORG_ADJ_PRC": "1"
        }

        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        raw = res.json()
        items = raw.get("output2", [])

        result = []
        for item in items:
            date_raw = item.get("stck_bsop_date")
            price_raw = item.get("stck_clpr")

            if not (date_raw and price_raw):
                continue

            date = datetime.strptime(date_raw, "%Y%m%d").strftime("%Y-%m-%d")
            result.append({"date": date, "price": int(price_raw.replace(",", ""))})
        result.sort(key=lambda x: x["date"])

        return result