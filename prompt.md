# EduProof AI — Complete System Build Prompt


---

## SYSTEM IDENTITY

You are building **EduProof AI** — a full-stack, AI-powered academic credential verification platform that builds a **Digital Academic Twin** for every candidate. The system does not merely check whether a document is real or fake. It verifies whether an entire academic identity is internally consistent, externally corroborated, and temporally coherent. The output is a nuanced, multi-dimensional **Academic Trust Score** used by HR teams and organisations to make high-confidence hiring decisions.

---

## TECH STACK

- **Frontend**: Next.js 14 (App Router), Tailwind CSS, shadcn/ui, Recharts
- **Backend**: Python FastAPI
- **AI/ML Layer**: OpenAI GPT-4o (or Claude 3.5 Sonnet) via API for analysis; open-source OCR via Tesseract / pytesseract; Sentence-Transformers for semantic similarity
- **Database**: PostgreSQL (primary relational data), Neo4j (Academic Trust Graph), Redis (job queues / caching)
- **Storage**: AWS S3 (or Supabase Storage) for uploaded documents
- **Authentication**: NextAuth.js (JWT-based, role-aware: Admin / HR / Candidate)
- **Queue**: Celery + Redis for async verification pipelines
- **Web Scraping**: Playwright / httpx for LinkedIn, GitHub, college websites
- **Deployment**: Docker Compose for local dev; production-ready Dockerfile per service

---

## ROLES AND ACCESS CONTROL

Three distinct roles exist in the system. Build middleware that enforces role-based access at every route.

### 1. CANDIDATE
- Self-registers with name, email, password
- Builds their profile: uploads resume, transcripts, certificates, project links, GitHub URL, LinkedIn URL
- Browses job listings posted by organisations
- Applies to a job (one-click apply, attaches their profile)
- Views their own Application Dashboard showing:
  - All jobs applied to
  - Current status per application: `Applied → Under Review → Verification Running → Interview Selected / Rejected`
  - If **selected for interview**: a personalised card explaining *why* they were selected — which specific skills stood out, which credentials were verified, what unique signals (GitHub commits, certifications, live project demos) made them stand out from others
  - If **rejected at any stage**: a transparent rejection card showing *exactly which stage they failed* and *why*:
    - Resume ATS score too low (score shown)
    - Degree/CGPA mismatch or unverifiable institution
    - Skill claimed without any supporting evidence (no project, no certificate, no GitHub activity)
    - Timeline contradiction detected (e.g. claimed skill predates any digital evidence)
    - AI-generated or plagiarised content detected in portfolio/SOP
    - Document tampering suspected
    - GitHub/LinkedIn activity inconsistent with claimed experience level

### 2. HR / ORGANISATION
- Registers organisation with name, industry, HR contact details
- Posts job listings with: title, description, required skills, minimum CGPA, degree type required, experience type (fresher/experienced), deadline
- Views a **Recruitment Dashboard** showing:
  - All jobs posted
  - Per job: total applicants, verification status breakdown, shortlisted candidates, rejected candidates
  - For every candidate who applied: their Academic Trust Score radar chart, per-layer confidence scores, red flags, green flags
  - After verification pipeline completes: a ranked shortlist of candidates selected for interview, each with a detailed profile card showing:
    - Overall Trust Score (out of 100)
    - Why this candidate was selected (unique differentiators, verified standout skills, consistent academic journey)
    - Skill-by-skill verification status
    - Document confidence summary
    - GitHub/LinkedIn activity summary
    - ATS resume score
  - A separate rejected candidates panel with per-candidate failure reasons for audit/compliance

### 3. ADMIN
- Full system visibility
- Views all organisations, all candidates, all jobs, all verification runs
- Can manually override a Trust Score with a note
- Sees system health: queue depth, average verification time, fraud detection stats, daily active users
- Can blacklist a candidate or organisation
- Manages job category taxonomy, institution database, skill ontology

