from datetime import datetime

from pandas import date_range
from pymongo import MongoClient

from src.schemes import SResponse, SRequest


def aggregate_payments(request: SRequest) -> SResponse:
    dt_from = request.dt_from
    dt_upto = request.dt_upto

    match request.group_type:
        case "month":
            group_id = {"year": {"$year": "$dt"}, "month": {"$month": "$dt"}}
            freq = "MS"
        case "day":
            group_id = {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"},
            }
            freq = "D"
        case "hour":
            group_id = {
                "year": {"$year": "$dt"},
                "month": {"$month": "$dt"},
                "day": {"$dayOfMonth": "$dt"},
                "hour": {"$hour": "$dt"},
            }
            freq = "H"
        case _:
            raise ValueError("Invalid group type")

    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["sampleDB"]
    collection = db["sample_collection"]

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {"_id": group_id, "total": {"$sum": "$value"}}},
        {"$sort": {"_id": 1}},
    ]

    result = collection.aggregate(pipeline)

    extra = {"day": 1} if request.group_type == "month" else {}
    result_dict = {
        datetime(**item["_id"], **extra).isoformat(): item["total"] for item in result
    }

    all_dates = date_range(start=dt_from, end=dt_upto, freq=freq)

    dataset = [result_dict.get(date.isoformat(), 0) for date in all_dates]
    labels = [date.isoformat() for date in all_dates]

    return SResponse(dataset=dataset, labels=labels)
