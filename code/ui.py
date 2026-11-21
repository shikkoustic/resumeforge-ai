"""ResumeForge AI — Presentation helpers, Apple-inspired Design System,
Frosted Glassmorphism, Navigation, Home Page, and Analysis UI.
"""
from __future__ import annotations

import html

# Rubric weights must match the ones in prompts/final/P1_gap_analysis.txt.
# Styled with Apple system colors (SF Blue, Indigo, Teal/Cyan, Amber, Mint).
RUBRIC = [
    ("hard_skills", "Required hard skills", 40, "linear-gradient(90deg, #0071E3, #2997FF)"),
    ("project_evidence", "Project / internship evidence", 25, "linear-gradient(90deg, #5E5CE6, #8280FF)"),
    ("measurable_impact", "Measurable impact", 15, "linear-gradient(90deg, #00A2C7, #30B0C7)"),
    ("keywords", "Role keywords", 10, "linear-gradient(90deg, #FF9500, #FFB340)"),
    ("structure", "Structure & readability", 10, "linear-gradient(90deg, #34C759, #63E6BE)"),
]

CSS = """
<style>
  /* -------------------------------------------------------------------------
     Apple System Theme & Glassmorphism Design Tokens
     ------------------------------------------------------------------------- */
  :root {
    --apple-blue: #0071E3;
    --apple-blue-hover: #0077ED;
    --apple-blue-active: #0062C4;
    --apple-blue-tint: rgba(0, 113, 227, 0.08);
    --apple-blue-border: rgba(0, 113, 227, 0.18);
    --apple-text-primary: #1D1D1F;
    --apple-text-secondary: #6E6E73;
    --apple-text-tertiary: #86868B;
    --apple-bg: #F5F5F7;
    --glass-card-bg: rgba(255, 255, 255, 0.82);
    --glass-card-border: rgba(255, 255, 255, 0.95);
    --glass-shadow: 0 4px 6px -1px rgba(0, 113, 227, 0.02), 0 12px 28px -4px rgba(0, 113, 227, 0.06), 0 24px 48px -12px rgba(0, 0, 0, 0.03);
    --glass-shadow-hover: 0 8px 16px -2px rgba(0, 113, 227, 0.05), 0 18px 36px -4px rgba(0, 113, 227, 0.1), 0 28px 56px -12px rgba(0, 0, 0, 0.06);
    --glass-rim: inset 0 0 0 1px rgba(255, 255, 255, 0.9);
    --apple-ease: cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* Typography & Antialiasing */
  html, body, [class*="st-"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", -system-ui, "Helvetica Neue", Helvetica, Arial, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -moz-osx-font-smoothing: grayscale !important;
    color: var(--apple-text-primary);
  }

  /* Global page background: Apple ambient light mesh */
  .stApp {
    background-color: var(--apple-bg) !important;
    background-image:
      radial-gradient(1200px 700px at 20% 0%, rgba(0, 113, 227, 0.08) 0%, transparent 65%),
      radial-gradient(1000px 600px at 80% 10%, rgba(90, 200, 250, 0.08) 0%, transparent 60%),
      radial-gradient(900px 800px at 50% 90%, rgba(0, 113, 227, 0.04) 0%, transparent 70%) !important;
    background-attachment: fixed !important;
  }

  /* Hide Streamlit default Deploy button, hamburger menu, footer and sidebar */
  [data-testid="stAppDeployButton"],
  .stAppDeployButton,
  #MainMenu,
  footer,
  [data-testid="stSidebar"],
  section[data-testid="stSidebar"],
  [data-testid="stSidebarCollapsedControl"],
  [data-testid="collapsedControl"],
  button[data-testid="stSidebarCollapseButton"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
  }

  /* Header adjustments */
  [data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
    height: 1.5rem !important;
  }

  .block-container {
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
    max-width: 1240px !important;
  }

  /* Entrance and Scroll-driven animations */
  @keyframes appleFloatUp {
    0% {
      opacity: 0;
      transform: translateY(16px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes appleScrollFadeIn {
    0% {
      opacity: 0;
      transform: translateY(34px) scale(0.98);
    }
    100% {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  /* Native CSS Scroll-Driven Animations (Chrome, Edge, Safari 18+) */
  @supports (animation-timeline: view()) {
    .rf-preview-card {
      animation: appleScrollFadeIn 0.75s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 5% cover 30%;
    }

    .rf-section-header {
      animation: appleScrollFadeIn 0.75s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 5% cover 30%;
    }

    .rf-features-grid .rf-feature-card:nth-child(1) {
      animation: appleScrollFadeIn 0.75s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 5% cover 28%;
    }
    .rf-features-grid .rf-feature-card:nth-child(2) {
      animation: appleScrollFadeIn 0.85s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 8% cover 32%;
    }
    .rf-features-grid .rf-feature-card:nth-child(3) {
      animation: appleScrollFadeIn 0.95s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 11% cover 35%;
    }

    .rf-timeline-grid .rf-timeline-card:nth-child(1) {
      animation: appleScrollFadeIn 0.75s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 5% cover 28%;
    }
    .rf-timeline-grid .rf-timeline-card:nth-child(2) {
      animation: appleScrollFadeIn 0.85s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 8% cover 32%;
    }
    .rf-timeline-grid .rf-timeline-card:nth-child(3) {
      animation: appleScrollFadeIn 0.95s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 11% cover 35%;
    }

    .rf-cta-banner {
      animation: appleScrollFadeIn 0.85s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 5% cover 35%;
    }

    .rf-card {
      animation: appleScrollFadeIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
      animation-timeline: view();
      animation-range: entry 5% cover 28%;
    }
  }

  /* JavaScript IntersectionObserver fallback classes */
  .rf-scroll-anim {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.65s cubic-bezier(0.16, 1, 0.3, 1),
                transform 0.65s cubic-bezier(0.16, 1, 0.3, 1);
    will-change: opacity, transform;
  }
  .rf-scroll-anim.rf-scrolled-in {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }

  @keyframes ringFillAnim {
    from {
      stroke-dashoffset: 400;
    }
  }

  @keyframes spinSlow {
    100% { transform: rotate(360deg); }
  }

  /* -------------------------------------------------------------------------
     Top Navigation Bar
     ------------------------------------------------------------------------- */
  .rf-nav-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.6rem;
    margin-bottom: 2.2rem;
    background: rgba(255, 255, 255, 0.78);
    backdrop-filter: blur(28px) saturate(190%);
    -webkit-backdrop-filter: blur(28px) saturate(190%);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-radius: 980px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03), inset 0 0 0 1px rgba(255, 255, 255, 0.9);
  }

  .rf-nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
    color: var(--apple-text-primary);
  }

  .rf-nav-mark {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: linear-gradient(135deg, #0077ED 0%, #0071E3 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFF;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 10px rgba(0, 113, 227, 0.3);
  }

  .rf-nav-name {
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.025em;
  }

  /* Style Streamlit navbar action buttons */
  .st-key-nav_btn_home, .st-key-nav_btn_analyze {
    display: flex !important;
    justify-content: flex-end !important;
  }
  .st-key-nav_btn_home button, .st-key-nav_btn_analyze button {
    border-radius: 980px !important;
    padding: 0.45rem 1.4rem !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    height: 38px !important;
    min-width: 96px !important;
    white-space: nowrap !important;
    letter-spacing: -0.01em !important;
    transition: all 0.2s var(--apple-ease) !important;
  }
  .st-key-nav_btn_home button *, .st-key-nav_btn_analyze button * {
    white-space: nowrap !important;
    font-size: 0.92rem !important;
  }

  /* -------------------------------------------------------------------------
     Home Page: Hero Section
     ------------------------------------------------------------------------- */
  .rf-home-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    padding: 2.5rem 1rem 3.5rem 1rem;
    animation: appleFloatUp 0.5s var(--apple-ease);
  }

  .rf-eyebrow-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 15px;
    border-radius: 980px;
    background: rgba(0, 113, 227, 0.08);
    border: 1px solid rgba(0, 113, 227, 0.18);
    color: var(--apple-blue);
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
  }

  .rf-eyebrow-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--apple-blue);
    box-shadow: 0 0 6px var(--apple-blue);
  }

  .rf-hero-title {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.08;
    color: var(--apple-text-primary);
    max-width: 920px;
    margin-bottom: 1.25rem;
  }

  .rf-hero-title-accent {
    background: linear-gradient(135deg, #0071E3 20%, #2997FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .rf-hero-desc {
    font-size: clamp(1.05rem, 2vw, 1.22rem);
    line-height: 1.55;
    color: var(--apple-text-secondary);
    max-width: 740px;
    margin-bottom: 2rem;
    letter-spacing: -0.015em;
  }

  /* -------------------------------------------------------------------------
     Home Page: Interactive Preview Card
     ------------------------------------------------------------------------- */
  .rf-preview-card {
    background: var(--glass-card-bg);
    backdrop-filter: blur(35px) saturate(200%);
    -webkit-backdrop-filter: blur(35px) saturate(200%);
    border: 1px solid var(--glass-card-border);
    border-radius: 24px;
    padding: 2rem 2.2rem;
    max-width: 960px;
    margin: 1rem auto 4rem auto;
    box-shadow: 0 20px 60px -15px rgba(0, 113, 227, 0.1), 0 10px 30px -10px rgba(0, 0, 0, 0.05), var(--glass-rim);
    animation: appleFloatUp 0.6s var(--apple-ease) 0.1s backwards;
  }

  .rf-preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
  }

  .rf-preview-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 980px;
    background: rgba(52, 199, 89, 0.12);
    border: 1px solid rgba(52, 199, 89, 0.25);
    color: #1E7E34;
    font-size: 0.75rem;
    font-weight: 600;
  }

  .rf-preview-grid {
    display: grid;
    grid-template-columns: 1fr 1.6fr;
    gap: 2rem;
    align-items: center;
  }

  /* -------------------------------------------------------------------------
     Home Page: Value Pillars / Features Grid
     ------------------------------------------------------------------------- */
  .rf-section-header {
    text-align: center;
    max-width: 640px;
    margin: 0 auto 2.5rem auto;
  }

  .rf-section-badge {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--apple-blue);
    margin-bottom: 0.5rem;
  }

  .rf-section-title {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--apple-text-primary);
    margin-bottom: 0.6rem;
  }

  .rf-section-sub {
    font-size: 1.02rem;
    color: var(--apple-text-secondary);
    line-height: 1.5;
  }

  .rf-features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 4rem;
  }

  .rf-feature-card {
    background: var(--glass-card-bg);
    backdrop-filter: blur(28px) saturate(190%);
    -webkit-backdrop-filter: blur(28px) saturate(190%);
    border: 1px solid var(--glass-card-border);
    border-radius: 20px;
    padding: 1.75rem 1.6rem;
    box-shadow: var(--glass-shadow), var(--glass-rim);
    transition: all 0.28s var(--apple-ease);
  }
  .rf-feature-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--glass-shadow-hover), inset 0 0 0 1px rgba(255, 255, 255, 0.95);
    border-color: rgba(0, 113, 227, 0.22);
  }

  .rf-feature-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(0, 113, 227, 0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin-bottom: 1.1rem;
    color: var(--apple-blue);
  }

  .rf-feature-title {
    font-size: 1.12rem;
    font-weight: 650;
    letter-spacing: -0.02em;
    color: var(--apple-text-primary);
    margin-bottom: 0.5rem;
  }

  .rf-feature-text {
    font-size: 0.91rem;
    line-height: 1.55;
    color: var(--apple-text-secondary);
  }

  /* -------------------------------------------------------------------------
     Home Page: Methodology Timeline
     ------------------------------------------------------------------------- */
  .rf-timeline-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-bottom: 4.5rem;
  }

  .rf-timeline-card {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 18px;
    padding: 1.6rem;
    position: relative;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
  }

  .rf-step-num {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--apple-blue);
    margin-bottom: 0.6rem;
    text-transform: uppercase;
  }

  .rf-step-title {
    font-size: 1.05rem;
    font-weight: 650;
    color: var(--apple-text-primary);
    margin-bottom: 0.45rem;
  }

  .rf-step-desc {
    font-size: 0.88rem;
    line-height: 1.52;
    color: var(--apple-text-secondary);
  }

  /* -------------------------------------------------------------------------
     Home Page: Bottom CTA Banner
     ------------------------------------------------------------------------- */
  .rf-cta-banner {
    background: linear-gradient(135deg, rgba(0, 113, 227, 0.06) 0%, rgba(90, 200, 250, 0.09) 100%), var(--glass-card-bg);
    backdrop-filter: blur(30px) saturate(190%);
    -webkit-backdrop-filter: blur(30px) saturate(190%);
    border: 1px solid rgba(0, 113, 227, 0.18);
    border-radius: 24px;
    padding: 3.4rem 2.5rem;
    text-align: center !important;
    margin-bottom: 2rem;
    box-shadow: 0 16px 40px rgba(0, 113, 227, 0.07);
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
  }

  .rf-cta-title {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: var(--apple-text-primary) !important;
    margin-bottom: 0.85rem !important;
    text-align: center !important;
    width: 100% !important;
  }

  .rf-cta-sub {
    font-size: 1.1rem !important;
    color: var(--apple-text-secondary) !important;
    max-width: 620px !important;
    margin: 0 auto 1.8rem auto !important;
    line-height: 1.55 !important;
    text-align: center !important;
    width: 100% !important;
  }

  /* -------------------------------------------------------------------------
     Analyze Page: Clean Header
     ------------------------------------------------------------------------- */
  .rf-analyze-header {
    display: flex;
    flex-direction: column;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    animation: appleFloatUp 0.45s var(--apple-ease);
  }

  .rf-brand {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .rf-mark {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #0077ED 0%, #0071E3 60%, #005BB5 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    box-shadow: 0 8px 20px rgba(0, 113, 227, 0.36), inset 0 1px 1px rgba(255, 255, 255, 0.45);
    transition: transform 0.25s var(--apple-ease);
  }
  .rf-mark:hover {
    transform: scale(1.05) rotate(2deg);
  }

  .rf-name {
    font-size: 2.35rem;
    font-weight: 700;
    letter-spacing: -0.035em;
    color: var(--apple-text-primary);
    line-height: 1.1;
  }

  .rf-tag {
    color: var(--apple-text-secondary);
    font-size: 1.05rem;
    line-height: 1.5;
    margin: 0.7rem 0 1.25rem 0;
    max-width: 760px;
  }

  .rf-pills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
  }

  .rf-pill-feature {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 980px;
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(0, 0, 0, 0.08);
    color: #3A3A3C;
    font-size: 0.82rem;
    font-weight: 500;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }

  /* -------------------------------------------------------------------------
     Clean Single-State Status Box (Fixes Overlapping Bug)
     ------------------------------------------------------------------------- */
  .rf-status-box {
    display: flex;
    align-items: center;
    gap: 14px;
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: blur(28px) saturate(190%);
    -webkit-backdrop-filter: blur(28px) saturate(190%);
    border: 1px solid rgba(0, 113, 227, 0.22);
    border-radius: 16px;
    padding: 0.95rem 1.35rem;
    margin: 1.25rem 0;
    box-shadow: 0 6px 20px rgba(0, 113, 227, 0.08);
    animation: appleFloatUp 0.3s var(--apple-ease);
  }

  .rf-status-box.running {
    border-color: rgba(0, 113, 227, 0.25);
  }

  .rf-status-box.complete {
    background: rgba(240, 253, 244, 0.88);
    border-color: rgba(52, 199, 89, 0.35);
  }

  .rf-status-box.error {
    background: rgba(254, 242, 242, 0.9);
    border-color: rgba(239, 68, 68, 0.35);
  }

  .rf-status-spinner {
    width: 22px;
    height: 22px;
    border: 2.5px solid rgba(0, 113, 227, 0.15);
    border-top-color: var(--apple-blue);
    border-radius: 50%;
    animation: spinSlow 0.8s linear infinite;
    flex-shrink: 0;
  }

  .rf-status-icon-check {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(52, 199, 89, 0.15);
    color: #1E7E34;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    flex-shrink: 0;
  }

  .rf-status-icon-error {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.15);
    color: #DC2626;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    flex-shrink: 0;
  }

  .rf-status-text-wrap {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .rf-status-step {
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--apple-blue);
  }
  .rf-status-box.complete .rf-status-step {
    color: #1E7E34;
  }
  .rf-status-box.error .rf-status-step {
    color: #DC2626;
  }

  .rf-status-msg {
    font-size: 0.92rem;
    font-weight: 550;
    color: var(--apple-text-primary);
  }

  /* -------------------------------------------------------------------------
     Glassmorphism Cards
     ------------------------------------------------------------------------- */
  .rf-card {
    background: var(--glass-card-bg) !important;
    backdrop-filter: blur(30px) saturate(190%) !important;
    -webkit-backdrop-filter: blur(30px) saturate(190%) !important;
    border: 1px solid var(--glass-card-border) !important;
    border-radius: 20px !important;
    padding: 1.6rem 1.75rem !important;
    margin-bottom: 1.35rem !important;
    box-shadow: var(--glass-shadow), var(--glass-rim) !important;
    transition: transform 0.28s var(--apple-ease),
                box-shadow 0.28s var(--apple-ease),
                border-color 0.28s ease !important;
    animation: appleFloatUp 0.45s var(--apple-ease) backwards;
  }
  .rf-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--glass-shadow-hover), inset 0 0 0 1px rgba(255, 255, 255, 0.95) !important;
    border-color: rgba(0, 113, 227, 0.24) !important;
  }

  .rf-card-title {
    font-size: 1.08rem;
    font-weight: 650;
    letter-spacing: -0.02em;
    color: var(--apple-text-primary);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .rf-icon-circle {
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: var(--apple-blue-tint);
    color: var(--apple-blue);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
  }

  .rf-input-label {
    font-size: 1.05rem;
    font-weight: 650;
    letter-spacing: -0.015em;
    color: var(--apple-text-primary);
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .rf-tab-placeholder {
    display: inline-flex;
    align-items: center;
    margin-bottom: 0.85rem;
    height: 38px;
  }
  .rf-tab-pill-static {
    display: inline-flex;
    align-items: center;
    padding: 0.45rem 1.3rem;
    font-size: 0.86rem;
    font-weight: 600;
    color: var(--apple-blue);
    background: #FFFFFF;
    border-radius: 980px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 113, 227, 0.12);
  }

  /* -------------------------------------------------------------------------
     Score Ring & Gauge
     ------------------------------------------------------------------------- */
  .rf-score-card-inner {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .rf-score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0.4rem 0 0.2rem 0;
  }
  .rf-score-svg {
    filter: drop-shadow(0 8px 18px rgba(0, 113, 227, 0.14));
    transition: transform 0.3s var(--apple-ease);
  }
  .rf-score-svg:hover {
    transform: scale(1.03);
  }
  .rf-ring-circle {
    transition: stroke-dashoffset 1.3s var(--apple-ease);
    animation: ringFillAnim 1.3s var(--apple-ease) forwards;
  }
  .rf-score-number {
    font-variant-numeric: tabular-nums;
  }
  .rf-score-status {
    margin-top: 0.8rem;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: 980px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  }

  /* -------------------------------------------------------------------------
     Rubric Bars
     ------------------------------------------------------------------------- */
  .rf-bar-row {
    margin-bottom: 0.95rem;
  }
  .rf-bar-row:last-child {
    margin-bottom: 0.15rem;
  }
  .rf-bar-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.88rem;
    font-weight: 500;
    color: #3A3A3C;
    margin-bottom: 0.4rem;
  }
  .rf-bar-badge {
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    font-size: 0.82rem;
    color: var(--apple-blue);
    background: rgba(0, 113, 227, 0.08);
    padding: 2px 8px;
    border-radius: 980px;
    border: 1px solid rgba(0, 113, 227, 0.12);
  }
  .rf-bar-badge-max {
    color: var(--apple-text-tertiary);
    font-weight: 400;
  }
  .rf-bar-track {
    background: rgba(0, 113, 227, 0.07);
    border-radius: 999px;
    height: 9px;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04);
  }
  .rf-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.9s var(--apple-ease);
  }

  /* -------------------------------------------------------------------------
     Chips & Evidence
     ------------------------------------------------------------------------- */
  .rf-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(0, 113, 227, 0.07);
    color: var(--apple-blue);
    border: 1px solid rgba(0, 113, 227, 0.18);
    border-radius: 980px;
    padding: 0.35rem 0.95rem;
    font-size: 0.85rem;
    font-weight: 550;
    margin: 0 0.45rem 0.55rem 0;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.22s var(--apple-ease);
  }
  .rf-chip:hover {
    background: rgba(0, 113, 227, 0.14);
    border-color: rgba(0, 113, 227, 0.35);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.12);
  }
  .rf-evidence {
    color: #515154;
    font-size: 0.85rem;
    font-style: italic;
    margin: -0.1rem 0 0.95rem 0.25rem;
    padding: 0.6rem 1rem;
    border-left: 3px solid var(--apple-blue);
    background: rgba(245, 247, 252, 0.7);
    border-radius: 0 12px 12px 0;
    line-height: 1.48;
  }

  /* -------------------------------------------------------------------------
     Bullet Rewrites
     ------------------------------------------------------------------------- */
  .rf-ba {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.1rem;
    margin-bottom: 0.7rem;
  }
  .rf-before, .rf-after {
    border-radius: 14px;
    padding: 1rem 1.15rem;
    font-size: 0.9rem;
    line-height: 1.54;
    transition: all 0.22s var(--apple-ease);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
  }
  .rf-before {
    background: rgba(254, 242, 242, 0.65);
    border: 1px solid rgba(239, 68, 68, 0.2);
    color: #4C2828;
  }
  .rf-before:hover {
    background: rgba(254, 242, 242, 0.85);
    border-color: rgba(239, 68, 68, 0.35);
  }
  .rf-after {
    background: rgba(240, 247, 255, 0.78);
    border: 1px solid rgba(0, 113, 227, 0.25);
    color: #0B3358;
    box-shadow: 0 4px 14px rgba(0, 113, 227, 0.05);
  }
  .rf-after:hover {
    background: rgba(240, 247, 255, 0.95);
    border-color: rgba(0, 113, 227, 0.42);
    box-shadow: 0 6px 20px rgba(0, 113, 227, 0.1);
  }
  .rf-ba-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 700;
    margin-bottom: 0.38rem;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .rf-before .rf-ba-label {
    color: #DC2626;
  }
  .rf-after .rf-ba-label {
    color: var(--apple-blue);
  }
  .rf-why {
    color: var(--apple-text-secondary);
    font-size: 0.86rem;
    line-height: 1.5;
    margin: -0.1rem 0 1.45rem 0.3rem;
    padding-left: 0.6rem;
    border-left: 2px solid rgba(0, 113, 227, 0.2);
  }
  .rf-tag-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.73rem;
    border-radius: 980px;
    padding: 0.18rem 0.65rem;
    margin-left: 0.55rem;
    vertical-align: middle;
    font-weight: 600;
  }
  .rf-tag-grounded {
    background: rgba(52, 199, 89, 0.12);
    color: #1E7E34;
    border: 1px solid rgba(52, 199, 89, 0.25);
  }

  /* -------------------------------------------------------------------------
     Red Flags & Liability Audits (Apple Inset Grouped Style)
     ------------------------------------------------------------------------- */
  .rf-flag-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
  }
  .rf-flag-count-pill {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 980px;
    background: rgba(255, 149, 0, 0.12);
    border: 1px solid rgba(255, 149, 0, 0.25);
    color: #B25E00;
  }
  .rf-flags-grouped {
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid rgba(0, 0, 0, 0.06);
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  }
  .rf-flag-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.9rem 1.2rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    transition: background 0.15s ease;
  }
  .rf-flag-item:last-child {
    border-bottom: none;
  }
  .rf-flag-item:hover {
    background: rgba(255, 149, 0, 0.04);
  }
  .rf-flag-icon-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #FF9500;
    box-shadow: 0 0 0 3px rgba(255, 149, 0, 0.16);
    flex-shrink: 0;
  }
  .rf-flag-label {
    font-size: 0.92rem;
    font-weight: 550;
    color: var(--apple-text-primary);
    line-height: 1.45;
  }
  .rf-flag-tag {
    margin-left: auto;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    padding: 2px 8px;
    border-radius: 6px;
    background: rgba(0, 0, 0, 0.04);
    color: var(--apple-text-secondary);
    flex-shrink: 0;
  }
  .rf-flags-clean {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 1rem 1.25rem;
    border-radius: 14px;
    background: rgba(52, 199, 89, 0.08);
    border: 1px solid rgba(52, 199, 89, 0.2);
  }
  .rf-flags-clean-icon {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    background: #34C759;
    color: #FFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    flex-shrink: 0;
  }
  .rf-flags-clean-text {
    font-size: 0.92rem;
    font-weight: 600;
    color: #1E7E34;
  }
  .rf-flags-clean-sub {
    font-size: 0.8rem;
    color: #2F855A;
    margin-top: 1px;
  }
  .rf-empty {
    color: var(--apple-text-tertiary);
    font-size: 0.9rem;
    padding: 0.5rem 0;
  }

  /* -------------------------------------------------------------------------
     Sidebar
     ------------------------------------------------------------------------- */
  [data-testid="stSidebar"] {
    background: rgba(245, 245, 247, 0.82) !important;
    backdrop-filter: blur(35px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(35px) saturate(200%) !important;
    border-right: 1px solid rgba(0, 0, 0, 0.07) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02) !important;
  }
  [data-testid="stSidebar"] hr {
    border-color: rgba(0, 0, 0, 0.08) !important;
    margin: 1.25rem 0 !important;
  }
  .rf-sidebar-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
  }
  .rf-mark-sm {
    width: 32px;
    height: 32px;
    border-radius: 9px;
    background: linear-gradient(135deg, #0077ED 0%, #0071E3 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 4px 10px rgba(0, 113, 227, 0.3);
  }
  .rf-sidebar-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--apple-text-primary);
    letter-spacing: -0.02em;
  }
  .rf-sidebar-sub {
    font-size: 0.75rem;
    color: var(--apple-text-tertiary);
  }

  /* -------------------------------------------------------------------------
     Streamlit Form Controls Overrides
     ------------------------------------------------------------------------- */
  [data-testid="stTextArea"], [data-testid="stTextInput"] {
    width: 100% !important;
  }
  [data-testid="stTextArea"] > div, [data-testid="stTextInput"] > div {
    width: 100% !important;
  }
  [data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    background: rgba(255, 255, 255, 0.82) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(0, 113, 227, 0.16) !important;
    border-radius: 16px !important;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.55 !important;
    color: var(--apple-text-primary) !important;
    padding: 1rem 1.2rem !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.02), 0 2px 8px rgba(0, 113, 227, 0.03) !important;
    transition: all 0.25s var(--apple-ease) !important;
  }
  [data-testid="stTextArea"] textarea:focus, [data-testid="stTextInput"] input:focus {
    background: #FFFFFF !important;
    border-color: var(--apple-blue) !important;
    box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.16), 0 8px 24px rgba(0, 113, 227, 0.08) !important;
    outline: none !important;
  }

  /* TABS - Apple Segmented Control Style */
  [data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {
    display: none !important;
  }
  [data-testid="stTabs"] {
    width: 100% !important;
    display: block !important;
  }
  [data-baseweb="tab-panel"], [data-testid="stTabContent"] {
    width: 100% !important;
    padding: 0 !important;
  }
  [data-baseweb="tab-panel"][aria-hidden="true"], [data-testid="stTabContent"][aria-hidden="true"] {
    display: none !important;
  }
  div[data-baseweb="tab-list"] {
    background: rgba(0, 0, 0, 0.05) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border-radius: 980px !important;
    padding: 3px !important;
    border: 1px solid rgba(0, 0, 0, 0.04) !important;
    display: inline-flex !important;
    gap: 2px !important;
    margin-bottom: 0.85rem !important;
    height: 38px !important;
    align-items: center !important;
    box-sizing: border-box !important;
  }
  button[data-baseweb="tab"] {
    border-radius: 980px !important;
    border: none !important;
    padding: 0.42rem 1.25rem !important;
    font-weight: 500 !important;
    font-size: 0.86rem !important;
    color: var(--apple-text-secondary) !important;
    background: transparent !important;
    transition: all 0.2s var(--apple-ease) !important;
  }
  button[data-baseweb="tab"][aria-selected="true"] {
    background: #FFFFFF !important;
    color: var(--apple-blue) !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04) !important;
  }

  /* File Uploader */
  [data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.65) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1.5px dashed rgba(0, 113, 227, 0.26) !important;
    border-radius: 16px !important;
    padding: 0.85rem !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
  }
  [data-testid="stFileUploader"]:hover {
    background: rgba(255, 255, 255, 0.88) !important;
    border-color: var(--apple-blue) !important;
    box-shadow: 0 6px 20px rgba(0, 113, 227, 0.08) !important;
  }

  /* Apple Primary Pill Button */
  button[kind="primary"], [data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primary"] {
    background: var(--apple-blue) !important;
    background-image: linear-gradient(180deg, #0077ED 0%, #0071E3 100%) !important;
    border-radius: 980px !important;
    padding: 0.65rem 1.8rem !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 4px 16px rgba(0, 113, 227, 0.35), 0 2px 4px rgba(0, 0, 0, 0.06) !important;
    cursor: pointer !important;
    white-space: nowrap !important;
    transition: all 0.25s var(--apple-ease) !important;
  }
  button[kind="primary"] *, [data-testid="stBaseButton-primary"] * {
    color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    letter-spacing: -0.01em !important;
    white-space: nowrap !important;
  }
  button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
    transform: scale(1.02) translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0, 113, 227, 0.48), 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    background-image: linear-gradient(180deg, #1A82F2 0%, #0077ED 100%) !important;
  }
  button[kind="primary"]:active, [data-testid="stBaseButton-primary"]:active {
    transform: scale(0.97) !important;
    box-shadow: 0 2px 8px rgba(0, 113, 227, 0.28) !important;
  }

  /* Apple Secondary Pill Button */
  button[kind="secondary"], .stButton > button[data-testid="stBaseButton-secondary"] {
    background: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    color: var(--apple-blue) !important;
    border-radius: 980px !important;
    border: 1px solid rgba(0, 113, 227, 0.22) !important;
    font-weight: 550 !important;
    font-size: 0.92rem !important;
    padding: 0.5rem 1.4rem !important;
    white-space: nowrap !important;
    transition: all 0.2s var(--apple-ease) !important;
    box-shadow: 0 2px 6px rgba(0, 113, 227, 0.06) !important;
  }
  button[kind="secondary"] *, .stButton > button[data-testid="stBaseButton-secondary"] * {
    white-space: nowrap !important;
  }
  button[kind="secondary"]:hover, .stButton > button[data-testid="stBaseButton-secondary"]:hover {
    background: rgba(0, 113, 227, 0.08) !important;
    border-color: var(--apple-blue) !important;
    transform: scale(1.015) !important;
    box-shadow: 0 4px 12px rgba(0, 113, 227, 0.12) !important;
  }
  button[kind="secondary"]:active, .stButton > button[data-testid="stBaseButton-secondary"]:active {
    transform: scale(0.98) !important;
  }

  [data-testid="stAlert"] {
    border-radius: 16px !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
  }

  [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.72) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(0, 0, 0, 0.07) !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03) !important;
  }

  ::-webkit-scrollbar {
    width: 7px;
    height: 7px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.15);
    border-radius: 999px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 113, 227, 0.4);
  }

  /* Ensure Streamlit scrollable main container enables scroll timeline */
  section.main, [data-testid="stMain"] {
    scroll-timeline: --mainTimeline block;
  }

  /* -------------------------------------------------------------------------
     Responsive — tablet and phone
     The layout was built for desktop only. Below 900px the multi-column grids
     squeeze text into unreadable strips, so they collapse to a single column.
     Streamlit's own st.columns do not stack on narrow screens either, so they
     are forced to full width here too.
     ------------------------------------------------------------------------- */
  @media (max-width: 900px) {
    .rf-preview-grid,
    .rf-features-grid,
    .rf-timeline-grid,
    .rf-ba {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    /* Streamlit lays columns out as flex children that never wrap */
    div[data-testid="stHorizontalBlock"] {
      flex-direction: column !important;
      gap: 0.75rem !important;
    }
    div[data-testid="stColumn"],
    div[data-testid="column"] {
      width: 100% !important;
      flex: 1 1 100% !important;
      min-width: 100% !important;
    }

    .block-container {
      padding-left: 1rem !important;
      padding-right: 1rem !important;
      padding-top: 1rem !important;
    }
  }

  @media (max-width: 640px) {
    /* The hero is sized for a wide screen; at phone width it eats the fold */
    .rf-hero-title { font-size: 2.1rem !important; line-height: 1.12 !important; }
    .rf-hero-desc  { font-size: 0.95rem !important; }

    .rf-card, .rf-feature-card, .rf-timeline-card, .rf-preview-card {
      padding: 1.05rem 1rem !important;
      border-radius: 14px !important;
    }

    /* Big numerals wrap awkwardly next to their "/ 100" suffix */
    .rf-score-value { font-size: 2.6rem !important; }

    /* Full-width tap targets, comfortably above the 44px minimum */
    .stButton > button {
      width: 100% !important;
      min-height: 46px !important;
      font-size: 0.95rem !important;
    }

    .rf-section-title { font-size: 1.15rem !important; }

    /* Nothing should force the page wider than the screen */
    .rf-preview-card, .rf-card { overflow-x: auto; }
  }

  /* Never let a long unbroken string create a horizontal scrollbar */
  .rf-quote, .rf-before, .rf-after, .rf-evidence {
    overflow-wrap: anywhere;
  }

</style>
"""