---

## DATABASE SCHEMA

Design and implement the following tables in PostgreSQL. Use Alembic for migrations.

```
users (id, email, password_hash, role [admin|hr|candidate], created_at, is_active)

organisations (id, user_id FK, name, industry, website, verified, created_at)

candidates (id, user_id FK, full_name, phone, dob, city, github_url, linkedin_url, resume_url, created_at)

jobs (id, org_id FK, title, description, required_skills JSON, min_cgpa FLOAT, degree_required VARCHAR, experience_type [fresher|experienced], deadline DATE, is_active, created_at)

applications (id, candidate_id FK, job_id FK, status [applied|under_review|verifying|interview_selected|rejected], applied_at, updated_at)

verification_reports (id, application_id FK, ats_score FLOAT, trust_score FLOAT, layer_scores JSON, red_flags JSON, green_flags JSON, rejection_reason TEXT, selection_reason TEXT, raw_analysis JSON, created_at)

documents (id, candidate_id FK, type [resume|transcript|certificate|other], s3_url, uploaded_at)

skills (id, candidate_id FK, skill_name, claimed_level, evidence_type [project|certificate|github|none], verified BOOL)

academic_records (id, candidate_id FK, degree, institution, cgpa FLOAT, start_year INT, end_year INT, current_semester INT, verified BOOL, institution_url_checked TEXT)

certificates (id, candidate_id FK, title, issuer, issue_date, expiry_date, credential_url, verified BOOL)

projects (id, candidate_id FK, title, description, skills_used JSON, github_link, live_link, verified BOOL)
```

Also initialise a **Neo4j graph database** where nodes represent: Candidate, Skill, Certificate, Institution, Project, Employer, and edges represent: HAS_SKILL, STUDIED_AT, COMPLETED_PROJECT, EARNED_CERTIFICATE, WORKED_AT. The Trust Intelligence layer queries this graph to detect structural contradictions and missing evidence chains.

---

## FRONTEND — PAGE BY PAGE

### Public Pages
- `/` — Landing page: hero section explaining EduProof AI, CTA buttons for HR signup and Candidate signup
- `/login` — Unified login with role auto-detection
- `/register/candidate` — Candidate registration form
- `/register/hr` — HR/Organisation registration form

### Candidate Pages (protected, role = candidate)
- `/candidate/dashboard` — Application overview: cards per application with live status badge and pipeline progress bar
- `/candidate/profile` — Build/edit profile: personal info, education, skills, projects, upload documents, add GitHub/LinkedIn
- `/candidate/jobs` — Browse active job listings with filter by skill, degree, CGPA requirement
- `/candidate/jobs/[id]` — Job detail page with Apply button
- `/candidate/applications/[id]` — Detailed view of one application:
  - Live status tracker (step-by-step pipeline visual)
  - If selected: Why You Were Selected card (green, positive, specific)
  - If rejected: What Went Wrong card (transparent, stage-by-stage, constructive)

### HR Pages (protected, role = hr)
- `/hr/dashboard` — Organisation overview: active jobs, total applicants, pending verifications, shortlisted count
- `/hr/jobs` — Manage job listings
- `/hr/jobs/new` — Create job listing form
- `/hr/jobs/[id]` — Job detail with applicant table: sortable by Trust Score, filter by status
- `/hr/jobs/[id]/applicants/[applicationId]` — Full candidate verification report:
  - Trust Score radar chart (6 axes: Document, Content, Evidence, Skill, Identity, Graph Confidence)
  - ATS score with keyword match breakdown
  - Per-verification-layer result cards
  - GitHub analysis: repo count, commit frequency chart, top languages, last active date
  - LinkedIn analysis: posts found, connections tier, activity recency
  - Red flags panel (if any)
  - Green flags panel
  - Final recommendation: Interview / Reject with reason narrative

