# 🎵 Music Generator Frontend

A **Next.js App Router** frontend for AI-powered music generation.
It integrates with a backend powered by Modal (for AI inference), Inngest (for async job orchestration), Prisma (for persistence), and Cloudflare R2 (for storage).

The codebase follows a **Clean Architecture** pattern to keep the system **scalable, testable, and adaptable** to future AI models.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/edwardbudaza/music-generator.git
cd music-generator/frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL="postgresql://postgres:password@localhost:5432/frontend"

# Auth
BETTER_AUTH_SECRET="super-secret-random-string"

# Storage (Cloudflare R2)
R2_ENDPOINT_URL="https://<your-endpoint>.r2.cloudflarestorage.com"
R2_BUCKET_NAME="music-gen-output"
R2_ACCESS_KEY_ID="your-access-key"
R2_SECRET_ACCESS_KEY="your-secret-key"
R2_REGION="weur"
R2_CUSTOM_DOMAIN="https://music.example.com"

# Modal / Backend
API_BEARER_TOKEN="your-api-token"
GENERATE_FROM_DESCRIPTION="https://...modal.run"
GENERATE_FROM_DESCRIBED_LYRICS="https://...modal.run"
GENERATE_WITH_LYRICS="https://...modal.run"

# Environment
NODE_ENV="development"
```

> ⚠️ Make sure to replace placeholders with real values.
> The backend must be running and reachable for generation to work.

### 4. Start a local database

If you don’t already have Postgres installed, use the provided Docker setup:

```bash
docker-compose -f dev-database/docker-compose.yml up -d
```

### 5. Run migrations

```bash
npm run db:migrate
```

### 6. Start the development server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📂 Project Structure

```
src/
├── app/              # Next.js App Router (UI entrypoints, API routes)
├── components/       # Shared UI components (shadcn/ui)
├── core/             # Business logic: domain models, use-cases, contracts
├── infrastructure/   # Concrete adapters (Prisma repo, R2 storage, Modal AI, Inngest queue)
├── inngest/          # Event workflows & async job handlers
├── hooks/            # React Query + Zustand hooks for client state
├── lib/              # Helpers (env, utils, logger)
├── server/           # Thin wrappers for Prisma client & auth
└── styles/           # Global CSS
```

---

## 📘 Why This Architecture?

* **Clean Architecture:** separates business logic from frameworks.
* **Core layer:** holds domain models and use-cases. Pure, framework-agnostic, testable.
* **Infrastructure layer:** Prisma (DB), R2 (storage), Modal (AI), Inngest (queue). Easily swappable.
* **App layer:** API routes + UI pages, very thin, just call use-cases.
* **Hooks:** React Query (server state) + Zustand (client state). Clear responsibilities.
* **Components:** shadcn/ui style (lowercase filenames, composable building blocks).

---

## 🛠️ Tools and Why We Use Them

* **Next.js (App Router):** hybrid server components + client components, great DX.
* **Prisma:** type-safe DB access, schema migrations.
* **React Query (TanStack Query):** handles server state, caching, polling for job status.
* **Zustand:** lightweight store for global state (player, UI flags).
* **Inngest:** async job orchestration — perfect for long AI tasks.
* **Cloudflare R2:** cheap, S3-compatible object storage for audio & cover images.

---

## 🎼 How Music Generation Works

### Inputs

* Prompt (text description)
* Lyrics (optional)
* Flags (e.g., instrumental)
* Parameters (guidance scale, seed, steps, duration)

### Flow

1. User submits a form → `useGenerateSong` hook → API route `/api/queue-song`.
2. API route calls `createSong` use-case → saves song with `status=queued`.
3. Inngest picks up event → runs Modal AI job → uploads audio to R2 → updates DB (`status=completed`).
4. React Query polls job → once ready, frontend fetches presigned R2 URL → plays via Zustand-powered global player.

---

## 🗃️ Database Schema (Prisma)

The schema defines **users**, **songs**, and **credits**.

Key models:

* **User**: has subscription status, credits, and songs.
* **Song**: represents one generation job, with `status`, `prompt`, `lyrics`, `audioR2Key`.
* **CreditTransaction**: records usage/purchases of credits.
* **Category**, **Like**: metadata & user engagement.
* **Session**, **Account**, **Verification**: standard auth tables.

See [`prisma/schema.prisma`](./prisma/schema.prisma) for full details.

---

## 📚 Further Reading

To deeply understand this architecture:

* *Clean Architecture* — Robert C. Martin
* *Domain-Driven Design Distilled* — Vaughn Vernon
* *Designing Data-Intensive Applications* — Martin Kleppmann
* Prisma Docs: [https://pris.ly/d/prisma-schema](https://pris.ly/d/prisma-schema)
* TanStack Query Docs: [https://tanstack.com/query](https://tanstack.com/query)
* Zustand Docs: [https://zustand-demo.pmnd.rs](https://zustand-demo.pmnd.rs)

---

## ✅ Good Practices in This Repo

* Thin API routes → all business logic is in `core/`.
* Dependency inversion → infrastructure (Prisma, Modal, R2) is swappable.
* React Query vs Zustand → clear boundary between server state and UI state.
* Prisma migrations → schema evolves safely.
* Inngest → async jobs are reliable, retryable, observable.
* Presigned URLs → storage credentials are never exposed to clients.

---

## 🎯 Summary

This frontend is structured to:

* **Scale** as more AI models and features are added.
* **Adapt** to infrastructure changes (Modal → OpenAI, R2 → S3).
* **Remain Testable** thanks to Clean Architecture principles.
* **Deliver a polished UX** with React Query, Zustand, and shadcn UI.