def home_hero() -> str:
    """Renders the Apple/Linear styled home page hero section without eyebrow badge."""
    return """
    <div class="rf-home-hero">
      <h1 class="rf-hero-title">
        Your resume, engineered for the role you <span class="rf-hero-title-accent">actually want</span>.
      </h1>
      <p class="rf-hero-desc">
        Stop guessing how hiring algorithms and recruiters evaluate your profile. ResumeForge delivers surgical gap analysis against any job description and grounded bullet rewrites—with zero fabricated metrics.
      </p>
    </div>
    """


def home_preview_card() -> str:
    """Renders an interactive product mockup demonstrating the dual-step pipeline."""
    return """
    <div class="rf-preview-card">
      <div class="rf-preview-header">
        <div style="display:flex;align-items:center;gap:8px;">
          <div style="width:10px;height:10px;border-radius:50%;background:#FF5F56;"></div>
          <div style="width:10px;height:10px;border-radius:50%;background:#FFBD2E;"></div>
          <div style="width:10px;height:10px;border-radius:50%;background:#27C93F;"></div>
          <span style="font-size:0.8rem;color:#86868B;margin-left:8px;font-weight:500;">Example output &mdash; illustrative, not a live run</span>
        </div>
        <div class="rf-preview-pill">✓ Strictly Grounded</div>
      </div>
      <div class="rf-preview-grid">
        <div style="text-align:center;padding:1.1rem;background:rgba(255,255,255,0.72);border-radius:18px;border:1px solid rgba(0,0,0,0.05);">
          <div style="font-size:0.75rem;font-weight:700;color:#0071E3;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.45rem;">Match Score</div>
          <div class="rf-score-value" style="font-size:3.2rem;font-weight:700;color:#1D1D1F;letter-spacing:-0.03em;line-height:1;display:flex;align-items:baseline;justify-content:center;gap:6px;">
            <span>84</span><span style="font-size:1.3rem;color:#86868B;font-weight:500;letter-spacing:-0.01em;">/ 100</span>
          </div>
          <div style="font-size:0.8rem;color:#34C759;font-weight:600;margin-top:0.45rem;">● Strong Role Alignment</div>
          <div style="font-size:0.75rem;color:#86868B;margin-top:0.6rem;">Evaluated against 5 placement rubrics</div>
        </div>
        <div>
          <div style="font-size:0.75rem;font-weight:700;color:#86868B;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.6rem;">Surgical Bullet Rewrite Example</div>
          <div style="background:#FFF5F5;border:1px solid #FFE0E0;border-radius:12px;padding:0.7rem 0.9rem;font-size:0.84rem;color:#7A3B3B;margin-bottom:0.6rem;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#DC2626;margin-bottom:0.2rem;">Original (Vague)</div>
            Did web development using React and improved performance.
          </div>
          <div style="background:#F0F7FF;border:1px solid rgba(0,113,227,0.22);border-radius:12px;padding:0.7rem 0.9rem;font-size:0.84rem;color:#0B3358;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;color:#0071E3;margin-bottom:0.2rem;">Rewritten (Grounded & Impactful)</div>
            Engineered responsive client-facing modules in React, optimizing frontend rendering lifecycle without inventing unverified metrics.
          </div>
        </div>
      </div>
    </div>
    """