### Admin Pages (protected, role = admin)
- `/admin/dashboard` — System stats: users, orgs, verifications run today, fraud detections
- `/admin/users` — User management table
- `/admin/organisations` — Org management table
- `/admin/verifications` — All verification runs with filter by status/date
- `/admin/override/[reportId]` — Manual score override form with audit note

---

## BACKEND — API ROUTES

Build all routes under FastAPI with `/api/v1/` prefix. Use Pydantic models for all request/response schemas.

### Auth
- `POST /auth/register` — Register (candidate or hr)
- `POST /auth/login` — Returns JWT
- `GET /auth/me` — Current user profile

### Candidates
- `GET /candidates/me` — Own profile
- `PUT /candidates/me` — Update profile
- `POST /candidates/me/documents` — Upload document to S3, save record
- `GET /candidates/me/applications` — List own applications with status

### Jobs
- `GET /jobs` — List active jobs (public, paginated, filterable)
- `GET /jobs/{id}` — Job detail
- `POST /jobs` — Create job (HR only)
- `PUT /jobs/{id}` — Update job (HR only)
- `DELETE /jobs/{id}` — Deactivate job (HR only)
- `POST /jobs/{id}/apply` — Candidate applies (creates application record, triggers async verification pipeline)

### Applications
- `GET /applications/{id}` — Get application + verification report (candidate sees own only; HR sees all for their org)
- `GET /hr/jobs/{jobId}/applications` — All applications for a job (HR only)

### Verification
- `POST /verify/{applicationId}` — Manually trigger verification (admin/hr)
- `GET /verify/{applicationId}/status` — Check pipeline progress

### Admin
- `GET /admin/stats` — System overview numbers
- `GET /admin/users` — All users
- `POST /admin/override/{reportId}` — Manual score override

---

## THE VERIFICATION PIPELINE (CORE ENGINE)

This is the heart of the system. When a candidate applies for a job, an async Celery task is triggered. The pipeline runs the following stages in sequence. Each stage produces a sub-score (0–100) and a list of flags. The final Trust Score is a weighted average.

---

### STAGE 0 — ATS RESUME SCORER

Before any verification, compute an ATS compatibility score.

**Process:**
1. Extract raw text from the uploaded resume PDF using pdfplumber or pytesseract
2. Parse the job description's required skills list
3. Use Sentence-Transformers (all-MiniLM-L6-v2) to compute semantic similarity between resume text chunks and each required skill
4. Count exact keyword matches, partial matches, and semantic near-matches
5. Score = weighted formula: (exact_match_ratio * 0.5) + (semantic_match_ratio * 0.3) + (formatting_score * 0.2)
6. Formatting score checks: proper section headings present, no spelling errors (use pyspellchecker), consistent date formats, no tables-in-PDF rendering issues, no excessive graphics
7. Output: `ats_score` (0–100), `matched_keywords` list, `missing_keywords` list, `formatting_flags` list

---

### STAGE 1 — LAYER 1: DOCUMENT CONFIDENCE (Certificate DNA Analysis)

**Weight: 15%**

For each uploaded document (degree certificate, transcript, offer letters):

1. **Metadata validation**: Extract PDF metadata (creator, creation date, modification date). Flag if modified date is after issue date, or if creator software is unusual for academic documents
2. **Logo and seal verification**: Use OCR to extract text from document. Use a pre-built reference database of 500+ Indian university logo regions and seal text patterns. Flag if institution name in document does not match logo/seal region
3. **OCR consistency check**: Run OCR twice (Tesseract + EasyOCR). Compare outputs. High divergence = possible image manipulation
4. **Font anomaly detection**: Check if font embedding in PDF is consistent. Mixed fonts in the same text block = editing indicator
5. **Digital signature check**: Check for embedded digital signatures (common in DigiLocker documents). Flag if claimed-DigiLocker document has no valid signature
6. **Tamper heuristics**: Check pixel entropy in critical regions (name field, CGPA field, date field). High localised entropy = possible Photoshop editing

