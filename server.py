from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(query: str = Query(..., description="The chat query of user")):
    job = queue.enqueue(process_query, query)

    return {"status": "queued", "job": job.id}


@app.get("/job-stats")
def get_result(job_id: str = Query(..., description="Job ID")):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return {"result": result}
