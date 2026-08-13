from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    return {
        "message": "Hey, I'm Lucca. This API proves I can take code from my machine to a live, HTTPS-secured domain.",
        "includes": "FastAPI > Docker > GitHub Actions > AWS EC2 > nginx > HTTPS.",
        "author": "Lucca Trevisan",
        "source": "github.com/luccatrevisan/fastapi-deploy-lab"
    }


@app.get("/health")
async def health_check():
    return {"status" : "ok"}
