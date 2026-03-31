"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import "./landing.css";

type Lang = "en" | "zh";

export default function LandingPage() {
  const [lang, setLang] = useState<Lang>("en");
  const containerRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);
  const counterRef = useRef<HTMLSpanElement>(null);

  const zh = lang === "zh";

  // Detect user locale on mount
  useEffect(() => {
    const stored = (() => { try { return localStorage.getItem("aha-lang"); } catch { return null; } })();
    const auto = (navigator.language || "").startsWith("zh") ? "zh" : "en";
    setLang((stored as Lang) || auto);
  }, []);

  // Persist lang
  useEffect(() => {
    try { localStorage.setItem("aha-lang", lang); } catch { /* ignore */ }
  }, [lang]);

  // Presentation controller
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const slides = Array.from(container.querySelectorAll<HTMLElement>(".slide"));
    const dots = Array.from(container.querySelectorAll<HTMLButtonElement>(".nav-dot"));
    const progressBar = progressRef.current;
    const curSlideEl = counterRef.current;
    const total = slides.length;
    let current = 0;

    function goTo(idx: number) {
      if (idx < 0 || idx >= total) return;
      current = idx;
      slides[idx].scrollIntoView({ behavior: "smooth" });
      update();
    }

    function update() {
      const pct = total <= 1 ? 100 : (current / (total - 1)) * 100;
      if (progressBar) progressBar.style.width = pct + "%";
      if (curSlideEl) curSlideEl.textContent = String(current + 1).padStart(2, "0");
      dots.forEach((d, i) => d.classList.toggle("active", i === current));
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            const idx = slides.indexOf(entry.target as HTMLElement);
            if (idx !== -1) { current = idx; update(); }
          }
        });
      },
      { root: container, threshold: 0.55 }
    );
    slides.forEach((s) => observer.observe(s));

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowDown" || e.key === "ArrowRight" || e.key === " ") {
        e.preventDefault(); goTo(current + 1);
      } else if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
        e.preventDefault(); goTo(current - 1);
      } else if (e.key === "Home") {
        e.preventDefault(); goTo(0);
      } else if (e.key === "End") {
        e.preventDefault(); goTo(total - 1);
      }
    };
    document.addEventListener("keydown", onKeyDown);

    dots.forEach((d, i) => d.addEventListener("click", () => goTo(i)));

    let wheelTimer: ReturnType<typeof setTimeout>;
    const onWheel = (e: WheelEvent) => {
      clearTimeout(wheelTimer);
      wheelTimer = setTimeout(() => {
        if (e.deltaY > 30) goTo(current + 1);
        else if (e.deltaY < -30) goTo(current - 1);
      }, 50);
    };
    container.addEventListener("wheel", onWheel, { passive: true });

    let touchY = 0;
    const onTouchStart = (e: TouchEvent) => { touchY = e.touches[0].clientY; };
    const onTouchEnd = (e: TouchEvent) => {
      const diff = touchY - e.changedTouches[0].clientY;
      if (Math.abs(diff) > 50) goTo(diff > 0 ? current + 1 : current - 1);
    };
    container.addEventListener("touchstart", onTouchStart, { passive: true });
    container.addEventListener("touchend", onTouchEnd, { passive: true });

    update();

    return () => {
      observer.disconnect();
      document.removeEventListener("keydown", onKeyDown);
      container.removeEventListener("wheel", onWheel);
      container.removeEventListener("touchstart", onTouchStart);
      container.removeEventListener("touchend", onTouchEnd);
    };
  }, []);

  return (
    <div ref={containerRef} className={`aha-landing${zh ? " lang-zh" : ""}`}>

      {/* ── Progress bar ── */}
      <div className="progress-bar" ref={progressRef} />

      {/* ── Slide counter ── */}
      <div className="slide-counter"><span ref={counterRef}>01</span> / 12</div>

      {/* ── Nav dots ── */}
      <nav className="nav-dots" aria-label="Slide navigation">
        {Array.from({ length: 12 }, (_, i) => (
          <button
            key={i}
            type="button"
            className={`nav-dot${i === 0 ? " active" : ""}`}
            aria-label={`Slide ${i + 1}`}
          />
        ))}
      </nav>

      {/* ── Language toggle ── */}
      <div className="lang-toggle" aria-label="Language / 语言">
        <button type="button" className={`lang-btn${!zh ? " active" : ""}`} onClick={() => setLang("en")} aria-label="Switch to English">EN</button>
        <span className="lang-sep" aria-hidden="true">|</span>
        <button type="button" className={`lang-btn${zh ? " active" : ""}`} onClick={() => setLang("zh")} aria-label="切换到中文">中</button>
      </div>

      {/* ══════════════════════════════════════════
          SLIDE 01 — HERO
      ══════════════════════════════════════════ */}
      <section className="slide" id="s1">
        <div className="s1-split">
          <div className="s1-text">
            <p className="hero-eyebrow reveal d1">AI Hero Academy · 2026</p>
            <h1 className="reveal d2">
              {zh ? <>从AI小白<br />到<em>AI超能职场人。</em><br />7天蜕变。</> : <>From AI-curious<br />to <em>AI-supercharged.</em><br />In 7 days.</>}
            </h1>
            <p className="hero-sub reveal d3">
              {zh
                ? "为每一位职场人打造的AI转型计划——不限职位与行业。场景化实战练习，真实AI教练，专属工具包永久保留。"
                : "Personal AI transformation for every professional — regardless of role or industry. Scenario-based practice, real coaching, a toolkit you keep."}
            </p>
            <div className="hero-metrics reveal d4">
              {[
                { val: "7",              lbl: zh ? "天"      : "Days",         red: false },
                { val: "6",              lbl: zh ? "技能支柱" : "Skill Pillars", red: false },
                { val: "90",             lbl: zh ? "分钟/天" : "Min / Day",     red: false },
                { val: zh ? "免费" : "Free",  lbl: zh ? "永久免费" : "Forever",  red: true  },
                { val: zh ? "双语" : "EN+ZH", lbl: zh ? "中英双语" : "Bilingual", red: false },
              ].map((m) => (
                <div key={m.lbl} className="metric-item">
                  <div className={`metric-val${m.red ? " red" : ""}`}>{m.val}</div>
                  <div className="metric-lbl">{m.lbl}</div>
                </div>
              ))}
            </div>
            <div className="reveal d5">
              <Link href="/login" className="cta-btn">
                {zh ? "开始第一天" : "Start Day 1"} <em className="arrow">→</em>
              </Link>
            </div>
          </div>
          <div className="s1-photo reveal-scale d2">
            <div className="s1-accent" />
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&q=85&auto=format&fit=crop&crop=faces,center"
              alt="Professional using AI tools at work"
              loading="eager"
            />
          </div>
        </div>
        <div className="bottom-rule" />
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 02 — THE PROBLEM
      ══════════════════════════════════════════ */}
      <section className="slide" id="s2">
        <div className="slide-num">02</div>
        <div className="slide-content">
          <div className="two-col">
            <div>
              <p className="label reveal-left d1">{zh ? "问题所在" : "The Problem"}</p>
              <div className="rule-accent reveal d2" />
              <h2 className="reveal d3">
                {zh ? <>AI培训满地都是，<br />却没有一个真正有效。</> : <>AI training is everywhere.<br />None of it sticks.</>}
              </h2>
              <div style={{ marginTop: "clamp(0.6rem, 2vh, 1.2rem)" }} className="reveal d4">
                <p>{zh
                  ? "视频课让学习者被动接受。证书毫无意义。通用提示词在真实工作中根本用不上。"
                  : "Video lectures leave learners passive. Certificates prove nothing. Generic prompts don't survive contact with real work."}</p>
              </div>
              <div style={{ marginTop: "clamp(0.5rem, 1.5vh, 1rem)" }} className="reveal d5">
                <p>{zh
                  ? <>差距不在于知识——而在于在压力下实战，需要一个<strong>了解你工作场景的AI教练。</strong></>
                  : <>The gap isn&apos;t <em>knowledge</em> — it&apos;s <strong>practice under pressure, with a coach who knows your context.</strong></>}</p>
              </div>
            </div>
            <div className="reveal-scale d3">
              <table className="compare-table">
                <thead>
                  <tr>
                    <th>{zh ? "其他平台" : "Other platforms"}</th>
                    <th className="red">AI Hero Academy</th>
                  </tr>
                </thead>
                <tbody>
                  {([
                    [zh ? "看视频"          : "Watch videos",         zh ? "AI教练陪练"              : "Practice with AI coach"],
                    [zh ? "通用内容"         : "Generic content",      zh ? "你的职位，你的行业"        : "Your role, your industry"],
                    [zh ? "一张证书"         : "A certificate",        zh ? "你亲手构建的专属工具包"    : "A toolkit you built and own"],
                    [zh ? "仅英语"          : "EN only",              zh ? "中英双语，从第一天起"      : "EN + ZH from day one"],
                    [zh ? "免费增值→付费墙"  : "Freemium → paywall",   zh ? "永久免费。"               : "Free. Always."],
                  ] as [string, string][]).map(([bad, good], i) => (
                    <tr key={i}>
                      <td>{bad}</td>
                      <td><span className="check">✦</span>{good}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 03 — 7-DAY ARC
      ══════════════════════════════════════════ */}
      <section className="slide" id="s3">
        <div className="slide-content" style={{ paddingTop: "calc(var(--pad-x) * 0.7)", paddingBottom: "calc(var(--pad-x) * 0.7)" }}>
          <p className="label reveal-left d1">{zh ? "学习模式" : "Learning Model"}</p>
          <h2 className="reveal d2">{zh ? "7天蜕变旅程" : "The 7-Day Transformation Arc"}</h2>
          <div className="arc-grid reveal d3">
            {([
              { day: zh ? "第0天" : "Day 0", title: zh ? "入门与诊断"            : "Onboarding & Diagnostic",          fw: zh ? "差距图谱" : "Gap Map",    cls: "day0"     },
              { day: zh ? "第1天" : "Day 1", title: zh ? "AI概念基础"            : "AI Conceptual Foundation",         fw: "MAPS",                         cls: ""         },
              { day: zh ? "第2天" : "Day 2", title: zh ? "提示词与上下文工程"    : "Prompting & Context Engineering",  fw: "CRAF",                         cls: ""         },
              { day: zh ? "第3天" : "Day 3", title: zh ? "AI工具熟练度"          : "AI Tool Fluency",                  fw: "CAST",                         cls: ""         },
              { day: zh ? "第4天" : "Day 4", title: zh ? "AI配置与控制"          : "Configuration & Control",          fw: "BRIEF",                        cls: ""         },
              { day: zh ? "第5天" : "Day 5", title: zh ? "多AI工作流设计"        : "Multi-AI Workflow Design",         fw: "Workflow",                     cls: ""         },
              { day: zh ? "第6天" : "Day 6", title: zh ? "智能体系统设计"        : "Agentic System Design",            fw: "CREW",                         cls: ""         },
              { day: zh ? "第7天" : "Day 7", title: zh ? "综合挑战"              : "Capstone Challenge",               fw: zh ? "证书" : "Credential",     cls: "capstone" },
            ] as { day: string; title: string; fw: string; cls: string }[]).map((cell) => (
              <div key={cell.day} className={`arc-cell${cell.cls ? " " + cell.cls : ""}`}>
                <div className="arc-day-n">{cell.day}</div>
                <div className="arc-title">{cell.title}</div>
                <span className="arc-fw">{cell.fw}</span>
              </div>
            ))}
          </div>
          <div className="daily-row reveal d4">
            {([
              { icon: "ph ph-book-open",     t: zh ? "精读" : "Reading",  min: zh ? "20分钟" : "20 min", d: zh ? "概念 · 案例 · 反例"        : "Concept · Example · Anti-pattern"       },
              { icon: "ph ph-robot",         t: zh ? "实战" : "Practice", min: zh ? "40分钟" : "40 min", d: zh ? "4个任务 + 实时AI教练"       : "4 tasks + live AI coaching"              },
              { icon: "ph ph-pencil-simple", t: zh ? "测验" : "Quiz",     min: zh ? "15分钟" : "15 min", d: zh ? "≥2.5/4分解锁下一天"        : "Pass ≥ 2.5/4 to unlock next day"        },
              { icon: "ph ph-wrench",        t: zh ? "构建" : "Build",    min: zh ? "15分钟" : "15 min", d: zh ? "1件永属于你的成果"          : "1 artifact you own forever"              },
            ] as { icon: string; t: string; min: string; d: string }[]).map((b) => (
              <div key={b.t} className="daily-block">
                <div className="daily-t"><i className={b.icon} /> {b.t}</div>
                <div className="daily-min">{b.min}</div>
                <div className="daily-d">{b.d}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 04 — 6 PILLARS + ARTIFACTS
      ══════════════════════════════════════════ */}
      <section className="slide" id="s4">
        <div className="slide-content" style={{ paddingTop: "calc(var(--pad-x) * 0.7)", paddingBottom: "calc(var(--pad-x) * 0.7)" }}>
          <p className="label reveal-left d1">{zh ? "核心知识产权 — 知识体系" : "Core IP — Knowledge Model"}</p>
          <h2 className="reveal d2">{zh ? "六大支柱。一名完整的AI职场专家。" : "Six pillars. One complete AI professional."}</h2>
          <div className="pillars-grid">
            {([
              { day: zh ? "第1天" : "Day 1", tag: "MAPS",     tagCls: "tag",      revCls: "d3",
                name: zh ? "AI概念基础"       : "AI Conceptual Foundation",
                desc: zh ? "LLM的真实工作原理。5种幻觉模式。模型选择与使用规范。" : "How LLMs actually work. The 5 hallucination patterns. Model selection. Governance.",
                art:  zh ? "AI工具选择清单"   : "Personal AI tool selection checklist" },
              { day: zh ? "第2天" : "Day 2", tag: "CRAF",     tagCls: "tag",      revCls: "d4",
                name: zh ? "提示词与上下文工程" : "Prompting & Context Engineering",
                desc: zh ? "上下文·角色·行动·格式。从简单请求到结构化提示词。" : "Context · Role · Action · Format. From shallow requests to structured prompts.",
                art:  zh ? "可复用提示词模板" : "Reusable prompt template for your job" },
              { day: zh ? "第3天" : "Day 3", tag: "CAST",     tagCls: "tag",      revCls: "d5",
                name: zh ? "AI工具熟练度"     : "AI Tool Fluency",
                desc: zh ? "能力·访问·来源目标·权衡取舍。掌握2026年AI工具全景。" : "Capability · Access · Source-to-destination · Tradeoff. Navigate the 2026 landscape.",
                art:  zh ? "个人AI工具决策框架" : "Personal AI tool decision framework" },
              { day: zh ? "第4天" : "Day 4", tag: "BRIEF",    tagCls: "tag",      revCls: "d4",
                name: zh ? "AI配置与控制"     : "Configuration & Control",
                desc: zh ? "系统提示词、温度参数、JSON模式——让AI稳定地为你服务。" : "System prompts, temperature, JSON schemas — configure AI to serve you reliably.",
                art:  zh ? "今天就能部署的系统提示词" : "A system prompt you deploy today" },
              { day: zh ? "第5天" : "Day 5", tag: "Workflow", tagCls: "tag-dark", revCls: "d5",
                name: zh ? "多AI工作流设计"   : "Multi-AI Workflow Design",
                desc: zh ? "人工统筹多AI工具完成多步骤流程。交接节点。人工检查点。" : "Human orchestrates AI tools across a multi-step pipeline. Handoffs. Human checkpoints.",
                art:  zh ? "3步AI工作流设计" : "3-step AI workflow for a real task you do" },
              { day: zh ? "第6天" : "Day 6", tag: "CREW",     tagCls: "tag",      revCls: "d6",
                name: zh ? "智能体系统设计"   : "Agentic System Design",
                desc: zh ? "组件·角色·边界情况·流程图。AI统筹AI。设计故障模式。" : "Components · Roles · Edge cases · Workflow map. AI orchestrates AI. Design the failure modes.",
                art:  zh ? "自动化智能体工作流设计" : "Agent workflow design for automation" },
            ] as { day: string; tag: string; tagCls: string; revCls: string; name: string; desc: string; art: string }[]).map((p) => (
              <div key={p.day} className={`pillar-card reveal ${p.revCls}`}>
                <div className="pillar-top">
                  <span className="pillar-day-n">{p.day}</span>
                  <span className={p.tagCls}>{p.tag}</span>
                </div>
                <div className="pillar-name">{p.name}</div>
                <div className="pillar-desc">{p.desc}</div>
                <div className="pillar-artifact">{p.art}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 05 — PACE COACH
      ══════════════════════════════════════════ */}
      <section className="slide" id="s5">
        <div className="slide-content" style={{ paddingTop: "calc(var(--pad-x) * 0.7)", paddingBottom: "calc(var(--pad-x) * 0.7)" }}>
          <p className="label reveal-left d1">{zh ? "核心知识产权 — AI教练" : "Core IP — AI Coach"}</p>
          <h2 className="reveal d2">{zh ? "不是聊天机器人。是教练。" : "Not a chatbot. A coach."}</h2>
          <div className="two-col" style={{ marginTop: "clamp(0.5rem, 1.5vh, 1rem)" }}>
            <div>
              <div className="pace-grid">
                {([
                  { letter: "P", d: "d3", h: zh ? "目的"  : "Purpose", p: zh ? "提问前先明确学习目标。没有目的，不出题。" : "Declare the learning objective before generating a question. No question without a purpose." },
                  { letter: "A", d: "d4", h: zh ? "评估"  : "Assess",  p: zh ? "同时读取认知信号（理解了什么）和情绪信号（感受如何）。" : "Read both the intellectual signal (what they understood) and the emotional signal (how they feel)." },
                  { letter: "C", d: "d5", h: zh ? "选择"  : "Choose",  p: zh ? <>基于评估选择教练动作——<strong>挑战 · 澄清 · 庆祝 · 支持</strong>。</> : <>Select the right coaching move — <strong>Challenge · Clarify · Celebrate · Support</strong> — based on the assessment.</> },
                  { letter: "E", d: "d6", h: zh ? "退出"  : "Exit",    p: zh ? "目标达成即刻收尾。不问多余的问题。不拖延。" : "Close the task the moment the objective is met. Never ask an unnecessary question. Never linger." },
                ] as { letter: string; d: string; h: string; p: React.ReactNode }[]).map((row) => (
                  <div key={row.letter} className={`pace-row reveal ${row.d}`}>
                    <div className="pace-letter">{row.letter}</div>
                    <div className="pace-body">
                      <h3>{row.h}</h3>
                      <p>{row.p}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="reveal-scale d3">
              <div className="q-budget-box">
                <div className="q-budget-title">{zh ? "3问上限——不可突破" : "3-Question Budget — Hard Ceiling"}</div>
                <div className="q-row"><div className="q-badge">1</div>{zh ? "开放式探问 — 引出当前思路（必问）" : "Open probe — surface current thinking (always)"}</div>
                <div className="q-row"><div className="q-badge">2</div>{zh ? "自适应 — 浅则挑战，好则肯定" : "Adaptive — challenge if shallow / affirm if good"}</div>
                <div className="q-row"><div className="q-badge">3</div>{zh ? "综合总结 — 巩固并衔接成果构建" : "Synthesis — consolidate + bridge to build artifact"}</div>
                <div className="q-row"><div className="q-badge blocked">4</div>{zh ? "已封锁。问题额度耗尽→直接给出洞见。" : "Blocked. Budget exhausted → give insight directly."}</div>
              </div>
              <div style={{ marginTop: "clamp(0.6rem, 1.5vh, 1rem)" }}>
                <div style={{ fontFamily: "var(--font-disp)", fontSize: "var(--small-size)", fontWeight: 700, letterSpacing: "0.1em", textTransform: "uppercase" as const, color: "var(--ink-3)", marginBottom: "0.4em" }}>
                  {zh ? "情绪识别 — 5种模式" : "Emotional Detection — 5 Patterns"}
                </div>
                <div className="emotion-grid">
                  {([
                    [zh ? "简短/敷衍"  : "Short / dismissive", zh ? "无压力重新引导"         : "Reframe without pressure"],
                    [zh ? "沮丧"       : "Frustrated",          zh ? "停问。直接给出洞见。"   : "Stop. Give insight directly."],
                    [zh ? "过于自信"   : "Overconfident",       zh ? "温和挑战：引导深入"     : "Gentle challenge: push deeper"],
                    [zh ? "真正洞见"   : "Genuine insight",     zh ? "庆祝+收尾。不再追问。" : "Celebrate + close. No more Qs."],
                  ] as [string, string][]).map(([strong, rest]) => (
                    <div key={strong} className="emotion-cell"><strong>{strong}</strong>{rest}</div>
                  ))}
                </div>
                <div className="emotion-cell" style={{ marginTop: "0.35em" }}>
                  <strong style={{ display: "block", fontWeight: 700, color: "var(--ink)" }}>{zh ? "困惑/迷失" : "Confused / lost"}</strong>
                  {zh ? "简化并结合工作场景重新引导" : "Simplify + ground in their work context"}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 06 — DATA FLYWHEEL
      ══════════════════════════════════════════ */}
      <section className="slide" id="s6">
        <div className="s6-bg" aria-hidden="true" />
        <div className="slide-content">
          <div className="flywheel-wrap">
            <div className="fw-copy">
              <p className="label reveal-left d1">{zh ? "可防御的护城河" : "Defensible Moat"}</p>
              <div className="rule-accent reveal d2" />
              <h2 className="reveal d3">
                {zh ? <>随每位学员<br />不断复利增长的<br />数据飞轮。</> : <>The data flywheel<br />that compounds<br />with every learner.</>}
              </h2>
              <p className="reveal d4" style={{ marginTop: "clamp(0.6rem, 1.5vh, 1rem)", fontSize: "clamp(0.7rem, 1.2vw, 0.9rem)" }}>
                {zh
                  ? "每次教练辅导都会生成学员模型：提取优势、识别差距、记录偏好框架。该模型让下一次辅导更智能——对个人和整体均如此。"
                  : "Every coaching session generates a learner model: strengths extracted, gaps identified, preferred framing logged. That model makes the next session smarter — for that learner and across the collective."}
              </p>
              <div className="moat-list reveal d5">
                {(zh ? [
                  "职位×行业辅导模式",
                  "每位用户的个性化学员模型",
                  "7天旅程上下文连续性",
                  "每次辅导后自动触发综合智能体",
                ] : [
                  "Role × industry coaching patterns",
                  "Individual learner model per user",
                  "7-day arc context continuity",
                  "Synthesis agent fires after every session",
                ]).map((item) => (
                  <div key={item} className="moat-item"><div className="moat-dot" />{item}</div>
                ))}
              </div>
            </div>
            <div className="fw-diagram reveal-scale d3">
              <div className="fw-ring" />
              <div className="fw-node fw-n"><div className="fw-icon"><i className="ph ph-books" /></div>{zh ? <>学员<br />完成</> : <>Learner<br />completes</>}</div>
              <div className="fw-node fw-e"><div className="fw-icon"><i className="ph ph-lightning" /></div>{zh ? <>综合<br />智能体</> : <>Synthesis<br />agent</>}</div>
              <div className="fw-node fw-s"><div className="fw-icon"><i className="ph ph-graph" /></div>{zh ? <>学员模型<br />更新</> : <>Learner<br />model updated</>}</div>
              <div className="fw-node fw-w"><div className="fw-icon"><i className="ph ph-robot" /></div>{zh ? <>教练<br />更智能</> : <>Coach<br />smarter</>}</div>
              <div className="fw-center">{zh ? <>数据<br />飞轮</> : <>Data<br />Flywheel</>}</div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 07 — CREDENTIAL
      ══════════════════════════════════════════ */}
      <section className="slide" id="s7">
        <div className="slide-content">
          <div className="two-col">
            <div className="reveal-scale d2">
              <div className="cred-card">
                <div className="cred-badge-circle"><i className="ph ph-trophy" /></div>
                <div className="cred-title">{zh ? "AI超能中级认证" : "AI-Supercharged Intermediate"}</div>
                <div className="cred-issuer">{zh ? "由AI Hero Academy颁发 · 永久有效" : "Issued by AI Hero Academy · Valid indefinitely"}</div>
                <div className="cred-tags">
                  {["MAPS", "CRAF", "CAST", "BRIEF", "Workflow", "CREW"].map((t) => <span key={t} className="cred-tag">{t}</span>)}
                  <span className="cred-tag">{zh ? "第7天综合挑战 ✓" : "Day 7 Capstone ✓"}</span>
                </div>
                <div className="cred-assets">
                  <div className="cred-asset"><div className="cred-asset-icon"><i className="ph ph-medal" /></div>{zh ? "Open Badge 3.0 — 机器可验证" : "Open Badge 3.0 — machine-verifiable"}</div>
                  <div className="cred-asset"><div className="cred-asset-icon"><i className="ph ph-file-text" /></div>{zh ? "PDF证书含支柱详情" : "PDF certificate with pillar breakdown"}</div>
                  <div className="cred-asset"><div className="cred-asset-icon"><i className="ph ph-linkedin-logo" /></div>{zh ? "LinkedIn一键添加" : "LinkedIn one-click add"}</div>
                  <div className="cred-asset"><div className="cred-asset-icon"><i className="ph ph-device-mobile" /></div>{zh ? "社交分享卡 — LinkedIn · 微信" : "Social share card — LinkedIn · WeChat"}</div>
                </div>
              </div>
            </div>
            <div>
              <p className="label reveal-left d1">{zh ? "证书认证" : "Credential"}</p>
              <div className="rule-accent reveal d2" />
              <h2 className="reveal d3">
                {zh ? <>值得分享的证书。<br />值得珍藏的工具包。</> : <>A credential worth sharing.<br />A toolkit worth keeping.</>}
              </h2>
              <div className="cred-features" style={{ marginTop: "clamp(0.75rem, 2vh, 1.5rem)" }}>
                <div className="cred-feature hi reveal d4">
                  <h3>Open Badge 3.0</h3>
                  <p>{zh ? "机器可验证。适用于LinkedIn、邮件签名、简历。与Google、Coursera、Credly相同标准。" : "Machine-verifiable. Works in LinkedIn, email signatures, resumes. Same standard as Google, Coursera, Credly."}</p>
                </div>
                <div className="cred-feature reveal d5">
                  <h3>{zh ? "内置病毒传播机制" : "Built-in viral loop"}</h3>
                  <p>{zh ? "每张证书都会生成可分享的社交卡片。每次分享即一次口碑推荐——零广告费用。" : "Every issued credential generates a shareable social card. Each share is a word-of-mouth referral — zero ad spend."}</p>
                </div>
                <div className="cred-feature reveal d6">
                  <h3>{zh ? "永不过期。无续费。" : "No expiry. No renewal fees."}</h3>
                  <p>{zh ? "证书代表你构建了什么，而非你何时上了课。" : "The credential represents what you built, not when you took a course."}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 08 — BUSINESS MODEL
      ══════════════════════════════════════════ */}
      <section className="slide" id="s8">
        <div className="slide-content">
          <div className="two-col">
            <div>
              <p className="label reveal-left d1">{zh ? "商业模式" : "Business Model"}</p>
              <div className="rule-accent reveal d2" />
              <h2 className="reveal d3">
                {zh ? <>免费，是<br />一种分发战略。</> : <>Free as a<br />distribution strategy.</>}
              </h2>
              <p className="reveal d4" style={{ marginTop: "clamp(0.5rem, 1.5vh, 1rem)", fontSize: "clamp(0.7rem, 1.2vw, 0.9rem)" }}>
                {zh
                  ? "7天项目永久免费。无付费墙。无增值服务。完成项目的学员是自我认定的AI技能构建者——市场上B2C教育领域意向最强的受众。"
                  : "The 7-day program is permanently free. No paywalls. No freemium tier. Learners who complete it are self-identified AI skill builders — the highest-intent B2C education audience in the market."}
              </p>
              <p className="reveal d5" style={{ marginTop: "0.5em", fontSize: "clamp(0.7rem, 1.2vw, 0.9rem)" }}>
                {zh
                  ? "完成后：推荐付费进阶课程。转化率高，因为信任是7天积累的，而非用折扣码买来的。"
                  : "Post-completion: curated offer for paid advanced courses. Conversion is high because trust is earned over 7 days, not bought with a discount code."}
              </p>
              <div className="model-note reveal d6">
                {zh
                  ? <><strong>病毒系数：</strong>每次徽章分享均包含发行方+行动号召。每张证书都是永久免费的效果广告。</>
                  : <><strong>Viral coefficient:</strong> Every badge share includes the issuer + a CTA. Each credential is a performance ad — permanently, for free.</>}
              </div>
            </div>
            <div className="reveal-scale d3">
              <div className="funnel">
                <div className="funnel-layer fl-1">
                  {zh ? <>任何对AI感兴趣的职场人<span className="funnel-sub"> · 中英双语 · 不限职位</span></> : <>Any professional curious about AI<span className="funnel-sub"> · Bilingual (EN+ZH) · Role-agnostic</span></>}
                </div>
                <div className="funnel-arrow">↓</div>
                <div className="funnel-layer fl-2">{zh ? <>完成7天项目<br /><span className="funnel-sub">高意向 · 获得证书</span></> : <>Completes 7-day program<br /><span className="funnel-sub">High-intent · Credential earned</span></>}</div>
                <div className="funnel-arrow">↓</div>
                <div className="funnel-layer fl-3">{zh ? <>分享徽章 · 引荐他人<br /><span className="funnel-sub">自然传播 — 每枚徽章即一次引荐</span></> : <>Shares badge · Refers others<br /><span className="funnel-sub">Organic distribution — every badge is a referral</span></>}</div>
                <div className="funnel-arrow">↓</div>
                <div className="funnel-layer fl-4">{zh ? "转化为付费进阶课程" : "Converts to paid advanced course"}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 09 — TECH STACK
      ══════════════════════════════════════════ */}
      <section className="slide" id="s9">
        <div className="slide-content">
          <p className="label reveal-left d1">{zh ? "为规模化而生" : "Built to Scale"}</p>
          <h2 className="reveal d2">{zh ? "100% GCP。双语原生设计。" : "100% GCP. Bilingual by design."}</h2>
          <p className="reveal d3" style={{ marginTop: "clamp(0.4rem, 1vh, 0.75rem)" }}>
            {zh
              ? "从第一天起就在Google Cloud上的生产架构。容器化、可移植，无第三方认证锁定。"
              : "Production architecture on Google Cloud from day one. Containerized, portable, no third-party auth lock-in."}
          </p>
          <div className="stack-grid reveal d4">
            {([
              { cat: zh ? "前端"         : "Frontend",         red: true,  items: <><strong>Next.js 15</strong> App Router<br />TypeScript · Tailwind CSS v4<br />next-intl (EN + ZH)</> },
              { cat: zh ? "认证与数据"   : "Auth & Data",      red: false, items: <><strong>Firebase Auth</strong> (Google / LinkedIn / Facebook)<br /><strong>Cloud Firestore</strong> (flat collections)<br />HTTP-only session cookies</> },
              { cat: zh ? "AI / 教练"    : "AI / Coaching",    red: false, items: <><strong>Gemini 2.0 Flash</strong> — coaching, scoring, synthesis<br /><strong>Gemini 3.1 Pro</strong> — content generation<br />SSE streaming · PACE model enforced in code</> },
              { cat: zh ? "基础设施"     : "Infrastructure",   red: false, items: <><strong>Cloud Run</strong> (containerized)<br /><strong>GCS</strong> — credential assets<br />Artifact Registry · GitHub Actions CI/CD</> },
              { cat: zh ? "证书"         : "Credentials",      red: false, items: <><strong>Open Badges 3.0</strong><br />sharp (PNG) · puppeteer (PDF)<br />LinkedIn deep link standard</> },
              { cat: zh ? "内容流水线"   : "Content Pipeline", red: false, items: <><strong>7-agent pipeline</strong> (Gemini Pro + Claude)<br />Tavily live research<br />JSON schema · perishable content flags</> },
            ] as { cat: string; red: boolean; items: React.ReactNode }[]).map((block) => (
              <div key={block.cat} className={`stack-block${block.red ? " red" : ""}`}>
                <div className="stack-cat">{block.cat}</div>
                <div className="stack-items">{block.items}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 10 — ENGAGEMENT + BILINGUAL
      ══════════════════════════════════════════ */}
      <section className="slide" id="s10">
        <div className="slide-content">
          <p className="label reveal-left d1">{zh ? "参与度与留存" : "Engagement & Retention"}</p>
          <h2 className="reveal d2">
            {zh ? <>为完成而设计，<br />不为放弃而生。</> : <>Designed to be finished.<br />Not abandoned.</>}
          </h2>
          <p className="reveal d3" style={{ marginTop: "clamp(0.4rem, 1vh, 0.75rem)" }}>
            {zh
              ? "借鉴Duolingo、Uxcel及游戏化研究。每个机制都经过深思熟虑——无惩罚性设计。"
              : "Informed by Duolingo, Uxcel, and gamification research. Every mechanic is deliberate — no punitive patterns."}
          </p>
          <div className="engage-grid">
            {([
              { icon: "ph ph-flame",      d: "d3", title: zh ? "每日连击"    : "Daily Streak",  desc: zh ? "可见连击计数，若当天晚间未开始学习则显示「风险」提示。"         : "Visible streak counter with \"at risk\" nudge if day not started by evening." },
              { icon: "ph ph-seal-check", d: "d4", title: zh ? "支柱徽章"    : "Pillar Badges", desc: zh ? "通过测验后颁发。可分享。个人主页可见。共六枚可收集。"           : "Awarded on quiz pass. Shareable. Visible on profile. Six to collect." },
              { icon: "ph ph-toolbox",    d: "d5", title: zh ? "构建画廊"    : "Build Gallery", desc: zh ? "累积工具包。六件成果。随时查阅、复制和复用。"                   : "Cumulative toolkit. Six artifacts. Review, copy, and reuse at any time." },
              { icon: "ph ph-chart-bar",  d: "d4", title: zh ? "差距图谱变化" : "Gap Map Delta", desc: zh ? "第7天后重新运行诊断，查看相对第0天基准的得分提升。"              : "After Day 7: re-run diagnostic. See score improvement vs Day 0 baseline." },
              { icon: "ph ph-clock",      d: "d5", title: zh ? "微节奏"      : "Micro-pacing",  desc: zh ? "每天上限90分钟。模块设计可在午休时间完成。"                     : "90 min/day ceiling. Modules designed to complete in a lunch break." },
              { icon: "ph ph-globe",      d: "d6", title: zh ? "中英双语"    : "EN + ZH",       desc: zh ? "完整双语对等。教练支持中文输出。所有界面文字已翻译。会话内可切换。" : "Full bilingual parity. Coach streams in ZH. All UI strings translated. Toggle in-session." },
            ] as { icon: string; d: string; title: string; desc: string }[]).map((card) => (
              <div key={card.title} className={`engage-card reveal ${card.d}`}>
                <div className="engage-icon"><i className={card.icon} /></div>
                <div className="engage-title">{card.title}</div>
                <div className="engage-desc">{card.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 11 — ROADMAP
      ══════════════════════════════════════════ */}
      <section className="slide" id="s11">
        <div className="slide-content">
          <p className="label reveal-left d1">{zh ? "执行计划" : "Execution Plan"}</p>
          <h2 className="reveal d2">{zh ? "四个冲刺，走向发布。" : "Four sprints to launch."}</h2>
          <p className="reveal d3" style={{ marginTop: "clamp(0.4rem, 1vh, 0.75rem)" }}>
            {zh
              ? "两条并行轨道。内容生成第一天即启动，无需依赖代码。工程在稳固的GCP基础上顺序构建。"
              : "Two parallel tracks. Content generation starts Day 1 with no code dependency. Engineering builds sequentially on a firm GCP foundation."}
          </p>
          <div className="roadmap-row">
            {([
              { sprint: zh ? "冲刺 1" : "Sprint 1", active: true,  d: "d3",
                title: zh ? "内容生成"     : "Content Generation",
                items: zh ? "7智能体AI流水线 · 全6支柱+诊断+综合挑战 · 角色场景库 · P1试点验证"                    : "7-agent AI pipeline · All 6 pillars + diagnostic + capstone · Role context library · P1 pilot gate" },
              { sprint: zh ? "冲刺 2" : "Sprint 2", active: false, d: "d4",
                title: zh ? "应用基础"     : "App Foundation",
                items: zh ? "Next.js脚手架 · Firebase Auth · Firestore模式 · 4屏入门引导 · CI/CD至Cloud Run"    : "Next.js scaffold · Firebase Auth · Firestore schema · 4-screen onboarding · CI/CD to Cloud Run" },
              { sprint: zh ? "冲刺 3" : "Sprint 3", active: false, d: "d5",
                title: zh ? "核心学习循环" : "Core Learning Loop",
                items: zh ? "教练引擎（PACE, SSE）· 日常模块UI · 测验 · 构建成果 · 综合智能体"                    : "Coach engine (PACE, SSE) · Daily module UX · Quiz · Build artifact · Synthesis agent" },
              { sprint: zh ? "冲刺 4" : "Sprint 4", active: false, d: "d6",
                title: zh ? "项目收尾"     : "Program Completion",
                items: zh ? "仪表盘+连击 · 第7天综合挑战 · 证书生成 · 中英双语国际化"                             : "Dashboard + streak · Day 7 capstone · Credential generation · EN/ZH i18n" },
            ] as { sprint: string; active: boolean; d: string; title: string; items: string }[]).map((block) => (
              <div key={block.sprint} className={`roadmap-block${block.active ? " active" : ""} reveal ${block.d}`}>
                <div className="roadmap-sprint">{block.sprint}</div>
                <div className="roadmap-title">{block.title}</div>
                <div className="roadmap-items">{block.items}</div>
              </div>
            ))}
          </div>
          <div className="reveal d7" style={{ marginTop: "clamp(0.6rem, 1.5vh, 1.2rem)", border: "1px solid var(--border)", borderRadius: "4px", padding: "clamp(0.5rem, 1.2vw, 0.85rem)", fontSize: "clamp(0.65rem, 1.1vw, 0.82rem)", color: "var(--ink-2)" }}>
            {zh
              ? <><strong style={{ color: "var(--accent)" }}>关键路径：</strong>冲刺1 ∥ 冲刺2同时启动。冲刺2完成+冲刺1 P1内容就绪后解锁冲刺3。冲刺4收尾。</>
              : <><strong style={{ color: "var(--accent)" }}>Critical path:</strong> Sprint 1 ∥ Sprint 2 start simultaneously. Sprint 3 unlocks after Sprint 2 complete + Sprint 1 P1 content ready. Sprint 4 closes the arc.</>}
          </div>
        </div>
      </section>

      {/* ══════════════════════════════════════════
          SLIDE 12 — CTA
      ══════════════════════════════════════════ */}
      <section className="slide" id="s12">
        <div className="s12-bg" />
        <div className="big-text">AHA</div>
        <div className="slide-content">
          <p className="label reveal-left d1">{zh ? "立即开始" : "Get Started"}</p>
          <h1 className="reveal d2" style={{ maxWidth: "14ch", marginTop: "clamp(0.4rem, 1.5vh, 1rem)" }}>
            {zh ? <>成为<br /><em>AI超能职场人。</em><br />只需7天。</> : <>Become<br /><em>AI-supercharged.</em><br />In 7 days.</>}
          </h1>
          <p className="cta-sub reveal d3" style={{ marginTop: "clamp(0.6rem, 1.5vh, 1.2rem)" }}>
            {zh ? "7天。每天90分钟。你亲手搭建的AI工具包+可分享证书。免费。永久。" : "7 days. 90 minutes a day. A personal AI toolkit you built + a shareable credential. Free. Forever."}
          </p>
          <div className="reveal d4">
            <Link href="/login" className="cta-btn-lg">
              {zh ? "开始第一天" : "Start Day 1"} <em style={{ fontStyle: "normal" }}>→</em>
            </Link>
            <div className="cta-note">{zh ? "无需信用卡 · 无试用期 · 中英双语 · 永久免费" : "No credit card · No trial · EN + ZH · Free forever"}</div>
          </div>
        </div>
      </section>

    </div>
  );
}