def home_features() -> str:
    """Renders the 3 core pillars of the product."""
    return """
    <div class="rf-section-header">
      <div class="rf-section-badge">The Precision Standard</div>
      <h2 class="rf-section-title">Engineered for credibility, not hype.</h2>
      <p class="rf-section-sub">Generic AI resume tools fabricate metrics that get candidates disqualified during interviews. ResumeForge enforces mathematical grounding.</p>
    </div>
    <div class="rf-features-grid">
      <div class="rf-feature-card">
        <div class="rf-feature-icon">🎯</div>
        <div class="rf-feature-title">Rubric Gap Analysis</div>
        <div class="rf-feature-text">Step 1 calculates a weighted match score across 5 placement dimensions: hard skills (40%), project evidence (25%), measurable impact (15%), keywords (10%), and structure (10%).</div>
      </div>
      <div class="rf-feature-card">
        <div class="rf-feature-icon">🛡️</div>
        <div class="rf-feature-title">Zero Metric Hallucination</div>
        <div class="rf-feature-text">Step 2 rewrites flagged bullets by rephrasing your actual contributions with stronger action verbs and technical specificity—never generating fake percentage increases.</div>
      </div>
      <div class="rf-feature-card">
        <div class="rf-feature-icon">🔍</div>
        <div class="rf-feature-title">Quoted JD Evidence</div>
        <div class="rf-feature-text">Every missing skill identifies the exact phrase from the job description it originated from, eliminating guesswork and giving you verifiable talking points.</div>
      </div>
    </div>
    """


