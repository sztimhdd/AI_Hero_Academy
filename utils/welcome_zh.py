"""
welcome_zh.py — Chinese content renderers for the Welcome page marketing sections.

Each function renders one marketing section in Chinese using st.markdown.
Called from pages/00_Welcome.py when session lang == "zh".
"""

import streamlit as st
import utils.icons as _icons


def render_hero_zh() -> None:
    st.markdown("""
<div class="demo-hero">
  <div class="demo-eyebrow">内部 · AI技能平台</div>
  <div class="demo-headline">
    让每位员工成为<br><em>AI赋能</em>的职场精英。
  </div>
  <div class="demo-subhead">
    不是另一门网络课程。<br>
    而是诊断引擎 + 个性化路径 + 实时AI辅导，
    专为每个岗位量身打造——适合您的整个团队。
  </div>
  <a class="demo-hero-cta" href="#cta-section">立即开始 &rarr;</a>
</div>
""", unsafe_allow_html=True)


def render_challenge_zh() -> None:
    st.markdown("""
<div class="demo-section-label">现实挑战</div>
<div class="demo-section-heading">您的员工已经在用AI了。问题是——他们用得对吗？</div>
<div class="demo-section-sub">三组数据，说明问题所在。</div>
""", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3, gap="medium")

    with sc1:
        st.markdown("""
<div class="demo-stat-card">
  <div class="demo-stat-number">68%</div>
  <div class="demo-stat-label">希望获得AI培训，胜过工作保障</div>
  <div class="demo-stat-context">您的员工有这个需求。AI技能已成为各职能部门最优先的职业发展方向。</div>
  <div class="demo-stat-source">Predictive Index, 2025</div>
</div>
""", unsafe_allow_html=True)

    with sc2:
        st.markdown("""
<div class="demo-stat-card">
  <div class="demo-stat-number">3×</div>
  <div class="demo-stat-label">AI实际使用量是管理层预期的3倍</div>
  <div class="demo-stat-context">影子AI已十分普遍。员工在使用管理层未批准的工具——既无规范，也无培训。</div>
  <div class="demo-stat-source">麦肯锡超级代理报告，2025</div>
</div>
""", unsafe_allow_html=True)

    with sc3:
        st.markdown("""
<div class="demo-stat-card">
  <div class="demo-stat-number">48%</div>
  <div class="demo-stat-label">将缺乏培训列为AI落地的首要障碍</div>
  <div class="demo-stat-context">培训能释放ROI。没有培训，AI工具要么闲置，要么被滥用——两种结果都会造成损失。</div>
  <div class="demo-stat-source">麦肯锡超级代理报告，2025</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-edc-callout">
  在整个组织中，已有逾100名员工提交了AI应用场景需求。
  会议支持、文件摘要和邮件撰写是三大最常见需求。
  本平台培养员工正确运用这些能力——安全、一致、可规模化。
</div>
""", unsafe_allow_html=True)


def render_loop_zh() -> None:
    st.markdown("""
<div class="demo-section-label">运作方式</div>
<div class="demo-section-heading">学习闭环</div>
<div class="demo-section-sub">四个阶段，一个持续循环，完全个性化。</div>
""", unsafe_allow_html=True)

    lc1, lc2, lc3, lc4 = st.columns(4, gap="medium")

    with lc1:
        st.markdown(f"""
<div class="demo-stage-card">
  <div class="demo-stage-icon">{_icons.ICON_DIAGNOSE}</div>
  <div class="demo-stage-num">第01阶段</div>
  <div class="demo-stage-label">诊断</div>
  <div class="demo-stage-body">6道开放性问题，由AI评分——没有标准答案，只有您的真实工作。约需5分钟，同步评估全部6个技能域。</div>
</div>
""", unsafe_allow_html=True)

    with lc2:
        st.markdown(f"""
<div class="demo-stage-card">
  <div class="demo-stage-icon">{_icons.ICON_MAP_GAPS}</div>
  <div class="demo-stage-num">第02阶段</div>
  <div class="demo-stage-label">差距图谱</div>
  <div class="demo-stage-body">AI生成个性化叙述式差距图谱，并排列您的培训路径顺序。</div>
</div>
""", unsafe_allow_html=True)

    with lc3:
        st.markdown(f"""
<div class="demo-stage-card">
  <div class="demo-stage-icon">{_icons.ICON_TRAIN}</div>
  <div class="demo-stage-num">第03阶段</div>
  <div class="demo-stage-label">训练</div>
  <div class="demo-stage-body">岗位专属场景 + 实时AI辅导员。您来练习；辅导员针对您的作答给出反馈。</div>
</div>
""", unsafe_allow_html=True)

    with lc4:
        st.markdown(f"""
<div class="demo-stage-card">
  <div class="demo-stage-icon">{_icons.ICON_SCORE}</div>
  <div class="demo-stage-num">第04阶段</div>
  <div class="demo-stage-label">评分与追踪</div>
  <div class="demo-stage-body">每完成一个模块，六边形技能雷达图即时更新。见证差距逐步缩小。</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-loop-callout">
  <strong>路径由您主导。</strong>第1模块根据您的最大差距立即解锁——
  而非按固定课程、人人相同的顺序学习。
</div>
""", unsafe_allow_html=True)