**Output**: `document_confidence_score`, list of document-level flags

---

### STAGE 2 — LAYER 2: CONTENT CONFIDENCE (Hallucination & Inflation Detection)

**Weight: 15%**

1. **AI-generated text detection**: Run resume text through a GPT-based classifier prompt and cross-check with a local logistic regression model trained on human vs AI resume corpora. Flag if AI probability > 0.7
2. **Achievement exaggeration detection**: Extract achievement statements ("Led a team of X", "Increased revenue by Y%", "Built a system handling Z requests/sec"). Run semantic similarity against a calibrated believability corpus. Flag outliers
3. **Skill inflation detection**: Extract all skill claims. For each skill, build a believability profile: does the candidate's experience timeline allow enough time to acquire this skill at the claimed level? Flag inconsistencies
4. **Portfolio plagiarism**: If project descriptions or GitHub README content is submitted, run Sentence-Transformer cosine similarity against a known-plagiarism corpus and public project databases. Flag if similarity > 0.85
5. **SOP / Cover letter AI detection**: Same AI-text classifier applied to any written statement

**Output**: `content_confidence_score`, list of content-level flags

---

### STAGE 3 — LAYER 3: EVIDENCE CONFIDENCE (Multi-Source Cross-Check)

**Weight: 20%**

This stage cross-checks every claimed credential against external sources.

#### 3A — Academic Record Verification (CRITICAL FOR FRESHERS)

For a fresher or currently-pursuing student:

1. **Extract from resume**: degree name, institution name, CGPA, start year, end year (or "pursuing"), current semester/year
2. **Degree validation**:
   - Search the institution's official website using a web scraper (Playwright)
   - Navigate to the academics/programmes page
   - Extract the list of offered programmes
   - **If the candidate claims B.Tech but the institution only offers BCA/BSc — REJECT immediately** with reason: "Institution does not offer claimed degree"
   - If institution website is unreachable, flag as "Institution unverifiable — manual check required" (do NOT auto-reject)
3. **CGPA plausibility check**:
   - Cross-reference claimed CGPA against the institution's grading scale (extract from website if available)
   - Flag if CGPA is above the institution's maximum scale (e.g. claiming 9.8/10 at a university that uses a 4.0 GPA system)
4. **Current student verification**:
   - If candidate marks themselves as "currently pursuing", require either:
     - Current year marksheet/grade report (uploaded document), OR
     - Student ID card (uploaded document)
   - If neither is provided, flag as "No current enrollment evidence — verification incomplete"
   - If marksheet is provided, OCR-extract semester/year and cross-check with claimed current year
5. **Marksheet timeline check**:
   - Extract all semester results from uploaded marksheets
   - Verify that semesters are sequential with no impossible gaps
   - Verify that the number of semesters completed matches the claimed current year of study

#### 3B — Skill-to-Evidence Mapping (CRITICAL)

For every skill listed on the resume:

1. **Project mapping**: Check if any project listed uses or required this skill. If yes — skill has project evidence (strong signal)
2. **Certificate mapping**: Check if any uploaded certificate covers this skill. If yes — skill has certificate evidence (medium signal)
3. **GitHub mapping**: Check GitHub repos/commit messages for use of this skill (Stage 3C provides the data). If yes — skill has activity evidence (strong signal)
4. **The Evidence Rule**:
   - If a skill has ZERO evidence across projects, certificates, and GitHub — flag it as "Skill claimed without evidence"
   - **A certificate is the minimum acceptable evidence for a claimed skill with no project or GitHub activity**
   - Skills with no evidence are NOT auto-rejection grounds alone, but accumulate as negative signals in the Trust Score
   - Exception: soft skills (communication, leadership, teamwork) are not checked for evidence

#### 3C — GitHub Analysis

1. Use the GitHub REST API (unauthenticated or with token) to fetch:
   - List of public repositories
   - Per-repo: languages used, star count, fork count, last pushed date, README content
   - Commit history for the last 2 years: commit count per week