def home_methodology() -> str:
    """Renders the 3-step workflow."""
    return """
    <div class="rf-section-header">
      <div class="rf-section-badge">Methodology</div>
      <h2 class="rf-section-title">How the dual-prompt pipeline works</h2>
      <p class="rf-section-sub">Splitting analysis from rewriting prevents LLMs from confabulating claims.</p>
    </div>
    <div class="rf-timeline-grid">
      <div class="rf-timeline-card">
        <div class="rf-step-num">Step 01</div>
        <div class="rf-step-title">Input & Context Ingestion</div>
        <div class="rf-step-desc">Provide your current resume (paste text or upload a PDF) alongside the target job posting. Our engine extracts clean textual content and prepares structure tokens.</div>
      </div>
      <div class="rf-timeline-card">
        <div class="rf-step-num">Step 02</div>
        <div class="rf-step-title">Strict Rubric Scoring (P1)</div>
        <div class="rf-step-desc">Prompt 1 acts purely as an auditor. It scores against 5 weighted categories, identifies missing skills with verbatim quotes, and flags weak bullet points without rewriting.</div>
      </div>
      <div class="rf-timeline-card">
        <div class="rf-step-num">Step 03</div>
        <div class="rf-step-title">Grounded Bullet Rewrites (P2)</div>
        <div class="rf-step-desc">Prompt 2 takes only the weak bullets identified by P1 and transforms them into crisp, high-impact statements strictly adhering to the candidate's existing experience.</div>
      </div>
    </div>
    """


