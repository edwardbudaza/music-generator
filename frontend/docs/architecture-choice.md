## 🎯 The Problem We’re Solving

We’re building a **music generation platform** that:

* integrates **AI (Modal)**,
* needs **async job processing (Inngest)**,
* stores results in **Cloudflare R2**,
* and serves a **rich Next.js frontend**.

This isn’t a simple CRUD app. It has multiple moving parts, and we expect it to **evolve quickly** (new features like remixing, voice models, collaboration, etc.).

So, the architecture must be:

* **Scalable** → easy to add features.
* **Maintainable** → new devs can onboard fast.
* **Testable** → core business rules can be validated without full stack.
* **Flexible** → we can swap out Modal/R2/Inngest if needed.

---

## 🏛️ Why Clean Architecture

1. **Separation of Concerns**

   * Domain rules (e.g. “a Song has a status: queued, processing, completed”) are kept pure in the `core/domain`.
   * Business flows (e.g. “queue a song, generate with AI, store result”) live in `core/application`.
   * Infrastructure (Prisma, Modal, R2, Inngest) is *just details*. If we change the provider, we only update that layer.
   * Interfaces (API routes, React hooks) are thin — they call use-cases, not business logic.

   👉 This prevents the “ball of mud” problem where UI, business, and infrastructure are all tangled together.

2. **Technology-Agnostic Core**

   * If tomorrow we move from Modal → OpenAI, or R2 → AWS S3, the **domain and use-cases don’t change**. We just swap the adapter.
   * The company’s *business logic* survives tech churn.

3. **Testability**

   * Use-cases can be unit tested by mocking `SongRepository`, `QueueService`, etc.
   * No need for a running DB or Inngest in every test run.

4. **Team Scaling**

   * Different teams can own different layers:

     * Backend team: infrastructure adapters.
     * AI team: modal/openai adapters.
     * Frontend team: React UI + hooks.
   * Clear boundaries reduce friction and miscommunication.

5. **Long-Term Value**

   * For a company investing in this app, Clean Architecture is a hedge: it makes the system adaptable to business pivots or vendor changes.

---

## 🔄 Alternatives We Considered

### 1. **Classic MVC (Model-View-Controller)**

* **Pros:** Simple, familiar to most devs, faster to start.
* **Cons:** In practice, business logic leaks into controllers and models. Tight coupling makes it hard to swap Modal/R2/Inngest later. Testing is painful because DB and external APIs are everywhere.

### 2. **Service-Oriented / Microservices**

* **Pros:** Strong isolation, independent scaling, clear service boundaries.
* **Cons:** Overkill for a team our size. Adds network latency, deployment complexity, service discovery, CI/CD overhead. We’d spend more time on infrastructure than product.

### 3. **Feature-Folder Structure (by module)**

* **Pros:** Keeps related files together (e.g., all “song” files in one folder). Works well in Next.js.
* **Cons:** Without discipline, business logic still gets mixed into infrastructure and UI. It’s “organized MVC,” not clean boundaries.

---

## 🏆 Why Clean Architecture Wins Here

* **More disciplined than MVC.**
* **Less overhead than microservices.**
* **More robust than feature-folder alone.**
* Fits perfectly with Next.js (App Router for UI, API routes for interfaces) and Inngest (asynchronous queue fits the use-case layer).

In short:

> *“We chose Clean Architecture because it lets us build a system that’s adaptable, testable, and scalable, without the complexity of microservices. It gives us guardrails to avoid tech debt as the app grows, while still delivering fast with Next.js and Inngest.”*

