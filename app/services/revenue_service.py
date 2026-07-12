from collections import defaultdict

from app.database import db


class RevenueService:

    @staticmethod
    async def get_daily_revenue():

        bills = await db.Bill.find(
            {},
            {
                "netAmount": 1,
                "created_at": 1
            }
        ).to_list(None)

        revenue_map = defaultdict(float)

        for bill in bills:

            if not bill.get("created_at"):
                continue

            date = bill["created_at"].strftime("%Y-%m-%d")

            revenue_map[date] += float(
                bill.get("netAmount", 0)
            )

        result = []

        for date in sorted(revenue_map.keys()):

            result.append({

                "date": date,

                "revenue": round(
                    revenue_map[date],
                    2
                )

            })

        return result
    

    @staticmethod
    async def get_monthly_revenue():

        bills = await db.Bill.find(
            {},
            {
                "netAmount": 1,
                "created_at": 1
            }
        ).to_list(None)

        revenue_map = defaultdict(float)

        for bill in bills:

            if not bill.get("created_at"):
                continue

            month = bill["created_at"].strftime("%Y-%m")

            revenue_map[month] += float(
                bill.get("netAmount", 0)
            )

        result = []

        for month in sorted(revenue_map.keys()):

            result.append({

                "month": month,

                "revenue": round(
                    revenue_map[month],
                    2
                )

            })

        return result