def render_tour_header_zh() -> None:
    st.markdown("""
<div class="demo-section-label">产品导览</div>
<div class="demo-section-heading">平台内部一览</div>
<div class="demo-section-sub">五个视图，一体化体验。</div>
""", unsafe_allow_html=True)


# Ordered to match tab1..tab5 in 00_Welcome.py
CAPTIONS_ZH = [
    "六道基于真实工作的开放性问题——无选择题，您描述自己如何使用AI。约需5分钟，同步评估全部6个技能域。",
    "六边形雷达图精准呈现您的能力水平。AI生成的差距图谱将原始评分转化为可立即采取行动的优先事项。",
    "每个模块以阅读部分开始，讲解核心框架——然后立即要求您将其应用于真实工作场景。",
    "AI辅导员针对您实际写下的内容作出回应——而非固定流程。它会追问、指出逻辑薄弱之处，并实时示范更好的做法。",
    "每个模块完成后，您将获得按评分标准分解的成绩和个性化辅导员点评。六边形雷达图即时更新。",
]


def render_differentiators_zh() -> None:
    st.markdown("""
<div class="demo-section-label">核心优势</div>
<div class="demo-section-heading">与众不同之处</div>
<div class="demo-section-sub">四项决策，将本平台与通用网络课程区别开来。</div>
""", unsafe_allow_html=True)

    dc1, dc2, dc3, dc4 = st.columns(4, gap="medium")

    with dc1:
        st.markdown(f"""
<div class="demo-diff-card">
  <div class="demo-diff-icon">{_icons.ICON_ROLE_SCENARIOS}</div>
  <div class="demo-diff-headline">您的岗位。您的场景。</div>
  <div class="demo-diff-body">每项练习任务均围绕您特定岗位的真实工作情境设计——客户经理、核保人、分析师。告别"写一段关于狗的提示词"此类通用练习。</div>
</div>
""", unsafe_allow_html=True)

    with dc2:
        st.markdown(f"""
<div class="demo-diff-card">
  <div class="demo-diff-icon">{_icons.ICON_AI_COACH}</div>
  <div class="demo-diff-headline">真正读懂您回答的AI辅导员。</div>
  <div class="demo-diff-body">辅导员看到您写下的确切内容，并给出有针对性的反馈。含糊的回答无法蒙混过关——它会直接指出问题。</div>
</div>
""", unsafe_allow_html=True)

    with dc3:
        st.markdown(f"""
<div class="demo-diff-card">
  <div class="demo-diff-icon">{_icons.ICON_GAPS_DRIVE}</div>
  <div class="demo-diff-headline">差距驱动学习顺序。</div>
  <div class="demo-diff-body">诊断评估6个技能域。第1模块针对您最需要提升的领域——而非按字母顺序排在最前面的那个。</div>
</div>
""", unsafe_allow_html=True)

    with dc4:
        st.markdown(f"""
<div class="demo-diff-card">
  <div class="demo-diff-icon">{_icons.ICON_LOCK}</div>
  <div class="demo-diff-headline">您的数据永不离开工作环境。</div>
  <div class="demo-diff-body">托管在GCP Cloud Run，从您组织的环境内部署。数据不发送至第三方培训平台，无需外部用户账户。</div>
</div>
""", unsafe_allow_html=True)