2. Build a GitHub Activity Profile:
   - `total_repos`, `active_repos` (pushed in last 12 months), `commit_frequency` (weekly average), `top_languages`, `longest_streak_days`, `last_active_date`
3. Timeline contradiction check:
   - If candidate claims "Python expert since 2021" but first Python file commit is from 2024 — flag as **TIMELINE CONTRADICTION** (high severity red flag)
   - Run this check for every language/skill mentioned with a year claim
4. Quality signals:
   - Repos with only README commits (no real code) = low quality signal
   - Repos with consistent, descriptive commit messages = positive signal
   - Forked repos with no original commits = not counted as original work

#### 3D — LinkedIn Analysis

1. Use Playwright to scrape the public LinkedIn profile (do not use LinkedIn API — it is unavailable):
   - Extract: headline, current position, education section, skills section, activity feed (recent posts, last 5)
   - Extract: approximate connection count tier (500+, 200-500, <200)
2. Cross-check LinkedIn education section with resume education section:
   - Institution name match (fuzzy match with threshold 0.85)
   - Degree name match
   - Year range match (within ±1 year tolerance)
   - Flag mismatches
3. Activity analysis:
   - Count posts in last 6 months
   - Check if posts mention skills or technologies claimed on resume (positive signal)
   - **FAIRNESS RULE**: Inactive LinkedIn (0 posts, low connections) ≠ fraud. Do NOT penalise for inactivity. Only penalise for contradictions.
4. Skills section cross-check:
   - If LinkedIn skills section exists and has overlapping skills with resume, treat as corroboration
   - If LinkedIn skills section directly contradicts resume (e.g. resume says Java but LinkedIn has no technical skills) — flag for review

#### 3E — Certificate Verification

For each uploaded certificate:
1. Extract certificate metadata: issuer name, issued date, credential ID (if any), candidate name on certificate
2. Check candidate name on certificate matches registered name (fuzzy match)
3. If credential URL is provided: scrape the URL and verify the certificate is still valid and matches the claimed details
4. Check issue date plausibility: a certificate issued before the candidate's stated learning period = flag
5. Widely-trusted issuers (Coursera, Google, AWS, Microsoft, NPTEL, IIT platforms) get automatic issuer trust boost

**Output**: `evidence_confidence_score`, per-skill evidence map, per-document cross-check results, github activity profile, linkedin cross-check results

---

### STAGE 4 — LAYER 4: SKILL CONFIDENCE (Adaptive AI Assessment)

**Weight: 20%**

For candidates who pass Stages 1–3 above a threshold (Trust Score so far > 40), trigger adaptive skill assessment.

1. **Select top 3 skills** from resume that are most relevant to the job description (using semantic similarity)
2. **For each skill, generate an assessment** using the LLM:
   - 2 MCQs (intermediate level for freshers, advanced for experienced)
   - 1 short coding challenge (for technical skills) OR 1 scenario-based question (for non-technical skills)
   - 1 debugging task (for programming skills)
3. The assessment is delivered to the candidate through a timed in-platform assessment UI (15 minutes total)
4. Candidate responses are evaluated by the LLM with a rubric:
   - MCQs: exact match scoring
   - Coding challenge: correctness + efficiency + code style
   - Scenario question: LLM rubric evaluating relevance, depth, structure
5. Skill assessment score per skill: 0–100
6. Overall Skill Confidence = weighted average of assessed skills

**Note**: If a candidate does not complete the assessment within 48 hours of trigger, mark skill confidence as "Not Assessed" — do not penalise, but note it in the report.

**Output**: `skill_confidence_score`, per-skill assessment results, assessment completion status

---

### STAGE 5 — LAYER 5: IDENTITY CONFIDENCE (Digital Twin Assembly)

**Weight: 15%**

