# 🎶 Music Generator

An **AI-powered music creation platform** that transforms simple text prompts and lyrics into **studio-quality tracks** with **automatically generated cover art**.

Built with **Modal (GPU-accelerated AI inference)**, **Prisma + Postgres (data layer)**, **Cloudflare R2 (storage)**, and a **Next.js frontend** that feels as smooth as apps like *Suno*.

Our mission is to make **music generation as accessible as writing a sentence.**

---

## ✨ What You Can Do

* 🎼 **Generate music from text** — describe the vibe, style, or mood and instantly get a full track.
* ✍️ **Write or auto-generate lyrics** — use your own or let AI compose them for you.
* 🎨 **Cover art made for you** — every song gets a unique cover with Stable Diffusion.
* 📦 **Save, share, and replay** — songs and covers are stored in Cloudflare R2, linked to your account.
* 🔑 **Credits and subscriptions** — free tier to start, upgrade for unlimited creativity.

---

## 🏗️ How It All Fits Together

### 🔹 Frontend

* **Next.js 13 App Router** with **shadcn UI** for a sleek, modern interface.
* **TanStack React Query** for real-time song generation updates.
* **Zustand** for global UI state (e.g., audio player, modals).
* Users can:

  * Input prompts/lyrics
  * Manage their songs
  * See generation progress in real time

### 🔹 Backend

* **Modal (GPU cloud)** — runs the heavy lifting models:

  * ACE-Step → audio synthesis
  * Qwen2-7B → lyrics generation
  * SDXL Turbo → cover art generation
* **Prisma + Postgres** — user accounts, credits, song metadata.
* **Cloudflare R2** — storage for audio + cover art.
* **Bearer token auth** — secure, production-ready.
* **Inngest queues** — async processing of generation jobs.

---

## 🌍 System Flow

1. **User creates a song** from description or lyrics.
2. **Frontend API call** → queues job in database.
3. **Inngest worker** picks up event → calls Modal AI → uploads results to R2.
4. **Database updated** with R2 file references + status.
5. **Frontend polls with React Query** → updates user UI with progress + results.
6. **User listens, shares, or remixes** the track directly in the browser.

---

## 🚀 Quick Start

### Prerequisites

* Node.js 18+
* Postgres (or use Docker with the included compose file)
* Modal account with GPU access
* Cloudflare R2 account

### 1. Clone the repository

```bash
git clone https://github.com/edwardbudaza/music-generator.git
cd music-generator
```

### 2. Setup the backend

See [backend/README.md](./backend/README.md) for full instructions.

### 3. Setup the frontend

```bash
cd frontend
npm install
cp .env.example .env   # add your credentials
npm run dev
```

Access the app at: **[http://localhost:3000](http://localhost:3000)**

---

## 🛠️ Tech Stack

* **Frontend:** Next.js, React Query, Zustand, shadcn/ui
* **Backend:** Modal, FastAPI, Inngest
* **Database:** Prisma, PostgreSQL
* **Storage:** Cloudflare R2
* **AI Models:**

  * ACE-Step → music generation
  * Qwen2-7B → lyrics generation
  * Stable Diffusion XL Turbo → cover art

---

## 🎯 Vision

Music creation should be:

* **Accessible** → anyone can create, not just trained musicians.
* **Collaborative** → AI assists creativity, doesn’t replace it.
* **Scalable** → from hobbyist to pro studio.

We’re building the **future of AI-driven creativity**, where generating a song is as easy as posting a tweet.

---

## 🤝 Contributing

We welcome contributions — from frontend polish to backend scaling.

* Fork the repo
* Create a feature branch
* Submit a PR

---

## 📄 License

MIT License. Free for research, remix, and extension.

---

## 🆘 Support

* Open a GitHub issue
* Check backend/frontend READMEs for setup help
* Reach out via discussions