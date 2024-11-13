from fastapi import FastAPI, Depends
from functools import lru_cache

app = FastAPI()


@lru_cache(maxsize=32)
def get_cached_data(param: str):
    # 비싼 연산이나 데이터베이스 쿼리를 수행
    return {"param": param}


@app.get("/data")
def read_data(param: str, cached_data=Depends(get_cached_data)):
    return cached_data
