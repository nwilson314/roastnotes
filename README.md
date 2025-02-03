# roastnotes - il gusto del caffè

## 📌 overview
**roastnotes** is a cozy, laid-back platform for **sharing and rating** coffee roasts—imagine an italian coffee house where every cup tells a story. users post their roasts with rich bean details and notes, then rate each brew method (v60, aeropress, moka pot, etc.) in a vibrant, artful way. while each roast is a personal creation, groups let you enjoy and compare experiences with your friends—just like gathering around a warm espresso bar.

---

## 🔹 features

### 1️⃣ roast creations & ratings
- **roast entries**: every roast is tied to its creator, featuring detailed bean info and narrative notes.
- **method-specific ratings**: capture the art of brewing with ratings that include:
  - **brew method** (v60, aeropress, moka pot, etc.)
  - **preferred method** flag (your top pick for that roast)
  - **ratio** (water-to-coffee magic)
  - **temperature** (the ideal warmth)
  - **grind** (texture and consistency details)
  - **tasting notes** (descriptive flavors and aromas)
  - **overall score** (a 100-point evaluation of excellence)

### 2️⃣ group ambience
- **community spirit**: groups aren’t about ownership—they’re a relaxed way to filter and appreciate your friends’ roasts, much like choosing a table in your favorite café.
- **flexible integration**: roasts remain personal, but groups create a vibrant collage of shared coffee moments.

### 3️⃣ aggregated charm
- enjoy aggregated roast ratings with an untappd-style flair.
- filter roasts by group for that curated espresso bar feel among your crew.

---

## 🔹 api - storage & retrieval

### current api endpoints
- `GET /users`, `POST /users` → manage your café regulars *(future: full auth integration)*
- `GET /groups`, `POST /groups` → set up your coffee circles
- `GET /roasts`, `POST /roasts`, `PATCH/DELETE /roasts/{id}` → handle your roast entries
- `GET /roasts/{id}/ratings`, `POST /roasts/{id}/ratings` → add and view detailed brew ratings

### planned api endpoints
- user authentication endpoints (think reserved seating with token-based access)
- endpoints to aggregate & filter roast ratings within groups

### orm & migration
- using **sqlmodel** for a clean, expressive schema
- managing schema evolution with **alembic** (autogenerate migrations)

---

## 🔹 database model

- **users**: our café regulars, holding details, roast submissions, and ratings.
- **groups**: friend circles, like cozy coffee tables connecting people via the **groupmember** join.
- **groupmember**: the link table that binds users and groups—keeping every shared cup in sync.
- **roasts**: individual roast entries, as personal as your favorite corner in a trattoria.
- **ratings**: method-specific evaluations that capture the essence of each brew.

---

## 🔹 frontend & ui

- built with **sveltekit** for a clean, vibrant, and intuitive web experience.
  - smooth roast submission and rating forms
  - dynamic dashboards to explore and compare coffee moments
- deployed on **vercel**, serving your coffee experiences worldwide.

---

## 🔹 deployment

- **backend**: fastapi with sqlmodel, serving fresh data from fly.io
- **database**: postgres—local dev via docker-compose, production on fly.io
- **frontend**: sveltekit on vercel for a responsive, espresso-fueled ui

---

## 🔹 roadmap

**short-term** (now):
- finalize models & endpoints for users, roasts, ratings, & groups
- roll out method-specific rating functionality with a vibrant ui
- deploy the mvp backend on fly.io and frontend on vercel

**medium-term**:
- integrate user authentication (token-based, like your personal café pass)
- refine group filtering and aggregated roast ratings for a smoother community vibe
- polish the ui with feedback to capture that authentic italian coffee house ambiance

**long-term**:
- expand brew method analytics (potentially with ai-assisted brewing tips)
- develop mobile shortcuts & browser extensions for on-the-go submissions
- explore deeper integrations with coffee resources and local café culture

---

## 🔹 development ethos & vibes

1. **italian coffee house essence**: cozy, laid back, yet vibrantly clean—like your favorite corner in a rome café.
2. **rapid, iterative flow**: build the mvp quickly, then refine based on real coffee chatter.
3. **future-proof design**: flexible models and endpoints ready for evolving needs.
4. **community over clutter**: personal roasts shared in a warm, inviting space.
5. **artful simplicity**: keep it unpretentious, letting the coffee (and code) speak for itself.

---

## 🔹 next steps

1. refine backend models & endpoints using sqlmodel and alembic.
2. set up the local dev environment (docker-compose for postgres).
3. deploy the mvp on fly.io (backend) and vercel (frontend).
4. iterate on ui/ux with genuine feedback from your coffee crew.
5. lay the groundwork for user auth and more detailed group filtering.

---

that's it. cozy & no frills.