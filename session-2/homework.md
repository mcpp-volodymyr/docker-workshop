# 🟢 Core Task (recommended for everyone)

Make sure you are in the project folder (where `docker-compose.yml` is located).

Reproduce the demo from the session.

1. Start the application:

```bash
docker compose up --build
```

2. Open browser:  
http://localhost:8000

3. Submit one or two votes and verify that the results page updates.

4. Stop the application:
```bash
docker compose down
```

5. Start it again:
```bash
docker compose up
```

6. Open the app again and verify that the votes are still there.

---

# 🔵 Small Extension
Modify the web page content.  
For example:
- change a title
- change a button label
- or change some text in the HTML template
Then rebuild and start only the web service:
```bash
docker compose up --build -d web
```

Refresh the browser and verify the change.

---

# 🔵 Optional Challenge (if you want to go further)
Remove the database volume and observe what happens.

1. Stop and remove the application together with the volume:
```bash
docker compose down -v
```

2. Start it again:
```bash
docker compose up
```

3. Open the app and verify that the previous votes are gone.

Question:
- Why did the data survive after docker compose down, but disappear after `docker compose down -v`?

---

# 🧠 Hints
Useful commands:
```bash
docker compose ps
docker compose logs -f
docker compose restart db
docker compose restart web
```

---

# ✅ Success Criteria
You're done if you can:
- start the full application with Docker Compose
- access it in the browser
- submit votes and see the results
- modify the web app and see the change
- explain the difference between `docker compose down` and `docker compose down -v`
