# 🟢 Core Task (recommended for everyone)

Make sure you are in the project folder (where Dockerfile is located).

Reproduce the demo from the session.

1. Build the Docker image:

```bash
docker build -t demo-http .
```

2. Run the container:

```bash
docker run --rm -p 8000:8000 demo-http
```

3. Open in browser:  
http://localhost:8000

4. Modify the response:
- Change the message in `server.py` (e.g. "Hello from Docker!" → "Hello from me!")
- Rebuild the image
- Run again and verify the change

---

# 🔵 Small Extension

Change the port mapping:

```bash
docker run --rm -p 9000:8000 demo-http
```

Then open:  
http://localhost:9000

---

# 🔵 Optional Challenge (if you want to go further)

Use docker-compose:

1. Create `docker-compose.yml`

2. Minimal example:

```yml
services:
  app:
    build: .
    ports:
      - "8000:8000"
```

3. Run:

```bash
docker compose up
```

4. Open in browser:  
http://localhost:8000

---

# 🧠 Hints

If something doesn’t work:

```bash
docker ps
docker logs <container_id>
```

Tip: use `docker ps` to find the container ID.

---

# ✅ Success Criteria

You're done if you can:
- run the container
- access it in the browser
- modify the response and see the change
