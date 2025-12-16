import FinanceDataReader as fdr
from back.cache.cache import RedisCache
from back.infrastructure.config.alias_map import get_alias_item_code

cache = RedisCache()

class StockMapper:
    DICT_KEY = "listed_company"

    # noinspection PyMethodMayBeStatic
    async def fetch_domestic_stocks(self):
        domestic_dict = {}

        try:
            kospi = fdr.StockListing("KOSPI")
            domestic_dict.update(dict(zip(kospi["Name"], kospi["Code"])))

            kosdaq = fdr.StockListing("KOSDAQ")
            domestic_dict.update(dict(zip(kosdaq["Name"], kosdaq["Code"])))

        except Exception as e:
            print("domestic dict failed")

        return domestic_dict

    # noinspection PyMethodMayBeStatic
    async def fetch_overseas_stocks(self):
        overseas_dict = {}

        try:
            nasdaq = fdr.StockListing("NASDAQ")
            overseas_dict.update(dict(zip(nasdaq["Name"], nasdaq["Symbol"])))

            nyse = fdr.StockListing("NYSE")
            overseas_dict.update(dict(zip(nyse["Name"], nyse["Symbol"])))

            amex = fdr.StockListing("AMEX")
            overseas_dict.update(dict(zip(amex["Name"], amex["Symbol"])))

        except Exception as e:
            print("overseas dict failed")

        return overseas_dict

    async def load_stocks(self):
       listed_company = await cache.get(self.DICT_KEY)

       if listed_company:
           return listed_company

       listed_company = {}

       domestic_dict = await self.fetch_domestic_stocks()
       overseas_dict = await self.fetch_overseas_stocks()
       listed_company.update(domestic_dict)
       listed_company.update(overseas_dict)

       await cache.set(self.DICT_KEY, listed_company, expire=24 * 60 * 60)

       return listed_company

    # noinspection PyMethodMayBeStatic
    async def get_item_code(self, name):
        return get_alias_item_code(name)

    async def get_listed_company(self):
        return await cache.get(self.DICT_KEY) or {}