def render_skill_model_zh() -> None:
    st.markdown("""
<div class="demo-section-label">技能模型</div>
<div class="demo-section-heading">六大领域。一个六边形。</div>
<div class="demo-section-sub">每个领域独立评分。诊断精确告知您在每个维度的位置。</div>
""", unsafe_allow_html=True)

    _DOMAINS_ZH = [
        (_icons.ICON_RESPONSIBLE_AI, "负责任的AI",   "守护您的职业声誉"),
        (_icons.ICON_PROMPTING,      "战略性提示",   "您的个人生产力超能力"),
        (_icons.ICON_CRITICAL_EVAL,  "批判性评估",   "永不因AI错误被动陷入困境"),
        (_icons.ICON_DATA,           "数据驱动决策", "数分钟内生成洞察，而非数小时"),
        (_icons.ICON_RELATIONSHIP,   "关系智能",     "比任何人都更了解每位利益相关方"),
        (_icons.ICON_COMM,           "增强沟通",     "以3倍速交付精致成果"),
    ]

    row1 = st.columns(3, gap="medium")
    row2 = st.columns(3, gap="medium")

    for i, (icon_svg, label, reframe) in enumerate(_DOMAINS_ZH):
        col = row1[i] if i < 3 else row2[i - 3]
        with col:
            st.markdown(f"""
<div class="demo-domain-pill">
  <div class="demo-domain-emoji">{icon_svg}</div>
  <div class="demo-domain-label">{label}</div>
  <div class="demo-domain-reframe">{reframe}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="demo-attribution">
  对标 Alan Turing Institute《知识型工作者AI技能框架》（2024）。
</div>
""", unsafe_allow_html=True)


def render_mastery_zh() -> None:
    st.markdown("""
<div class="demo-mastery-row">
  <span class="demo-mastery-pill">初识</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">探索者</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill active">实践者</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">熟练者</span>
  <span class="demo-mastery-arrow">→</span>
  <span class="demo-mastery-pill">卓越者</span>
</div>
<div class="demo-mastery-note">每个领域独立评分。诊断精确告知您在每个维度的位置。</div>
""", unsafe_allow_html=True)


def render_roadmap_header_zh() -> None:
    st.markdown("""
<div class="demo-section-label">路线图</div>
<div class="demo-section-heading">未来规划</div>
<div class="demo-section-sub">这是第一版。目前已有三个职位上线。<br>以下路线图反映正在构建中的功能。</div>
""", unsafe_allow_html=True)


def render_roadmap_content_zh() -> None:
    """Render the content inside the roadmap expander in Chinese."""
    rc1, rc2 = st.columns(2, gap="medium")

    with rc1:
        st.markdown("""
<div class="demo-roadmap-card" style="margin-bottom:1rem">
  <div class="demo-roadmap-badge">🔜 第一阶段</div>
  <div class="demo-roadmap-title">更多职位</div>
  <div class="demo-roadmap-body">PM、工程师、法律、财务——相同方法论，基于同一6域技能模型构建的岗位专属场景。</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="demo-roadmap-card">
  <div class="demo-roadmap-badge">🔜 第三阶段+</div>
  <div class="demo-roadmap-title">董事会级指标</div>
  <div class="demo-roadmap-body">按领域统计达到实践者及以上水平的员工比例；可导出用于季度报告和董事会材料。</div>
</div>
""", unsafe_allow_html=True)

    with rc2:
        st.markdown("""
<div class="demo-roadmap-card" style="margin-bottom:1rem">
  <div class="demo-roadmap-badge">🔜 第三阶段+</div>
  <div class="demo-roadmap-title">组织级仪表盘</div>
  <div class="demo-roadmap-body">管理员视图：按部门的完成率、平均分，以及全员技能差距热力图。</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("""
<div class="demo-roadmap-card">
  <div class="demo-roadmap-badge">🔜 第一阶段+</div>
  <div class="demo-roadmap-title">Microsoft Copilot专题模块</div>
  <div class="demo-roadmap-body">专为M365 Copilot设计的模块——员工需求最多的工具。</div>
</div>
""", unsafe_allow_html=True)


def render_cta_zh() -> None:
    """Render the ZH CTA section header (Get Started)."""
    st.markdown("""
<div class="demo-cta-header">
  <div class="demo-section-label">开始使用</div>
  <div class="demo-cta-headline">准备好了解您的AI技能水平了吗？</div>
  <div class="demo-cta-sub">6道开放性问题。约5分钟。<br>没有标准答案——您的回答塑造您的路径。</div>
</div>
""", unsafe_allow_html=True)
