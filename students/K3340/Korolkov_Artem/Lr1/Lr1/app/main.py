from fastapi import FastAPI

from app.routers import auth, users, projects, tags, tasks, time_entries

app = FastAPI(title="Time Manager API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tags.router)
app.include_router(tasks.router)
app.include_router(time_entries.router)


@app.get("/")
def root():
    return {"message": "Time Manager API is running"}
