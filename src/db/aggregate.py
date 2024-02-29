from datetime import datetime

from dateutil.relativedelta import relativedelta
from pandas import date_range
from pymongo import MongoClient

from src.schemes import SResponse, SRequest


def aggregate_payments_naive(request: SRequest) -> SResponse:
    dt_from = request.dt_from
    dt_upto = request.dt_upto

    match request.group_type:
        case "month":
            delta = relativedelta(months=1)
        case "day":
            delta = relativedelta(days=1)
        case "hour":
            delta = relativedelta(hours=1)
        case _:
            raise ValueError("Invalid group type")

    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client["sampleDB"]
    collection = db["sample_collection"]

    dataset = []
    labels = []

    while dt_from < dt_upto:
        next_dt = dt_from + delta

        result = collection.aggregate(
            [
                {"$match": {"dt": {"$gte": dt_from, "$lt": next_dt}}},
                {"$group": {"_id": None, "total": {"$sum": "$value"}}},
            ]
        )

        result_list = list(result)

        total = result_list[0]["total"] if result_list else 0
        dataset.append(total)
        labels.append(dt_from)

        dt_from = next_dt

    if dt_from == dt_upto:
        dataset.append(0)
        labels.append(dt_from)

    return SResponse(dataset=dataset, labels=labels)


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