def home_cta() -> str:
    """Renders the bottom CTA banner on the home page with perfectly centered typography."""
    return """
    <div class="rf-cta-banner">
      <h2 class="rf-cta-title" style="text-align:center !important;width:100% !important;margin-left:auto !important;margin-right:auto !important;">Ready to optimize your application?</h2>
      <p class="rf-cta-sub" style="text-align:center !important;width:100% !important;margin:0 auto 1.8rem auto !important;">Run your resume against your target role in seconds. Completely private, instantaneous, and rubric-verified.</p>
    </div>
    """


def analyze_header() -> str:
    """Apple-styled clean header for the Analyze page without project/academic branding."""
    return """
    <div class="rf-analyze-header">
      <div class="rf-brand">
        <div class="rf-mark">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
        </div>
        <div>
          <div class="rf-name">ResumeForge AI</div>
        </div>
      </div>
      <div class="rf-tag">
        Paste a resume and a target job description below to generate an instant, rubric-weighted gap analysis and grounded bullet rewrites.
      </div>
      <div class="rf-pills-row">
        <div class="rf-pill-feature"><span>⚡</span> Two-Prompt Sequential Pipeline (P1 → P2)</div>
        <div class="rf-pill-feature"><span>🎯</span> 5-Dimension Rubric Scoring</div>
        <div class="rf-pill-feature"><span>🛡️</span> Zero Fabricated Metrics Guarantee</div>
      </div>
    </div>
    """


