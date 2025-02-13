# roastnotes - il gusto del caffè

## 📌 overview
**roastnotes** is a cozy, laid-back platform for **sharing and rating** coffee roasts—imagine an italian coffee house where every cup tells a story. users post their roasts with rich bean details and narrative notes, then rate each brew method (v60, aeropress, moka pot, etc.) in a vibrant, artful way. while each roast is a personal creation, groups let you enjoy and compare experiences with your friends—just like gathering around a warm espresso bar.

---

## 🔹 features

### 1️⃣ roast creations & ratings
- **roast entries**: every roast is tied to its creator, featuring detailed bean info and narrative notes. bean details now live in a dedicated table with structured info (species, cultivar, processing method, altitude) plus an extra jsonb field for additional metadata.
- **enhanced method-specific ratings**: capture the art of brewing with ratings that include:
  - **brew method** (v60, aeropress, moka pot, etc.)
  - **preferred method** flag (your top pick for that roast)
  - **ratio** (water-to-coffee magic)
  - **temperature** (the ideal warmth)
  - **grind** (texture and consistency details)
  - **tasting notes** (descriptive flavors and aromas)
  - **overall score** (a 100-point evaluation of excellence)
  
  backed by a caching system for global and group-specific stats, managed atomically via the rating manager service.
- **rating manager service**: handles adding/updating ratings, atomic transactions, and cached statistics updates—including group-specific calculations.
- **roast level**: each roast now includes a roast level field, managed as an enum (unspecified, light, medium, dark) using postgres’ native enum type for consistency.

### 2️⃣ group ambience
- **community spirit**: groups aren’t about ownership—they’re a relaxed way to filter and appreciate your friends’ roasts, much like choosing a table in your favorite café.
- **group roast collections**: groups now feature dedicated roast collections (via the new group roast collection model) that track which user added a roast, include cached group-specific rating stats, and let you add contextual notes.
- **flexible integration**: roasts remain personal, but groups create a vibrant collage of shared coffee moments.

### 3️⃣ aggregated charm
- enjoy aggregated roast ratings with an untappd-style flair—maybe even some letterboxd vibes.
- filter roasts by group for that curated espresso bar feel among your crew.

---

## mvp frontend (latest sveltekit)
- **landing page**: for non-logged in users, a top section offers a brief overview with a “login?” button and a placeholder for an image.
- **common header**: a fixed, minimalist header displaying either the user’s profile pic or a “login?” button.
- **roasts view**: logged in users see trending roasts (most recent) if not in a group, or a tabbed interface (group vs trending) when in a group.
- **profile page**: a barebones page showcasing basic user info.

---

## 🔹 api - storage & retrieval

### current api endpoints
- GET /users, POST /users → manage your café regulars *(future: full auth integration)*
- GET /groups, POST /groups → set up your coffee circles
- GET /roasts, POST /roasts, PATCH/DELETE /roasts/{id} → handle your roast entries
- POST /roasts/rate → add or update a rating via the rating manager
- GET /roasts/{roast_id}/ratings → view detailed brew ratings for a roast
- GET /ratings/trending → explore global trends
- GET /groups/{group_id}/roasts → fetch group-specific roast collections

### planned api endpoints
- user authentication endpoints (think reserved seating with token-based access)
- endpoints to further aggregate & filter roast ratings within groups

### orm & migration
- using **sqlmodel** for a clean, expressive schema
- managing schema evolution with **alembic** (autogenerate migrations)

---

## 🔹 database model

- **users**: our café regulars, holding details, roast submissions, and ratings.
- **groups**: friend circles, like cozy coffee tables connecting people via the groupmember join.
- **groupmember**: the link table that binds users and groups—keeping every shared cup in sync.
- **group roast collection**: a new model managing group-specific roast collections, tracking the user who added a roast, holding cached group rating stats, and storing contextual notes.
- **roasts**: individual roast entries, as personal as your favorite corner in a trattoria, now with a roast level (unspecified, light, medium, dark) for added consistency.
- **bean details**: a dedicated table for bean info that stores structured attributes (species, cultivar, processing method, altitude) with an extra jsonb field for extra metadata.
- **ratings**: an enhanced, method-specific model capturing brew method, preferred flag, ratio, temperature, grind, tasting notes, and overall score—with efficient caching for both global and group-specific evaluations.

---

## 🔹 deployment

- **backend**: fastapi with sqlmodel, serving fresh data from fly.io
- **database**: postgres—local dev via docker-compose, production on fly.io
- **frontend**: sveltekit on vercel for a responsive, espresso-fueled ui

---

## 🔹 roadmap

**short-term** (now):
- finalize models & endpoints for users, roasts, ratings, groups, and group roast collections
- roll out the enhanced, method-specific rating functionality with its vibrant ui and robust caching
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

1. user auth 
2. implement refined group filtering (aggregated ratings) with real-time updates
3. deploy the mvp on fly.io (backend) and vercel (frontend)
4. iterate on ui/ux with genuine feedback from your coffee crew

that's it. cozy & no frills.