import { useEffect, useState } from "react";
import "./index.css";

const API = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");
const MEDIA_BASE = (import.meta.env.VITE_MEDIA_URL || API).replace(/\/$/, "");

// 🟢 اصلاح شد: هوشمندسازی تابع برای جلوگیری از تکرار پوشه media/media/
function resolveImageUrl(url) {
  if (!url) return null;
  if (/^https?:\/\//i.test(url)) return url;

  let cleanUrl = url;
  // اگر آدرس فایل از بک‌اند با media/ شروع شده و دامین اصلی هم خودش شامل media/ هست، تکرار اول را پاک کن
  if (cleanUrl.startsWith("media/") && MEDIA_BASE.endsWith("media/")) {
    cleanUrl = cleanUrl.replace("media/", "");
  }

  // تمیزکاری اسلش‌های ابتدا و انتها برای ساختن یک URL استاندارد
  const base = MEDIA_BASE.endsWith("/") ? MEDIA_BASE : `${MEDIA_BASE}/`;
  const path = cleanUrl.startsWith("/") ? cleanUrl.slice(1) : cleanUrl;

  return `${base}${path}`;
}

export default function App() {
  const [profile, setProfile] = useState(null);
  const [projects, setProjects] = useState([]);
  const [skills, setSkills] = useState([]);
  const [categories, setCategories] = useState([]);
  const [education, setEducation] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");
  const [contactStatus, setContactStatus] = useState("idle");

  useEffect(() => {
    Promise.all([
      fetchJson(`${API}/profile/`),
      fetchJson(`${API}/projects/`),
      fetchJson(`${API}/skills/`),
      fetchJson(`${API}/education/`),
      fetchJson(`${API}/categories/`),
    ])
      .then(([p, pr, s, e, cats]) => {
        setProfile(p);
        setProjects(sortProjects(pr));
        setSkills(sortSkills(s));
        setEducation(sortEducation(e));
        setCategories(cats);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="boot-screen">
        <pre className="boot-text">
{`$ initializing portfolio...
$ fetching /api/profile/      [ok]
$ fetching /api/projects/      ...
$ fetching /api/skills/        ...
$ fetching /api/education/     ...`}
        </pre>
      </div>
    );
  }

  if (error) {
    return (
      <div className="boot-screen">
        <pre className="boot-text boot-error">
{`$ initializing portfolio...
$ error: ${error}
$ check that the API server is running at
$ ${API}`}
        </pre>
      </div>
    );
  }

  const filteredProjects =
    filter === "all"
      ? projects
      : filter === "featured"
      ? projects.filter((p) => p.is_featured)
      : projects.filter((p) =>
          String(p.tech_list || p.tech_stack || "")
            .toLowerCase()
            .includes(filter)
        );

  const featuredProject = projects.find((p) => p.is_featured) || projects[0];

  return (
    <div className="page">
      <Nav profile={profile} />
      <main>
        <Hero profile={profile} featured={featuredProject} />
        <ProjectsSection
          projects={filteredProjects}
          allProjects={projects}
          filter={filter}
          setFilter={setFilter}
        />
        <SkillsSection skills={skills} categories={categories} />
        <EducationSection education={education} />
        <ContactSection status={contactStatus} setStatus={setContactStatus} profile={profile} />
      </main>
      <Footer profile={profile} />
    </div>
  );
}

/* ---------------- helpers ---------------- */

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${url} returned ${response.status}`);
  }
  return response.json();
}

function sortProjects(list) {
  return [...list].sort((a, b) => {
    if (a.is_featured !== b.is_featured) return a.is_featured ? -1 : 1;
    return new Date(b.created_at) - new Date(a.created_at);
  });
}

function sortSkills(list) {
  return [...list].sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
}

function sortEducation(list) {
  return [...list].sort((a, b) => {
    if (a.is_current !== b.is_current) return a.is_current ? -1 : 1;
    return (b.start_year ?? 0) - (a.start_year ?? 0);
  });
}

function groupSkills(skills) {
  const groups = {};
  for (const s of skills) {
    const catId = s.category?.id ?? "other";
    if (!groups[catId]) groups[catId] = [];
    groups[catId].push(s);
  }
  return groups;
}

/* ---------------- Nav ---------------- */

function Nav({ profile }) {
  const initials = (profile?.full_name || "?")
    .split(" ")
    .map((p) => p[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <header className="nav">
      <div className="nav-inner">
        <a href="#top" className="nav-mark">
          {profile?.avatar ? (
            <img
              className="nav-avatar"
              src={resolveImageUrl(profile.avatar)}
              alt={profile.full_name}
            />
          ) : (
            <span className="nav-cursor">{initials}</span>
          )}
          {profile?.full_name && <span className="nav-name">{profile.full_name}</span>}
        </a>
        <nav className="nav-links">
          <a href="#projects">projects</a>
          <a href="#skills">skills</a>
          <a href="#education">education</a>
          <a href="#contact">contact</a>
        </nav>
      </div>
    </header>
  );
}

/* ---------------- Hero ---------------- */

function Hero({ profile, featured }) {
  const lines = [
    { cmd: "whoami", out: profile?.full_name || "developer" },
    { cmd: "cat role.txt", out: profile?.title || "" },
    { cmd: "cat status.txt", out: profile?.bio || "Building things on the web." },
  ].filter((l) => l.out);

  return (
    <section id="top" className="hero">
      <div className="hero-grid">
        <div className="hero-text">
          <p className="eyebrow">portfolio.json</p>
          <h1 className="hero-title">{profile?.full_name || "Personal Portfolio"}</h1>
          {profile?.title && <p className="hero-role">{profile.title}</p>}
          <p className="hero-bio">{profile?.bio}</p>
          <div className="hero-actions">
            <a href="#projects" className="btn btn-primary">
              view projects
            </a>
            <a href="#contact" className="btn btn-ghost">
              get in touch
            </a>
            {profile?.resume_file && (
              <a
                href={resolveImageUrl(profile.resume_file)}
                target="_blank"
                rel="noreferrer"
                className="btn btn-ghost"
              >
                resume
              </a>
            )}
          </div>
          {(profile?.github_url || profile?.linkedin_url || profile?.email) && (
            <div className="hero-social">
              {profile?.github_url && (
                <a href={profile.github_url} target="_blank" rel="noreferrer">
                  github
                </a>
              )}
              {profile?.linkedin_url && (
                <a href={profile.linkedin_url} target="_blank" rel="noreferrer">
                  linkedin
                </a>
              )}
              {profile?.email && <a href={`mailto:${profile.email}`}>email</a>}
            </div>
          )}
        </div>

        <div className="terminal" aria-hidden="true">
          <div className="terminal-bar">
            <span className="dot dot-red" />
            <span className="dot dot-amber" />
            <span className="dot dot-green" />
            <span className="terminal-title">session — zsh</span>
          </div>
          <div className="terminal-body">
            {lines.map((l, i) => (
              <div className="terminal-line" key={i}>
                <span className="prompt">$</span> {l.cmd}
                <div className="terminal-out">{l.out}</div>
              </div>
            ))}
            {featured && (
              <div className="terminal-line">
                <span className="prompt">$</span> cat featured_project.md
                <div className="terminal-out">
                  <strong>{featured.title}</strong>
                  <br />
                  {truncate(featured.description, 110)}
                </div>
              </div>
            )}
            <div className="terminal-line">
              <span className="prompt">$</span>{" "}
              <span className="cursor-blink">▮</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function truncate(text, max) {
  if (!text) return "";
  return text.length > max ? text.slice(0, max).trim() + "…" : text;
}

/* ---------------- Projects ---------------- */

function ProjectsSection({ projects, allProjects, filter, setFilter }) {
  const techs = new Set();
  allProjects.forEach((p) =>
    String(p.tech_list || p.tech_stack || "")
      .split(",")
      .map((t) => t.trim().toLowerCase())
      .filter(Boolean)
      .forEach((t) => techs.add(t))
  );

  const filters = ["all", "featured", ...Array.from(techs).slice(0, 6)];

  return (
    <section id="projects" className="section">
      <SectionHeading index="01" title="Projects" />

      <div className="filter-row">
        {filters.map((f) => (
          <button
            key={f}
            className={`filter-chip ${filter === f ? "is-active" : ""}`}
            onClick={() => setFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      {projects.length === 0 ? (
        <p className="empty-state">No projects match this filter yet.</p>
      ) : (
        <div className="project-grid">
          {projects.map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </div>
      )}
    </section>
  );
}

function ProjectCard({ project }) {
  const tags = (Array.isArray(project.tech_list)
    ? project.tech_list
    : String(project.tech_stack || "").split(","))
    .map((t) => t.trim())
    .filter(Boolean);

  return (
    <article className={`project-card ${project.is_featured ? "is-featured" : ""}`}>
      {project.image && (
        <div className="project-image">
          <img src={resolveImageUrl(project.image)} alt={project.title} loading="lazy" />
        </div>
      )}
      <div className="project-body">
        <div className="project-header">
          <h3>{project.title}</h3>
          {project.is_featured && <span className="badge badge-featured">featured</span>}
        </div>
        <p className="project-desc">{project.description}</p>

        {tags.length > 0 && (
          <div className="tag-row">
            {tags.map((tag) => (
              <span className="tag" key={tag}>
                {tag}
              </span>
            ))}
          </div>
        )}

        <div className="project-footer">
          {project.created_at && (
            <span className="project-date">{formatDate(project.created_at)}</span>
          )}
          <div className="project-links">
            {project.live_url && (
              <a href={project.live_url} target="_blank" rel="noreferrer" className="link-btn">
                live ↗
              </a>
            )}
            {project.github_url && (
              <a href={project.github_url} target="_blank" rel="noreferrer" className="link-btn">
                code ↗
              </a>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}

function formatDate(dateStr) {
  try {
    return new Date(dateStr).toLocaleDateString(undefined, {
      year: "numeric",
      month: "short",
    });
  } catch {
    return dateStr;
  }
}

/* ---------------- Skills ---------------- */

function SkillsSection({ skills, categories }) {
  const grouped = groupSkills(skills);
  const activeCats = categories.filter((cat) => grouped[cat.id]?.length);
  const uncategorized = grouped["other"] || [];

  return (
    <section id="skills" className="section">
      <SectionHeading index="02" title="Skills" />

      {skills.length === 0 ? (
        <p className="empty-state">Skills coming soon.</p>
      ) : (
        <div className="skills-grid">
          {activeCats.map((cat) => (
            <div className="skill-group" key={cat.id}>
              <h3 className="skill-group-title">{cat.name}</h3>
              <div className="skill-list">
                {grouped[cat.id].map((s) => (
                  <div className="skill-row" key={s.id}>
                    <div className="skill-row-top">
                      <span className="skill-name">{s.name}</span>
                      <span className="skill-level">{s.level}%</span>
                    </div>
                    <div className="skill-bar">
                      <div
                        className="skill-bar-fill"
                        style={{ width: `${Math.min(Math.max(s.level, 0), 100)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {uncategorized.length > 0 && (
            <div className="skill-group" key="other">
              <h3 className="skill-group-title">other</h3>
              <div className="skill-list">
                {uncategorized.map((s) => (
                  <div className="skill-row" key={s.id}>
                    <div className="skill-row-top">
                      <span className="skill-name">{s.name}</span>
                      <span className="skill-level">{s.level}%</span>
                    </div>
                    <div className="skill-bar">
                      <div
                        className="skill-bar-fill"
                        style={{ width: `${Math.min(Math.max(s.level, 0), 100)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

/* ---------------- Education ---------------- */

function EducationSection({ education }) {
  return (
    <section id="education" className="section">
      <SectionHeading index="03" title="Education" />

      {education.length === 0 ? (
        <p className="empty-state">Education history coming soon.</p>
      ) : (
        <div className="timeline">
          {education.map((e) => (
            <div className="timeline-item" key={e.id}>
              <div className="timeline-marker">
                <span className={`timeline-dot ${e.is_current ? "is-current" : ""}`} />
              </div>
              <div className="timeline-content">
                <div className="timeline-header">
                  <h3>{e.university}</h3>
                  {e.is_current && <span className="badge badge-current">current</span>}
                </div>
                <p className="timeline-degree">
                  {e.degree} · {e.field}
                </p>
                <div className="timeline-meta">
                  <span>
                    {e.start_year}
                    {e.end_year ? ` — ${e.end_year}` : e.is_current ? " — present" : ""}
                  </span>
                  {e.gpa && <span className="timeline-gpa">GPA {e.gpa}</span>}
                </div>
                {e.description && <p className="timeline-desc">{e.description}</p>}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

/* ---------------- Contact ---------------- */

function ContactSection({ status, setStatus, profile }) {
  const [form, setForm] = useState({ name: "", email: "", message: "" });

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("sending");
    try {
      const res = await fetch(`${API}/contact/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("request failed");
      setStatus("sent");
      setForm({ name: "", email: "", message: "" });
    } catch {
      setStatus("error");
    }
  }

  return (
    <section id="contact" className="section">
      <SectionHeading index="04" title="Contact" />

      <div className="contact-grid">
        <div>
          <p className="contact-intro">
            Have a project in mind or just want to say hi? Send a message below.
          </p>
          {profile?.email && (
            <p className="contact-direct">
              or reach me directly at{" "}
              <a href={`mailto:${profile.email}`}>{profile.email}</a>
            </p>
          )}
        </div>

        <form className="contact-form" onSubmit={handleSubmit}>
          <label className="field">
            <span>Name</span>
            <input
              type="text"
              required
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />
          </label>
          <label className="field">
            <span>Email</span>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />
          </label>
          <label className="field">
            <span>Message</span>
            <textarea
              required
              rows={4}
              value={form.message}
              onChange={(e) => setForm({ ...form, message: e.target.value })}
            />
          </label>

          <button type="submit" className="btn btn-primary" disabled={status === "sending"}>
            {status === "sending" ? "sending..." : "send message"}
          </button>

          {status === "sent" && <p className="form-status form-success">Message sent.</p>}
          {status === "error" && (
            <p className="form-status form-error">Something went wrong. Try again.</p>
          )}
        </form>
      </div>
    </section>
  );
}

/* ---------------- Shared ---------------- */

function SectionHeading({ index, title }) {
  return (
    <div className="section-heading">
      <span className="section-index">{index}</span>
      <h2>{title}</h2>
    </div>
  );
}

function Footer({ profile }) {
  return (
    <footer className="footer">
      <p>© {new Date().getFullYear()} {profile?.full_name || "Personal Portfolio"}</p>
    </footer>
  );
}