import io
from typing import List
import pandas as pd


def to_csv(data: List[dict]):
    df = pd.DataFrame.from_records(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    return stream


def to_xls(data: List[dict]):
    df = pd.DataFrame.from_records(data)
    stream = io.BytesIO()
    df.to_excel(stream, index=False)
    return stream