1. Merge all verified data points into a unified candidate identity profile:
   - Verified name (consistent across all documents and platforms)
   - Verified institution and degree
   - Verified skills (with evidence type per skill)
   - Verified projects (with corroborating GitHub activity)
   - Verified certificates (with live URL checks)
   - Verified timelines (academic, project, certification — plotted chronologically)
2. Run a **Timeline Coherence Check**:
   - Plot all dated events on a timeline: enrollment, graduation, certificates, internships, projects, GitHub first commits, LinkedIn education dates
   - Flag any event that is temporally impossible (e.g. completing a 6-month course in 2 weeks, or graduating before enrolling)
3. Run a **Cross-Platform Name Consistency Check**:
   - Name on resume vs name on documents vs LinkedIn name vs GitHub username pattern
   - Flag significant mismatches
4. Compute **Identity Completeness Score**:
   - How much of the claimed identity is corroborated by at least one external source?
   - More corroborated points = higher identity confidence

**Output**: `identity_confidence_score`, timeline coherence result, digital twin profile JSON

---

### STAGE 6 — LAYER 6: TRUST INTELLIGENCE (Academic Trust Graph)

**Weight: 15%**

Using the Neo4j graph:

1. **Build the candidate subgraph**: all nodes (Candidate, Skills, Institutions, Certificates, Projects, Employers) and edges created from verified data
2. **Detect structural contradictions**:
   - Orphaned skill node (skill with no connecting evidence edge) = red flag
   - Disconnected institution node (institution with no corroborating web presence) = yellow flag
   - Temporal edge violation (certificate earned before claimed skill acquisition started) = red flag
3. **Detect skill inflation pattern**:
   - Compare the candidate's skill graph density to a benchmark graph for candidates at the same education level
   - Suspiciously high skill count relative to experience years = inflation signal
4. **Detect systemic fraud patterns**:
   - Check if the same document hash has been submitted by multiple candidates (shared/forged document)
   - Check if institutional email domain matches the claimed institution domain
5. **Compute final Graph Confidence Score** based on graph connectivity, contradiction count, and anomaly density

**Output**: `graph_confidence_score`, contradiction list, fraud pattern flags

---

### FINAL TRUST SCORE COMPUTATION

```
Trust Score = (
  document_confidence * 0.15 +
  content_confidence  * 0.15 +
  evidence_confidence * 0.20 +
  skill_confidence    * 0.20 +
  identity_confidence * 0.15 +
  graph_confidence    * 0.15
)
```

Apply the **Fairness Principle**:
- Missing data (no LinkedIn, no GitHub) → does NOT reduce the score. These fields are scored as "neutral" (50) not zero
- Contradictory data → DOES reduce the score. Conflicting timelines trigger automatic scrutiny
- A candidate with no LinkedIn but consistent documents and strong GitHub can still score > 85

---

### SELECTION / REJECTION REASON GENERATION

After the Trust Score is computed, call the LLM with a structured prompt to generate:

**For selected candidates (Trust Score ≥ threshold set by HR or system default 70)**:
Generate a 150–200 word personalised selection narrative covering:
- Which verified credentials stood out
- Which skills are backed by the strongest evidence
- Any unique signals (exceptional GitHub activity, rare certification, cross-domain project, etc.)
- Why this candidate is a strong match for the specific job role

**For rejected candidates**:
Generate a 100–150 word rejection report covering:
- Primary stage of failure (ATS / Document / Content / Evidence / Skill / Identity / Graph)
- Specific finding that caused rejection (e.g. "Claimed B.Tech degree from an institution that does not offer B.Tech", "Python listed as primary skill but no Python-related projects or repositories found", "Certificate issue date precedes claimed learning period by 18 months")
- Whether the issue is correctable (e.g. "Please upload current semester marksheet to complete verification") or disqualifying (e.g. "Degree mismatch with institution offerings is a hard disqualification")
- Tone must be constructive, not punitive

---

