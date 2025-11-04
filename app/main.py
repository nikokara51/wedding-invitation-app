import os
import csv
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, func
import databases
from app.models import guests
from app.database import DATABASE_URL

# Initialize database
database = databases.Database(DATABASE_URL)

# Initialize FastAPI
app = FastAPI()

# Serve static files (images, backgrounds)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Startup: connect to DB and populate from CSV if empty
@app.on_event("startup")
async def startup():
    await database.connect()
    count_query = select(func.count()).select_from(guests)
    count = await database.fetch_val(count_query)

    if count == 0:
        await reload_csv_from_file()


# Shutdown: disconnect database
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Helper function to load CSV into database
async def reload_csv_from_file():
    csv_path = os.path.join(os.path.dirname(__file__), "../data/guests.csv")
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV file not found at {csv_path}")
        return
    
    # Optional: clear table first
    await database.execute(guests.delete())
    
    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            slug = row.get("slug") or row["name"].lower().replace(" ", "_")
            query = guests.insert().values(
                name=row["name"],
                email=row.get("email"),
                slug=slug,
                church_name=row.get("church_name"),
                church_lat=float(row.get("church_lat") or 0),
                church_lng=float(row.get("church_lng") or 0),
                reception_name=row.get("reception_name"),
                reception_lat=float(row.get("reception_lat") or 0),
                reception_lng=float(row.get("reception_lng") or 0),
                rsvp=None
            )
            await database.execute(query)
    print("✅ Guests loaded from CSV")


# Endpoint to reload CSV on demand (GET/POST)
@app.api_route("/reload-csv", methods=["GET", "POST"])
async def reload_csv():
    await reload_csv_from_file()
    return HTMLResponse("""
        <html>
        <body style="text-align:center; font-family:Playfair Display, serif;">
            <h1>CSV reloaded successfully!</h1>
            <a href="/">Back to home</a>
        </body>
        </html>
    """)


# Landing page
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse("""
    <html>
    <head>
        <title>Welcome to Our Wedding</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Playfair Display', serif;
                background-image: url('/static/background.jpg');
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 0;
                color: #4B2E2E;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                text-align: center;
            }
            .overlay {
                background: rgba(255, 244, 230, 0.95);
                padding: 50px 70px;
                border-radius: 25px;
                box-shadow: 0 15px 30px rgba(0,0,0,0.25);
            }
            h1 { font-size: 48px; color: #C84B31; margin-bottom: 20px; }
            p { font-size: 20px; margin-bottom: 30px; color: #5D4037; }
            button {
                padding: 15px 30px;
                font-size: 18px;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                background: linear-gradient(135deg, #FFB6A9 0%, #FFD6C5 100%);
                color: #6B4226;
                transition: 0.3s;
            }
            button:hover { transform: translateY(-3px); }
            form { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="overlay">
            <h1>Welcome to Our Wedding!</h1>
            <p>We are delighted to invite you to our special day.</p>
            <p>Please use your personal invitation link to RSVP.</p>
            <form action="/reload-csv" method="post">
                <button type="submit">Reload Guests from CSV</button>
            </form>
        </div>
    </body>
    </html>
    """)


# Invitation page
@app.get("/invite/{slug}", response_class=HTMLResponse)
async def invite(slug: str):
    query = guests.select().where(guests.c.slug == slug)
    guest = await database.fetch_one(query)
    if not guest:
        raise HTTPException(status_code=404, detail="Invite not found")

    html_content = f"""
    <html>
    <head>
        <title>Wedding Invitation for {guest['name']}</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Playfair Display', serif;
                background-image: url('/static/background.jpg');
                background-size: cover;
                background-position: center;
                margin: 0;
                padding: 0;
                color: #4B2E2E;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .overlay {{
                background: rgba(255, 244, 230, 0.95);
                padding: 50px 60px;
                border-radius: 25px;
                box-shadow: 0 15px 30px rgba(0,0,0,0.25);
                text-align: center;
                max-width: 520px;
            }}
            h1 {{ color: #C84B31; font-size: 38px; margin-bottom: 15px; }}
            h2 {{ color: #E07A5F; font-size: 24px; margin-bottom: 20px; }}
            p {{ font-size: 18px; margin: 10px 0; color: #5D4037; }}
            a {{ color: #E07A5F; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            button {{
                padding: 14px 28px;
                margin: 10px;
                border: none;
                border-radius: 30px;
                cursor: pointer;
                font-size: 18px;
                transition: 0.3s;
                box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            }}
            .yes {{
                background: linear-gradient(135deg, #FFB6A9 0%, #FFD6C5 100%);
                color: #6B4226;
            }}
            .yes:hover {{ transform: translateY(-3px); }}
            .no {{
                background: linear-gradient(135deg, #FFCDB2 0%, #FFE5D4 100%);
                color: #6B4226;
            }}
            .no:hover {{ transform: translateY(-3px); }}
        </style>
    </head>
    <body>
        <div class="overlay">
            <h1>Dear {guest['name']}</h1>
            <h2>We invite you to our wedding!</h2>
            <p><strong>Church:</strong> {guest['church_name']} <br>
            <a href="https://www.google.com/maps?q={guest['church_lat']},{guest['church_lng']}" target="_blank">View on map</a></p>
            <p><strong>Reception:</strong> {guest['reception_name']} <br>
            <a href="https://www.google.com/maps?q={guest['reception_lat']},{guest['reception_lng']}" target="_blank">View on map</a></p>
            <h3>Will you attend?</h3>
            <form method="post" action="/rsvp/{guest['slug']}">
                <button type="submit" name="rsvp" value="yes" class="yes">Yes</button>
                <button type="submit" name="rsvp" value="no" class="no">No</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(html_content)


# RSVP endpoint
@app.post("/rsvp/{slug}")
async def rsvp(slug: str, rsvp: str = Form(...)):
    query = guests.update().where(guests.c.slug == slug).values(rsvp=rsvp)
    await database.execute(query)
    return HTMLResponse(f"""
        <html>
        <body style="text-align:center; font-family:Playfair Display, serif;">
            <h1>Thank you, your RSVP is recorded as '{rsvp.upper()}'!</h1>
            <a href="/invite/{slug}">Back to invitation</a>
        </body>
        </html>
    """)