def status_banner(step: str, message: str, state: str = "running") -> str:
    """Single-state clean status banner that avoids overlapping text and glitching."""
    step_clean = html.escape(step)
    msg_clean = html.escape(message)

    if state == "complete":
        icon_html = '<div class="rf-status-icon-check">✓</div>'
        css_state = "complete"
    elif state == "error":
        icon_html = '<div class="rf-status-icon-error">!</div>'
        css_state = "error"
    else:
        icon_html = '<div class="rf-status-spinner"></div>'
        css_state = "running"

    return f"""
    <div class="rf-status-box {css_state}">
      {icon_html}
      <div class="rf-status-text-wrap">
        <div class="rf-status-step">{step_clean}</div>
        <div class="rf-status-msg">{msg_clean}</div>
      </div>
    </div>
    """


def score_card(score: int) -> str:
    """Renders the Overall Match score matching the crisp typography and layout of the home screen preview."""
    score = max(0, min(100, int(score)))

    if score >= 70:
        status_label = "Strong Match"
        status_bg = "rgba(52, 199, 89, 0.12)"
        status_color = "#1E7E34"
        bar_grad = "linear-gradient(90deg, #0071E3, #34C759)"
    elif score >= 45:
        status_label = "Moderate Match"
        status_bg = "rgba(255, 149, 0, 0.12)"
        status_color = "#B25E00"
        bar_grad = "linear-gradient(90deg, #FF9500, #FFCC00)"
    else:
        status_label = "Needs Alignment"
        status_bg = "rgba(255, 59, 48, 0.12)"
        status_color = "#D32F2F"
        bar_grad = "linear-gradient(90deg, #FF3B30, #FF6482)"

    return f"""
    <div style="text-align:center;padding:1.4rem 1.2rem;background:rgba(255,255,255,0.72);border-radius:18px;border:1px solid rgba(0,0,0,0.05);box-shadow:0 4px 20px rgba(0,0,0,0.02);">
      <div style="font-size:0.78rem;font-weight:700;color:#0071E3;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.45rem;">
        Match Score
      </div>
      <div class="rf-score-value" style="font-size:3.5rem;font-weight:700;color:#1D1D1F;letter-spacing:-0.03em;line-height:1;margin-bottom:0.55rem;display:flex;align-items:baseline;justify-content:center;gap:6px;font-feature-settings:'tnum' 1;">
        <span>{score}</span><span style="font-size:1.35rem;color:#86868B;font-weight:500;letter-spacing:-0.01em;">/ 100</span>
      </div>
      <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:980px;background:{status_bg};color:{status_color};font-size:0.82rem;font-weight:600;margin-bottom:0.85rem;">
        <span style="font-size:8px;">●</span> {status_label}
      </div>
      <div style="width:100%;height:8px;background:rgba(0,0,0,0.05);border-radius:980px;overflow:hidden;margin-bottom:0.65rem;">
        <div style="width:{score}%;height:100%;background:{bar_grad};border-radius:980px;transition:width 0.8s cubic-bezier(0.16,1,0.3,1);"></div>
      </div>
      <div style="font-size:0.78rem;color:#86868B;font-weight:500;">
        Evaluated across 5 placement rubrics
      </div>
    </div>
    """