## UI/UX DESIGN SYSTEM

- **Primary colours**: Deep Navy `#0F172A`, Electric Blue `#3B82F6`, Slate Gray `#64748B`
- **Accent**: Emerald `#10B981` (verified/success), Amber `#F59E0B` (pending/flag), Rose `#F43F5E` (rejected/red flag)
- **Typography**: `Geist` for headings, `Inter` for body
- **Trust Score radar chart**: Use Recharts `RadarChart` with 6 axes (one per layer). Fill colour transitions from rose (low) through amber (mid) to emerald (high) based on score value
- **Application status pipeline**: A horizontal stepper component with 6 nodes, animated fill as stages complete
- **Card design**: Glassmorphism-style cards for Trust Score display; flat cards for data tables
- **Dark mode**: Full dark mode support using Tailwind's `dark:` variants
- **Responsive**: Mobile-first. All dashboards must be usable on a 375px screen.

---

## ENVIRONMENT VARIABLES

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/eduproof
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=yourpassword
REDIS_URL=redis://localhost:6379

# Storage
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET=eduproof-documents
AWS_REGION=ap-south-1

# AI
OPENAI_API_KEY=
# OR
ANTHROPIC_API_KEY=

# GitHub (optional, increases rate limit)
GITHUB_TOKEN=

# Auth
NEXTAUTH_SECRET=
NEXTAUTH_URL=http://localhost:3000
JWT_SECRET=

# App
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## FOLDER STRUCTURE

