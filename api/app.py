from fastapi import FastAPI, HTTPException
from program.scrapper_service import scrapper_pipeline

app = FastAPI()

@app.get('/')
def status():
    return {
        'status': 'running',
        'service': 'market-tracker'
    }

@app.post('/scrapper')
def run_scrapper(pages: int = 5):
    if pages <= 0:
        raise HTTPException(status_code=400, detail='Error: Number of pages must be a positive number')
    if pages > 20:
        raise HTTPException(status_code=400, detail='Error: Max number of pages is 20')
    
    report = scrapper_pipeline(pages)
    return report