score_ring = score_card


def red_flags_card(flags: list[str]) -> str:
    """Renders an Apple Settings-style grouped audit card for detected liabilities."""
    if not flags:
        return """
        <div class="rf-card">
          <div class="rf-card-title">
            <span class="rf-icon-circle">⚠️</span> Red flags detected
          </div>
          <div class="rf-flags-clean">
            <div class="rf-flags-clean-icon">✓</div>
            <div>
              <div class="rf-flags-clean-text">Zero red flags detected</div>
              <div class="rf-flags-clean-sub">No formatting liabilities, critical gaps, or disqualifying issues found.</div>
            </div>
          </div>
        </div>
        """

    count_label = f"{len(flags)} item" if len(flags) == 1 else f"{len(flags)} items"
    rows = []
    for f in flags:
        clean_text = html.escape(str(f))
        rows.append(
            f'<div class="rf-flag-item">'
            f'<div class="rf-flag-icon-dot"></div>'
            f'<div class="rf-flag-label">{clean_text}</div>'
            f'<div class="rf-flag-tag">Attention</div>'
            f'</div>'
        )

    return f"""
    <div class="rf-card">
      <div class="rf-flag-card-header">
        <div class="rf-card-title" style="margin-bottom:0;">
          <span class="rf-icon-circle">⚠️</span> Red flags detected
        </div>
        <div class="rf-flag-count-pill">{count_label}</div>
      </div>
      <div class="rf-flags-grouped">
        {''.join(rows)}
      </div>
    </div>
    """


def rubric_bars(breakdown: dict) -> str:
    """One bar per rubric dimension, scaled to that dimension's maximum."""
    rows = []
    for key, label, maximum, colour in RUBRIC:
        got = breakdown.get(key)
        if got is None:
            continue
        got = max(0, min(maximum, int(got)))
        pct = (got / maximum) * 100
        rows.append(
            f'<div class="rf-bar-row">'
            f'<div class="rf-bar-top">'
            f'<span class="rf-bar-label">{html.escape(label)}</span>'
            f'<span class="rf-bar-badge">{got} <span class="rf-bar-badge-max">/ {maximum}</span></span>'
            f'</div>'
            f'<div class="rf-bar-track">'
            f'<div class="rf-bar-fill" style="width:{pct:.0f}%;background:{colour};"></div>'
            f'</div></div>'
        )
    if not rows:
        return '<div class="rf-empty">No breakdown returned.</div>'
    return "".join(rows)