```
eduproof-ai/
├── frontend/                        # Next.js 14 App
│   ├── app/
│   │   ├── (public)/               # Landing, login, register
│   │   ├── candidate/              # Candidate-role pages
│   │   ├── hr/                     # HR-role pages
│   │   └── admin/                  # Admin-role pages
│   ├── components/
│   │   ├── ui/                     # shadcn/ui components
│   │   ├── trust-radar.tsx         # Trust Score radar chart
│   │   ├── pipeline-stepper.tsx    # Application status stepper
│   │   ├── candidate-card.tsx      # Candidate summary card for HR
│   │   └── verification-layer-card.tsx
│   ├── lib/
│   │   ├── api.ts                  # API client
│   │   └── auth.ts                 # NextAuth config
│   └── types/                      # TypeScript interfaces
│
├── backend/                         # FastAPI
│   ├── app/
│   │   ├── api/v1/                 # Route handlers
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── services/               # Business logic
│   │   └── core/                   # Config, security, deps
│   ├── verification/               # The entire pipeline lives here
│   │   ├── pipeline.py             # Orchestrator: runs all stages in order
│   │   ├── stage0_ats.py           # ATS scoring
│   │   ├── stage1_document.py      # Document confidence
│   │   ├── stage2_content.py       # Content confidence
│   │   ├── stage3_evidence.py      # Evidence confidence (academic, GitHub, LinkedIn, certs)
│   │   ├── stage3a_academic.py     # Academic record + institution scraper
│   │   ├── stage3b_skill_map.py    # Skill-to-evidence mapper
│   │   ├── stage3c_github.py       # GitHub analyser
│   │   ├── stage3d_linkedin.py     # LinkedIn scraper
│   │   ├── stage3e_certificate.py  # Certificate verifier
│   │   ├── stage4_skill.py         # Adaptive skill assessment generator
│   │   ├── stage5_identity.py      # Digital twin assembler
│   │   ├── stage6_graph.py         # Trust graph analysis (Neo4j)
│   │   ├── scorer.py               # Final weighted score computation
│   │   └── narrator.py             # LLM-based selection/rejection reason generator
│   ├── tasks/
│   │   └── verification_task.py    # Celery task wrapping the pipeline
│   └── alembic/                    # DB migrations
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## DOCKER COMPOSE

Define the following services:
- `frontend` — Next.js on port 3000
- `backend` — FastAPI on port 8000
- `postgres` — PostgreSQL 15
- `neo4j` — Neo4j 5 Community on ports 7474, 7687
- `redis` — Redis 7
- `celery_worker` — Celery worker running the verification pipeline
- `celery_flower` — Flower monitoring UI on port 5555

---

## SEED DATA

Create a seed script that inserts:
- 1 admin user
- 2 sample HR/organisation accounts with 3 job listings each
- 5 sample candidate accounts with realistic profiles (mix of strong, weak, and fraudulent profiles for demo purposes)
- 3 pre-completed verification reports (one high trust, one medium, one rejected for degree mismatch)

---

## KEY IMPLEMENTATION NOTES

1. **Institute scraper robustness**: The institution website scraper must handle timeouts gracefully. If a site is unreachable after 3 retries, mark as "Institution unverifiable — manual check required" and do NOT auto-reject the candidate. Penalise score lightly (−5 points) but do not disqualify.

2. **Fairness over speed**: Every rejection reason must be traceable to a specific data point. Never produce a vague "low trust score" rejection. The system must be explainable at every step.

3. **Rate limiting**: GitHub API requests must respect rate limits. Use token authentication to get 5000 requests/hour. Cache GitHub results for 24 hours per candidate.

4. **PDF extraction fallback**: If pdfplumber fails (scanned/image PDFs), fall back to pytesseract OCR. Flag OCR-extracted documents as lower confidence than natively digital PDFs.

5. **Async pipeline**: The verification pipeline should NEVER block the API. It runs as a Celery background task. The frontend polls `/verify/{applicationId}/status` every 10 seconds to show live progress. Use WebSockets (or Server-Sent Events) for a real-time progress bar if possible.

6. **LLM prompt design**: All LLM calls must use structured output (JSON mode). Never parse free-text LLM responses. Define a Pydantic schema for every LLM output and pass it as the response format.

7. **Graph contradiction detection**: The Neo4j queries must be parameterised — never build Cypher strings with f-strings (injection risk).

8. **Data privacy**: Documents stored in S3 must use server-side encryption. Pre-signed URLs must expire in 15 minutes. Candidates can delete their own documents. Deleted documents must be removed from S3 within 24 hours via a scheduled job.

9. **Skill assessment delivery**: The adaptive assessment UI must be a distraction-free, full-screen mode page with a countdown timer. Candidates cannot re-take an assessment for the same job application.

10. **Admin audit log**: Every manual override by an admin must be logged with timestamp, admin user ID, original score, new score, and justification note. This log is immutable.

---

## BUILD ORDER (RECOMMENDED FOR AGENT)

1. Set up monorepo structure, Docker Compose, environment config
2. Build PostgreSQL schema + Alembic migrations
3. Build FastAPI auth routes (register, login, JWT middleware)
4. Build candidate profile CRUD + document upload (S3)
5. Build job listing CRUD (HR)
6. Build application submission endpoint
7. Build frontend: auth pages + candidate dashboard skeleton + HR dashboard skeleton
8. Build Stage 0 (ATS scorer) — simplest stage, good for testing pipeline plumbing
9. Build Stage 3C (GitHub analyser) — self-contained, testable with real data
10. Build Stage 3A (Academic record + institution scraper)
11. Build Stages 1, 2, 3B, 3D, 3E
12. Build Stage 4 (Skill assessment) + frontend assessment UI
13. Build Stages 5 and 6 (Identity + Trust Graph)
14. Build scorer.py + narrator.py (final score + reason generation)
15. Wire Celery task to trigger on application submit
16. Build frontend: Trust Score radar chart + verification report pages
17. Build admin dashboard
18. Seed data + end-to-end test with demo profiles
19. Polish UI, add dark mode, mobile responsiveness
20. Write README with setup instructions

---

*This prompt defines the complete EduProof AI system. Build it in full. Do not simplify or omit any stage. Every stage of the verification pipeline, every role's dashboard, and every database table described above must be implemented.*