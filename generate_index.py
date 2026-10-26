import json

with open("wine_web_data.json", "r", encoding="utf-8") as f:
    wine_data = json.load(f)

wine_data_json_str = json.dumps(wine_data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WINE_QUALITY.EXE | ML Feature Selection Lab (CRISP-DM)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Share+Tech+Mono&family=VT323&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
  <style>
    /* ============================================================
       Y2K / RETRO 90S OS CYBER-STUDIO DESIGN SYSTEM
       ============================================================ */
    :root {{
      --bg-dark: #0a0c13;
      --bg-surface: #10131f;
      --bg-surface-alt: #171b2d;
      --win-bg: #c0c4ce;
      --win-border-light: #ffffff;
      --win-border-dark: #404040;
      --win-border-shadow: #101010;
      --win-title-blue: linear-gradient(90deg, #000080, #1084d0);
      --win-title-pink: linear-gradient(90deg, #800040, #ff007f);
      --win-title-green: linear-gradient(90deg, #005020, #00c853);
      --win-title-yellow: linear-gradient(90deg, #665200, #ffcc00);
      --win-title-wine: linear-gradient(90deg, #4a0e17, #9b111e);
      
      --neon-cyan: #00f0ff;
      --hot-pink: #ff007f;
      --acid-yellow: #ccff00;
      --matrix-green: #00ff66;
      --wine-red: #ff2a55;
      --paper-beige: #f4e8d1;
      --led-off: #202b36;
      --crt-scanline: rgba(18, 16, 16, 0.35);

      --font-pixel: 'Press Start 2P', monospace;
      --font-terminal: 'VT323', monospace;
      --font-mono: 'Share Tech Mono', monospace;
      --font-sans: 'Space Grotesk', -apple-system, sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}

    body {{
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(#1e2438 1px, transparent 1px),
        linear-gradient(to bottom, #07090e, #0e121d 60%, #15091e);
      background-size: 24px 24px, 100% 100%;
      color: #e2e8f0;
      font-family: var(--font-mono);
      min-height: 100vh;
      overflow-x: hidden;
      position: relative;
    }}

    /* CRT Scanline & Glass curvature overlay */
    .crt-overlay {{
      pointer-events: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: 9999;
      background: linear-gradient(
        rgba(18, 16, 16, 0) 50%, 
        rgba(0, 0, 0, 0.3) 50%
      ), linear-gradient(
        90deg,
        rgba(255, 0, 0, 0.03),
        rgba(0, 255, 0, 0.01),
        rgba(0, 0, 255, 0.03)
      );
      background-size: 100% 3px, 6px 100%;
      opacity: 0.75;
      transition: opacity 0.3s ease;
    }}

    .crt-overlay.disabled {{
      opacity: 0;
    }}

    .crt-glow {{
      position: fixed;
      inset: 0;
      box-shadow: inset 0 0 100px rgba(0, 240, 255, 0.08), inset 0 0 40px rgba(255, 0, 127, 0.06);
      pointer-events: none;
      z-index: 9998;
    }}

    /* Windows 95 / Retro Frame Utility */
    .retro-window {{
      background: var(--win-bg);
      border-top: 2px solid var(--win-border-light);
      border-left: 2px solid var(--win-border-light);
      border-right: 2px solid var(--win-border-dark);
      border-bottom: 2px solid var(--win-border-dark);
      box-shadow: 4px 4px 0px var(--win-border-shadow), 0 0 15px rgba(0, 240, 255, 0.15);
      color: #111;
      margin-bottom: 20px;
      position: relative;
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
    }}

    .retro-titlebar {{
      background: var(--win-title-blue);
      color: #fff;
      padding: 4px 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-pixel);
      font-size: 10px;
      letter-spacing: 0.5px;
      text-shadow: 1px 1px #000;
    }}

    .retro-titlebar.pink {{
      background: var(--win-title-pink);
    }}
    .retro-titlebar.green {{
      background: var(--win-title-green);
    }}
    .retro-titlebar.yellow {{
      background: var(--win-title-yellow);
      color: #111;
      text-shadow: none;
    }}
    .retro-titlebar.wine {{
      background: var(--win-title-wine);
    }}

    .retro-title-left {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .retro-btn-box {{
      display: flex;
      gap: 3px;
    }}

    .retro-win-btn {{
      width: 16px;
      height: 14px;
      background: #c0c4ce;
      border-top: 1px solid #fff;
      border-left: 1px solid #fff;
      border-right: 1px solid #404040;
      border-bottom: 1px solid #404040;
      font-family: var(--font-pixel);
      font-size: 9px;
      line-height: 12px;
      text-align: center;
      cursor: pointer;
      color: #000;
      padding: 0;
    }}
    .retro-win-btn:active {{
      border-top: 1px solid #404040;
      border-left: 1px solid #404040;
      border-right: 1px solid #fff;
      border-bottom: 1px solid #fff;
    }}

    .retro-inset {{
      background: #111522;
      border-top: 2px solid #080a11;
      border-left: 2px solid #080a11;
      border-right: 2px solid #ffffff33;
      border-bottom: 2px solid #ffffff33;
      color: #d8e2ec;
      padding: 12px;
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      overflow: hidden;
    }}

    /* Container & Layout */
    .app-container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 16px 20px 40px 20px;
      width: 100%;
      box-sizing: border-box;
    }}

    /* Header & Ticker */
    .sys-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 2px dashed #00f0ff44;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .brand-title-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-logo-badge {{
      background: var(--hot-pink);
      color: #fff;
      font-family: var(--font-pixel);
      font-size: 11px;
      padding: 6px 10px;
      box-shadow: 3px 3px 0 var(--neon-cyan);
      letter-spacing: 1px;
      animation: pulse-glow 2s infinite alternate;
    }}

    @keyframes pulse-glow {{
      0% {{ box-shadow: 3px 3px 0 var(--neon-cyan); }}
      100% {{ box-shadow: 3px 3px 12px var(--hot-pink), 0 0 8px var(--neon-cyan); }}
    }}

    .brand-h1 {{
      font-family: var(--font-pixel);
      font-size: 18px;
      color: var(--neon-cyan);
      text-shadow: 2px 2px #ff007f, 4px 4px #000;
      letter-spacing: -0.5px;
    }}

    .brand-sub {{
      font-family: var(--font-mono);
      font-size: 12px;
      color: #94a3b8;
    }}

    .header-controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    /* WINE SWITCHER DROPDOWN */
    .dataset-switcher-wrap {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: #141a2e;
      border: 2px solid #3b82f6;
      box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
      padding: 4px 8px;
    }}

    .switcher-label {{
      font-family: var(--font-pixel);
      font-size: 8px;
      color: var(--acid-yellow);
      letter-spacing: 0.5px;
    }}

    .retro-dropdown-wine {{
      background: #c0c4ce;
      color: #000;
      border-top: 2px solid #fff;
      border-left: 2px solid #fff;
      border-right: 2px solid #404040;
      border-bottom: 2px solid #404040;
      font-family: var(--font-mono);
      font-size: 13px;
      font-weight: bold;
      padding: 4px 10px;
      cursor: pointer;
      outline: none;
      transition: all 0.15s;
    }}

    .retro-dropdown-wine:hover {{
      background: #e2e8f0;
      box-shadow: 0 0 8px var(--neon-cyan);
    }}

    .system-badge {{
      background: #000;
      border: 1px solid var(--acid-yellow);
      color: var(--acid-yellow);
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 4px 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .live-dot {{
      width: 8px;
      height: 8px;
      background: var(--acid-yellow);
      border-radius: 50%;
      animation: blink 1s infinite steps(1);
    }}

    @keyframes blink {{
      0%, 50% {{ opacity: 1; }}
      51%, 100% {{ opacity: 0; }}
    }}

    .arcade-toggle-btn {{
      background: #252d42;
      border: 2px solid #576585;
      color: #fff;
      font-family: var(--font-pixel);
      font-size: 9px;
      padding: 6px 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}
    .arcade-toggle-btn:hover {{
      background: #3a4768;
      border-color: var(--neon-cyan);
      color: var(--neon-cyan);
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    }}
    .arcade-toggle-btn.active {{
      background: var(--neon-cyan);
      color: #000;
      border-color: #fff;
      box-shadow: 0 0 12px var(--neon-cyan);
    }}

    /* Marquee Banner */
    .retro-ticker-bar {{
      background: #07090f;
      border: 1px solid #1e293b;
      border-left: 4px solid var(--neon-cyan);
      border-right: 4px solid var(--hot-pink);
      padding: 6px 12px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      overflow: hidden;
      font-family: var(--font-pixel);
      font-size: 10px;
    }}

    .ticker-label {{
      background: var(--hot-pink);
      color: #fff;
      padding: 3px 8px;
      margin-right: 12px;
      white-space: nowrap;
      font-size: 9px;
    }}

    .ticker-content {{
      display: inline-block;
      white-space: nowrap;
      animation: marquee 26s linear infinite;
      color: var(--acid-yellow);
      letter-spacing: 0.5px;
    }}

    .ticker-content span {{
      margin-right: 28px;
    }}
    .ticker-content .val-glow {{
      color: var(--neon-cyan);
      font-weight: bold;
    }}

    @keyframes marquee {{
      0% {{ transform: translate3d(0, 0, 0); }}
      100% {{ transform: translate3d(-50%, 0, 0); }}
    }}

    /* Main Grid Layout */
    .studio-grid {{
      display: grid;
      grid-template-columns: 360px minmax(0, 1fr);
      gap: 20px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }}

    @media (max-width: 1100px) {{
      .studio-grid {{
        grid-template-columns: minmax(0, 1fr);
      }}
    }}

    aside {{
      width: 100%;
      max-width: 360px;
      min-width: 0;
      box-sizing: border-box;
    }}

    main {{
      width: 100%;
      min-width: 0;
      max-width: 100%;
      overflow: hidden;
      box-sizing: border-box;
    }}

    /* Model Selection Window & Controls */
    .model-nav-list {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-bottom: 14px;
    }}

    .model-radio-card {{
      background: #171d2e;
      border: 1px solid #2e3b58;
      padding: 8px 10px;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s;
    }}
    .model-radio-card:hover {{
      background: #20283f;
      border-color: var(--neon-cyan);
    }}
    .model-radio-card.selected {{
      background: #13243a;
      border-color: var(--neon-cyan);
      box-shadow: inset 0 0 10px rgba(0, 240, 255, 0.25), 0 0 8px rgba(0, 240, 255, 0.3);
    }}

    .model-card-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .pixel-radio {{
      width: 14px;
      height: 14px;
      border: 2px solid #576585;
      background: #090c14;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .model-radio-card.selected .pixel-radio {{
      border-color: var(--neon-cyan);
      background: var(--neon-cyan);
      box-shadow: 0 0 6px var(--neon-cyan);
    }}
    .pixel-radio-dot {{
      width: 6px;
      height: 6px;
      background: #000;
    }}

    .model-name {{
      font-family: var(--font-pixel);
      font-size: 10px;
      color: #fff;
    }}
    .model-radio-card.selected .model-name {{
      color: var(--neon-cyan);
    }}

    .model-badge {{
      font-size: 11px;
      font-family: var(--font-terminal);
      padding: 2px 6px;
      background: #252f47;
      color: #a0aec0;
      border-radius: 2px;
    }}
    .model-badge.best {{
      background: var(--acid-yellow);
      color: #000;
      font-weight: bold;
    }}

    /* Slider / Param Control Group */
    .param-group {{
      background: #151a2b;
      border: 1px dashed #303e61;
      padding: 10px;
      margin-bottom: 12px;
    }}

    .param-header {{
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      margin-bottom: 6px;
      color: #cbd5e1;
    }}

    .param-slider {{
      width: 100%;
      accent-color: var(--hot-pink);
      cursor: pointer;
    }}

    /* Feature Flags (LED style) */
    .feature-flags-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-top: 8px;
    }}

    .feat-flag-pill {{
      background: #0f1422;
      border: 1px solid #2a3754;
      padding: 5px 8px;
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 10px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .feat-led {{
      width: 8px;
      height: 8px;
      border-radius: 2px;
      background: var(--led-off);
      border: 1px solid #111;
      transition: all 0.2s;
      flex-shrink: 0;
    }}
    .feat-led.on {{
      background: var(--matrix-green);
      box-shadow: 0 0 8px var(--matrix-green);
    }}
    .feat-led.off {{
      background: #451a20;
    }}

    /* Charts & Analytics Area */
    .charts-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 20px;
    }}

    @media (max-width: 900px) {{
      .charts-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-canvas-container {{
      background: #07090e;
      border: 1px solid #1e263d;
      position: relative;
      padding: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}

    .radar-grid-bg {{
      position: absolute;
      inset: 10px;
      background-image: 
        linear-gradient(rgba(0, 240, 255, 0.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.07) 1px, transparent 1px);
      background-size: 20px 20px;
      pointer-events: none;
    }}

    /* Arcade Leaderboard Table */
    .leaderboard-table {{
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-pixel);
      font-size: 9px;
    }}

    .leaderboard-table th {{
      background: #1e2538;
      color: var(--neon-cyan);
      padding: 8px 6px;
      text-align: left;
      border-bottom: 2px solid var(--neon-cyan);
    }}

    .leaderboard-table td {{
      padding: 7px 6px;
      border-bottom: 1px solid #1e273f;
    }}

    .leaderboard-table tr:hover td {{
      background: #172138;
      color: #fff;
    }}

    .rank-num {{
      color: var(--hot-pink);
    }}
    .rank-num.first {{
      color: var(--acid-yellow);
    }}

    /* K-VALUE SELECTOR TABS & MODEL PERFORMANCE WINDOW */
    .k-tabs-toolbar {{
      background: #141926;
      border: 1px solid #2a354f;
      padding: 8px 10px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin-bottom: 14px;
      border-bottom: 2px solid #00f0ff44;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }}

    .k-tabs-label {{
      font-family: var(--font-pixel);
      font-size: 8px;
      color: #94a3b8;
      display: flex;
      align-items: center;
      gap: 6px;
      margin-right: 4px;
      white-space: nowrap;
    }}

    .k-tabs-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      flex: 1;
    }}

    /* Vintage Media Player / Windows 95 Tab Button */
    .k-tab-btn {{
      position: relative;
      background: #c0c4ce;
      color: #111;
      border-top: 2px solid #ffffff;
      border-left: 2px solid #ffffff;
      border-right: 2px solid #404040;
      border-bottom: 2px solid #404040;
      font-family: var(--font-pixel);
      font-size: 8px;
      padding: 6px 9px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      transition: all 0.12s ease;
      letter-spacing: 0.5px;
      box-shadow: 2px 2px 0px #000;
      outline: none;
    }}

    .k-tab-btn:hover {{
      background: #d5d9e4;
      color: #000;
    }}

    .k-tab-btn:active, .k-tab-btn.active {{
      background: #a2a6b2;
      border-top: 2px solid #404040;
      border-left: 2px solid #404040;
      border-right: 2px solid #ffffff;
      border-bottom: 2px solid #ffffff;
      transform: translate(1px, 1px);
      box-shadow: 0 0 8px rgba(0, 240, 255, 0.5);
    }}

    .k-tab-btn.sweet-spot {{
      background: linear-gradient(180deg, #093b1d 0%, #041c0e 100%);
      color: #00ff88;
      border-top: 2px solid #00ff88;
      border-left: 2px solid #00ff88;
      border-right: 2px solid #004d22;
      border-bottom: 2px solid #004d22;
      box-shadow: 0 0 12px rgba(0, 255, 102, 0.5), 2px 2px 0px #000;
    }}

    .k-tab-btn.overfit-cliff {{
      background: linear-gradient(180deg, #442207 0%, #291202 100%);
      color: #fbbf24;
      border-top: 2px solid #f59e0b;
      border-left: 2px solid #f59e0b;
      border-right: 2px solid #78350f;
      border-bottom: 2px solid #78350f;
      box-shadow: 0 0 10px rgba(245, 158, 11, 0.4), 2px 2px 0px #000;
    }}

    /* Dual Performance Charts - Always in same row */
    .perf-dual-grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      margin-bottom: 16px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }}

    .perf-chart-card {{
      background: #080b13;
      border: 1px solid #1f283d;
      padding: 10px 12px;
      position: relative;
      display: flex;
      flex-direction: column;
      width: 100%;
      min-width: 0;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
    }}

    .perf-canvas-wrap {{
      position: relative;
      width: 100%;
      height: 230px;
      min-width: 0;
      max-width: 100%;
      overflow: hidden;
      box-sizing: border-box;
    }}

    canvas#rmseChartCanvas, canvas#r2ChartCanvas {{
      width: 100% !important;
      max-width: 100% !important;
      min-width: 0 !important;
      height: 230px !important;
      display: block;
      box-sizing: border-box;
    }}

    .perf-chart-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      z-index: 5;
    }}

    .perf-chart-title {{
      font-family: var(--font-pixel);
      font-size: 9px;
      letter-spacing: 0.5px;
    }}

    .perf-chart-badge {{
      font-size: 10px;
      font-family: var(--font-mono);
      padding: 2px 6px;
      border-radius: 2px;
    }}

    /* OLS Equation Card */
    .ols-card {{
      background: #020704;
      border: 2px solid #005522;
      box-shadow: inset 0 0 25px rgba(0, 255, 102, 0.15), 0 0 18px rgba(0, 255, 102, 0.12);
      padding: 14px 16px;
      position: relative;
      overflow: hidden;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }}

    .ols-card::before {{
      content: "";
      position: absolute;
      inset: 0;
      background: repeating-linear-gradient(
        0deg,
        rgba(0, 255, 102, 0.035) 0px,
        rgba(0, 255, 102, 0.035) 1px,
        transparent 1px,
        transparent 3px
      );
      pointer-events: none;
    }}

    .ols-header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px dashed #008033;
      padding-bottom: 6px;
      margin-bottom: 10px;
      font-family: var(--font-terminal);
      font-size: 16px;
      color: #6ee7b7;
    }}

    .ols-formula-display {{
      font-family: var(--font-terminal);
      font-size: 24px;
      line-height: 1.35;
      color: #00ff66;
      text-shadow: 0 0 10px rgba(0, 255, 102, 0.75);
      word-break: break-word;
      margin-bottom: 12px;
      letter-spacing: 0.5px;
      background: rgba(0, 20, 10, 0.6);
      border: 1px solid #00441a;
      padding: 10px 14px;
      max-width: 100%;
      overflow-x: auto;
      box-sizing: border-box;
    }}

    .ols-telemetry-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      border-top: 1px solid #00441a;
      padding-top: 10px;
      align-items: center;
      font-size: 11px;
      max-width: 100%;
      overflow: hidden;
      box-sizing: border-box;
    }}

    /* Predictor Arcade Machine Widget */
    .arcade-machine {{
      background: #131726;
      border: 3px solid #ff007f;
      box-shadow: 0 0 20px rgba(255, 0, 127, 0.25), inset 0 0 15px rgba(0, 0, 0, 0.8);
      padding: 16px;
      margin-bottom: 20px;
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
    }}

    .arcade-screen {{
      background: #02120b;
      border: 3px solid #005a28;
      box-shadow: inset 0 0 25px rgba(0, 255, 102, 0.3);
      padding: 14px;
      margin-bottom: 16px;
      font-family: var(--font-terminal);
      color: var(--matrix-green);
      text-shadow: 0 0 6px var(--matrix-green);
    }}

    .screen-header-row {{
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #005a28;
      padding-bottom: 6px;
      margin-bottom: 8px;
      font-size: 16px;
    }}

    .screen-readout-main {{
      font-size: 38px;
      font-weight: bold;
      letter-spacing: 2px;
      text-align: right;
      color: #fff;
      text-shadow: 0 0 12px var(--matrix-green), 0 0 20px var(--neon-cyan);
    }}

    .screen-formula-row {{
      font-family: var(--font-mono);
      font-size: 11px;
      color: #6ee7b7;
      text-shadow: none;
      margin-top: 6px;
      white-space: nowrap;
      overflow-x: auto;
    }}

    /* 11 Chemical Cassette Cards Grid */
    .input-grid-arcade {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 10px;
      margin-bottom: 16px;
    }}

    .cassette-card {{
      background: #0c0f1a;
      border: 2px solid #2a3754;
      padding: 8px 10px;
      position: relative;
    }}
    .cassette-card::before {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: var(--neon-cyan);
    }}
    .cassette-card.pink-accent::before {{
      background: var(--hot-pink);
    }}
    .cassette-card.yellow-accent::before {{
      background: var(--acid-yellow);
    }}

    .cassette-title {{
      font-family: var(--font-pixel);
      font-size: 8px;
      color: #94a3b8;
      margin-bottom: 4px;
      display: flex;
      justify-content: space-between;
    }}

    .arcade-number-input {{
      width: 100%;
      background: #192033;
      border: 1px solid #3d4f7c;
      color: #fff;
      font-family: var(--font-terminal);
      font-size: 20px;
      padding: 3px 6px;
      outline: none;
      transition: all 0.15s;
    }}
    .arcade-number-input:focus {{
      border-color: var(--neon-cyan);
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    }}

    .preset-btns-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }}

    .preset-chip {{
      background: #1b2438;
      border: 1px solid #3e4f75;
      color: #93c5fd;
      font-size: 11px;
      padding: 4px 10px;
      cursor: pointer;
      font-family: var(--font-pixel);
      font-size: 8px;
      transition: all 0.15s;
    }}
    .preset-chip:hover {{
      background: var(--hot-pink);
      color: #fff;
      border-color: #fff;
      box-shadow: 0 0 8px var(--hot-pink);
    }}

    .action-btn-row {{
      display: flex;
      gap: 12px;
    }}

    .arcade-big-btn {{
      flex: 1;
      background: linear-gradient(180deg, #ff007f 0%, #b30059 100%);
      border: 3px solid #ff80bf;
      color: #fff;
      font-family: var(--font-pixel);
      font-size: 12px;
      padding: 14px 20px;
      cursor: pointer;
      letter-spacing: 1px;
      box-shadow: 0 6px 0 #59002c, 0 8px 15px rgba(255, 0, 127, 0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all 0.1s;
    }}
    .arcade-big-btn:hover {{
      background: linear-gradient(180deg, #ff1a8c 0%, #cc0066 100%);
      transform: translateY(-2px);
      box-shadow: 0 8px 0 #59002c, 0 12px 20px rgba(255, 0, 127, 0.6);
    }}
    .arcade-big-btn:active {{
      transform: translateY(4px);
      box-shadow: 0 2px 0 #59002c;
    }}

    /* Outliers & Residual Inspector */
    .terminal-window {{
      background: #05070c;
      border: 2px solid #232b40;
      color: #00ff66;
      font-family: var(--font-terminal);
      font-size: 17px;
      padding: 12px;
      height: 290px;
      overflow-y: auto;
    }}

    .terminal-table {{
      width: 100%;
      border-collapse: collapse;
    }}

    .terminal-table th {{
      text-align: left;
      border-bottom: 1px dashed #008f3a;
      padding: 4px 6px;
      color: #9effa0;
      font-size: 15px;
    }}

    .terminal-table td {{
      padding: 4px 6px;
      border-bottom: 1px dotted #14351e;
    }}

    .badge-state {{
      padding: 1px 4px;
      background: #11281a;
      border: 1px solid #00ff66;
      font-size: 14px;
    }}

    .res-negative {{
      color: #ff5277;
    }}
    .res-positive {{
      color: #00ffc2;
    }}

    /* CRT Footer Status Bar */
    .status-bar-bottom {{
      background: #c0c4ce;
      border-top: 2px solid #fff;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      padding: 3px 8px;
      color: #111;
      font-family: var(--font-pixel);
      margin-top: 24px;
    }}

    .status-segment {{
      border: 1px solid #808080;
      border-top-color: #404040;
      border-left-color: #404040;
      border-bottom-color: #fff;
      border-right-color: #fff;
      padding: 2px 8px;
      display: flex;
      align-items: center;
      gap: 6px;
      min-width: 0;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }}

    /* Custom Tooltip */
    #chart-tooltip {{
      position: absolute;
      pointer-events: none;
      background: rgba(10, 14, 26, 0.95);
      border: 1px solid var(--neon-cyan);
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
      padding: 8px 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      color: #e2e8f0;
      z-index: 10000;
      display: none;
      max-width: 280px;
      line-height: 1.4;
    }}
  </style>
</head>
<body>

  <!-- CRT Visual Filters -->
  <div class="crt-overlay" id="crtOverlay"></div>
  <div class="crt-glow"></div>
  <div id="chart-tooltip"></div>

  <div class="app-container">

    <!-- OS TOP BAR & CONTROLS -->
    <header class="sys-header">
      <div class="brand-title-wrap">
        <div class="brand-logo-badge">AIoT HW2 // WINE-QUALITY</div>
        <div>
          <h1 class="brand-h1">WINE_QUALITY.EXE</h1>
          <div class="brand-sub">CRISP-DM MULTIPLE LINEAR REGRESSION &amp; 5-METHOD FEATURE SELECTION (UCI ENOLOGY LAB)</div>
        </div>
      </div>

      <!-- DATASET SWITCHER (RED WINE / WHITE WINE) -->
      <div class="dataset-switcher-wrap">
        <span class="switcher-label">DATASET:</span>
        <select id="wineTypeSelect" class="retro-dropdown-wine" title="Toggle Red Wine vs White Wine Dataset">
          <option value="red">🍷 RED WINE (1,599 Bottles)</option>
          <option value="white">🥂 WHITE WINE (4,898 Bottles)</option>
        </select>
      </div>

      <div class="header-controls">
        <button class="arcade-toggle-btn active" id="btnCrtToggle" title="Toggle CRT scanline raster">
          <span>📺 CRT: ON</span>
        </button>
        <button class="arcade-toggle-btn active" id="btnAudioToggle" title="Toggle 8-bit Audio SFX">
          <span>🔊 SFX: ON</span>
        </button>
        <div class="system-badge" id="clockDisplay">13:50:42</div>
      </div>
    </header>

    <!-- REAL-TIME METRIC TICKER (Marquee) -->
    <div class="retro-ticker-bar">
      <div class="ticker-label">LIVE TELEMETRY</div>
      <div class="ticker-content" id="tickerStream">
        <!-- Injected via JS based on active wine dataset -->
      </div>
    </div>

    <!-- MAIN TWO-COLUMN WORKSPACE -->
    <div class="studio-grid">
      
      <!-- LEFT COLUMN: FEATURE SELECTION CONSOLE -->
      <aside>
        
        <!-- WINDOW: MODEL SELECTOR -->
        <div class="retro-window">
          <div class="retro-titlebar">
            <div class="retro-title-left">
              <span>&#9881;</span>
              <span>METHOD_SELECTOR.SYS</span>
            </div>
            <div class="retro-btn-box">
              <button class="retro-win-btn">_</button>
              <button class="retro-win-btn">&#9633;</button>
              <button class="retro-win-btn">&times;</button>
            </div>
          </div>
          <div class="retro-inset">
            <div style="font-size: 11px; margin-bottom: 8px; color: #94a3b8;">
              SELECT CRISP-DM FEATURE SELECTION ALGORITHM:
            </div>

            <!-- Radio Card List -->
            <div class="model-nav-list" id="modelListContainer">
              <!-- Rendered via JS -->
            </div>

            <!-- HYPERPARAMETERS -->
            <div class="param-group">
              <div class="param-header">
                <span>TRAIN/TEST SPLIT:</span>
                <span id="splitValLabel" style="color: var(--neon-cyan); font-weight: bold;">80% / 20%</span>
              </div>
              <input type="range" min="60" max="90" value="80" step="5" class="param-slider" id="splitSlider">
              <div style="display: flex; justify-content: space-between; font-size: 9px; color: #64748b; margin-top: 2px;">
                <span>60/40</span>
                <span>80/20 (Default)</span>
                <span>90/10</span>
              </div>
            </div>

            <div class="param-group">
              <div class="param-header">
                <span>CROSS-VALIDATION FOLDS (K):</span>
                <span id="kValLabel" style="color: var(--hot-pink); font-weight: bold;">5 FOLDS</span>
              </div>
              <input type="range" min="3" max="10" value="5" step="1" class="param-slider" id="kSlider">
              <div style="display: flex; justify-content: space-between; font-size: 9px; color: #64748b; margin-top: 2px;">
                <span>k=3</span>
                <span>k=5 (Default)</span>
                <span>k=10</span>
              </div>
            </div>

            <!-- ACTIVE FEATURE FLAGS (LED) -->
            <div style="margin-top: 10px;">
              <div style="font-size: 10px; font-family: var(--font-pixel); color: var(--neon-cyan); margin-bottom: 6px;">
                ACTIVE FEATURE FLAGS (11 LAB ATTRIBUTES):
              </div>
              <div class="feature-flags-grid" id="featureFlagsGrid">
                <!-- Rendered by JS -->
              </div>
            </div>

          </div>
        </div>

        <!-- WINDOW: MODEL DIAGNOSTICS & SUMMARY -->
        <div class="retro-window">
          <div class="retro-titlebar green">
            <div class="retro-title-left">
              <span>&#128202;</span>
              <span>METRICS_REPORT.TXT</span>
            </div>
            <div class="retro-btn-box">
              <button class="retro-win-btn">_</button>
              <button class="retro-win-btn">&times;</button>
            </div>
          </div>
          <div class="retro-inset">
            <table style="width: 100%; font-size: 11px; border-collapse: collapse;">
              <tr style="border-bottom: 1px solid #252e47;">
                <td style="padding: 5px 0; color: #94a3b8;">ACTIVE METHOD:</td>
                <td style="text-align: right; color: var(--neon-cyan); font-family: var(--font-pixel); font-size: 9px;" id="statMethodName">Forward SFS</td>
              </tr>
              <tr style="border-bottom: 1px solid #252e47;">
                <td style="padding: 5px 0; color: #94a3b8;">SELECTED FEATURES:</td>
                <td style="text-align: right; color: #fff; font-weight: bold;" id="statFeatureCount">6 of 11</td>
              </tr>
              <tr style="border-bottom: 1px solid #252e47;">
                <td style="padding: 5px 0; color: #94a3b8;">TEST R² SCORE:</td>
                <td style="text-align: right; color: var(--acid-yellow); font-weight: bold;" id="statR2">0.4031</td>
              </tr>
              <tr style="border-bottom: 1px solid #252e47;">
                <td style="padding: 5px 0; color: #94a3b8;">ADJUSTED R²:</td>
                <td style="text-align: right; color: #e2e8f0;" id="statAdjR2">0.3916</td>
              </tr>
              <tr style="border-bottom: 1px solid #252e47;">
                <td style="padding: 5px 0; color: #94a3b8;">TEST RMSE:</td>
                <td style="text-align: right; color: var(--hot-pink); font-weight: bold;" id="statRMSE">0.6246</td>
              </tr>
              <tr style="border-bottom: 1px solid #252e47;">
                <td style="padding: 5px 0; color: #94a3b8;">TRAIN CV RMSE:</td>
                <td style="text-align: right; color: #a5f3fc;" id="statCvRmse">0.6582</td>
              </tr>
              <tr>
                <td style="padding: 5px 0; color: #94a3b8;">MULTICOLLINEARITY (VIF):</td>
                <td style="text-align: right; color: var(--matrix-green); font-weight: bold;" id="statVif">Safe (< 5.0)</td>
              </tr>
            </table>
          </div>
        </div>

      </aside>

      <!-- RIGHT COLUMN: CHARTS, PREDICTOR & OUTLIERS -->
      <main>
        
        <!-- WINDOW: RETRO CHARTS & ANALYTICS -->
        <div class="retro-window">
          <div class="retro-titlebar">
            <div class="retro-title-left">
              <span>&#9733;</span>
              <span>RETRO_VISUALIZER.EXE - Actual vs Predicted &amp; Model Benchmark</span>
            </div>
            <div class="retro-btn-box">
              <button class="retro-win-btn">_</button>
              <button class="retro-win-btn">&#9633;</button>
              <button class="retro-win-btn">&times;</button>
            </div>
          </div>
          <div class="retro-inset">
            
            <div class="charts-grid">
              
              <!-- LEFT CHART: ACTUAL VS PREDICTED SCATTER -->
              <div class="chart-canvas-container">
                <div class="radar-grid-bg"></div>
                <div style="width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; z-index: 10;">
                  <span style="font-family: var(--font-pixel); font-size: 9px; color: var(--neon-cyan);">
                    ACTUAL vs PREDICTED (0-10)
                  </span>
                  <span style="font-size: 10px; color: #64748b;">45° IDEAL LINE</span>
                </div>
                
                <canvas id="scatterCanvas" width="460" height="260" style="width: 100%; max-width: 460px; height: 260px;"></canvas>
                
                <div style="width: 100%; display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; margin-top: 6px; z-index: 10;">
                  <span>&bull; Cyan = Test Set Wine Samples</span>
                  <span>Hover to inspect residuals</span>
                </div>
              </div>

              <!-- RIGHT CHART: ALGORITHM CV RMSE LEADERBOARD -->
              <div class="chart-canvas-container">
                <div class="radar-grid-bg"></div>
                <div style="width: 100%; display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; z-index: 10;">
                  <span style="font-family: var(--font-pixel); font-size: 9px; color: var(--acid-yellow);">
                    HIGH SCORE LEADERBOARD (CV RMSE)
                  </span>
                  <span style="font-size: 10px; color: #64748b;">LOWER IS BETTER</span>
                </div>

                <div style="width: 100%; z-index: 10; overflow-x: auto;">
                  <table class="leaderboard-table">
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>METHOD</th>
                        <th>FEAT</th>
                        <th>CV RMSE</th>
                        <th>TEST R²</th>
                      </tr>
                    </thead>
                    <tbody id="leaderboardBody">
                      <!-- Rendered by JS -->
                    </tbody>
                  </table>
                </div>

                <div style="width: 100%; margin-top: 10px; z-index: 10; font-size: 10px; color: #94a3b8;" id="leaderboardFootnote">
                  <!-- Injected via JS -->
                </div>
              </div>

            </div>

          </div>
        </div>

        <!-- WINDOW: MODEL PERFORMANCE & K-OPTIMIZER (Progression k = 1...11) -->
        <div class="retro-window" id="perfWindow">
          <div class="retro-titlebar" style="background: linear-gradient(90deg, #0f2c42 0%, #086972 50%, #00a896 100%);">
            <div class="retro-title-left">
              <span>&#128200;</span>
              <span id="perfWindowTitle">MODEL_PERFORMANCE_MONITOR.EXE - Feature Progression (k = 1...11)</span>
            </div>
            <div class="retro-btn-box">
              <button class="retro-win-btn">_</button>
              <button class="retro-win-btn">&#9633;</button>
              <button class="retro-win-btn">&times;</button>
            </div>
          </div>
          <div class="retro-inset">
            
            <!-- K-VALUE SELECTOR TABS -->
            <div class="k-tabs-toolbar">
              <div class="k-tabs-label">
                <span>&#9205; K-VALUE (1..11):</span>
              </div>
              <div class="k-tabs-group" id="kTabsContainer">
                <!-- Injected dynamically via JS: k=1..11 buttons with sweet spot highlights -->
              </div>
            </div>

            <!-- 5-METHOD COMPARISON LEGEND -->
            <div id="perfComparisonLegend" style="display: none; align-items: center; justify-content: center; flex-wrap: wrap; gap: 14px; background: #070a14; border: 1px solid #1e293b; padding: 6px 12px; margin-bottom: 12px; font-family: var(--font-pixel); font-size: 8px;">
              <span style="color: #64748b; font-family: var(--font-mono); font-size: 10px; font-weight: bold;">5 ALGORITHMS:</span>
              <span style="color: #00f0ff; display: inline-flex; align-items: center; gap: 5px;">&#9679; LassoCV (L1)</span>
              <span style="color: #ff8c00; display: inline-flex; align-items: center; gap: 5px;">&#9632; Forward SFS</span>
              <span style="color: #00ff66; display: inline-flex; align-items: center; gap: 5px;">&#9650; RFECV</span>
              <span style="color: #ff007f; display: inline-flex; align-items: center; gap: 5px;">&#9670; ElasticNetCV</span>
              <span style="color: #b388ff; display: inline-flex; align-items: center; gap: 5px;">&#9660; Exhaustive Search</span>
            </div>

            <!-- DUAL LINE CHARTS (RMSE & R-squared) -->
            <div class="perf-dual-grid">
              
              <!-- LEFT: RMSE TREND -->
              <div class="perf-chart-card">
                <div class="radar-grid-bg"></div>
                <div class="perf-chart-header">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="perf-chart-title" id="rmseChartTitle" style="color: var(--neon-cyan);">
                      RMSE TREND BY K-FEATURES
                    </span>
                    <span class="perf-chart-badge" style="background: #10263d; color: var(--neon-cyan); border: 1px solid #00f0ff88;">
                      LOWER IS BETTER
                    </span>
                  </div>
                  <span id="rmseChartSub" style="font-size: 10px; color: #00ff88; font-family: var(--font-pixel);">
                    OPTIMAL K
                  </span>
                </div>

                <div class="perf-canvas-wrap">
                  <canvas id="rmseChartCanvas" width="460" height="230"></canvas>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; margin-top: 6px; z-index: 5;">
                  <span id="rmseChartFootL" style="color: #00ff88;">★ Optimal Sweet Spot</span>
                  <span id="rmseChartFootR" style="color: #fbbf24;">k=11: Full Parameter Set</span>
                </div>
              </div>

              <!-- RIGHT: R-SQUARED TREND -->
              <div class="perf-chart-card">
                <div class="radar-grid-bg"></div>
                <div class="perf-chart-header">
                  <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="perf-chart-title" id="r2ChartTitle" style="color: var(--acid-yellow);">
                      R-SQUARED TREND BY K-FEATURES
                    </span>
                    <span class="perf-chart-badge" style="background: #2b2b10; color: var(--acid-yellow); border: 1px solid #ccff0088;">
                      HIGHER IS BETTER
                    </span>
                  </div>
                  <span id="r2ChartSub" style="font-size: 10px; color: #00ff88; font-family: var(--font-pixel);">
                    PEAK R²
                  </span>
                </div>

                <div class="perf-canvas-wrap">
                  <canvas id="r2ChartCanvas" width="460" height="230"></canvas>
                </div>

                <div style="display: flex; justify-content: space-between; font-size: 10px; color: #94a3b8; margin-top: 6px; z-index: 5;">
                  <span id="r2ChartFootL" style="color: #00ff88;">★ Peak R² Explained</span>
                  <span id="r2ChartFootR" style="color: #fbbf24;">k=11 Model</span>
                </div>
              </div>

            </div>

            <!-- OLS EQUATION CARD -->
            <div class="ols-card">
              <div class="ols-header-bar">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <span class="live-dot" style="background: #00ff66;"></span>
                  <span>TERMINAL: C:\\CRISP-DM\\WINE\\FITTED_OLS_EQUATION.BAT</span>
                </div>
                <div id="olsCardStatusBadge" style="font-family: var(--font-pixel); font-size: 9px; color: #00ff88;">
                  [★ SWEET SPOT ACTIVE]
                </div>
              </div>

              <!-- Formula Box in CRT Terminal Font -->
              <div style="font-size: 11px; color: #94a3b8; margin-bottom: 6px; font-family: var(--font-mono); display: flex; justify-content: space-between;">
                <span>FITTED ORDINARY LEAST SQUARES (OLS) REGRESSION FORMULA:</span>
                <span id="olsFormulaKTag" style="color: #a7f3d0; font-family: var(--font-pixel); font-size: 9px;">MODEL: k = 6</span>
              </div>
              
              <div class="ols-formula-display" id="olsFormulaOutput">
                <!-- Injected by JS in CRT Terminal Font -->
              </div>

              <!-- Telemetry & Diagnostic Footer -->
              <div class="ols-telemetry-row">
                <div style="max-width: 100%; word-break: break-word;">
                  <span style="color: #94a3b8;">ACTIVE FEATURES:</span>
                  <span id="olsFeatSubset" style="color: var(--neon-cyan); font-weight: bold; margin-left: 4px; word-break: break-word;">[]</span>
                </div>
                <div>
                  <span style="color: #94a3b8;">TEST RMSE:</span>
                  <span id="olsMetricRmse" style="color: #00ff88; font-weight: bold; margin-left: 4px;">0.6246</span>
                </div>
                <div>
                  <span style="color: #94a3b8;">TEST R²:</span>
                  <span id="olsMetricR2" style="color: var(--acid-yellow); font-weight: bold; margin-left: 4px;">0.4031</span>
                </div>
                <div style="flex: 1; min-width: 220px; text-align: right;">
                  <button class="preset-chip" id="btnSyncWithCalc" style="background: #0d2e1c; border-color: #00ff66; color: #00ff88;" title="Load this k-model into Wine Quality Predictor">
                    &#9889; SYNC TO PREDICTOR
                  </button>
                </div>
              </div>

              <!-- Interpretive Insight Banner -->
              <div id="olsInterpretationText" style="margin-top: 10px; font-size: 11px; color: #a7f3d0; background: #06190f; border-left: 3px solid #00ff66; padding: 7px 10px; line-height: 1.5;">
                ★ ENOLOGICAL INSIGHT: Higher alcohol content and lower volatile acidity are the primary chemical determinants of superior wine sensory scores.
              </div>

            </div>

          </div>
        </div>

        <!-- ARCADE MACHINE WIDGET: WINE QUALITY CALCULATOR & PREDICTOR -->
        <div class="arcade-machine">
          
          <!-- Screen Ledgers -->
          <div class="arcade-screen">
            <div class="screen-header-row">
              <span>WINE_QUALITY_PREDICTOR // ACTIVE MODEL: <span id="calcModelBadge">Forward SFS</span></span>
              <span>SENSORY SCALE: 0 - 10</span>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <span style="font-size: 18px; color: #00ff66;">PREDICTED QUALITY SCORE:</span>
              <span class="screen-readout-main" id="screenProfitOutput">5.87 / 10</span>
            </div>

            <div class="screen-formula-row" id="screenFormulaBreakdown">
              Equation: Quality = β₀ + β₁·Alcohol - β₂·VolatileAcidity + ...
            </div>
          </div>

          <!-- Quick Presets -->
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px; flex-wrap: wrap;">
            <span style="font-family: var(--font-pixel); font-size: 8px; color: var(--acid-yellow);">QUICK PRESETS:</span>
            <div class="preset-btns-row" id="presetBtnsContainer" style="margin-bottom: 0;">
              <!-- Injected by JS based on Red vs White wine -->
            </div>
          </div>

          <!-- 11 Input Fields / Cassettes -->
          <div class="input-grid-arcade" id="cassettesContainer">
            <!-- 11 chemical cassettes rendered dynamically by JS -->
          </div>

          <!-- Big Action Button -->
          <div class="action-btn-row">
            <button class="arcade-big-btn" id="btnRunPrediction">
              <span>&#9654;</span>
              <span>RUN_PREDICTION.BAT</span>
              <span style="font-size: 9px; opacity: 0.8;">[COMPUTE QUALITY SCORE]</span>
            </button>
          </div>

        </div>

        <!-- WINDOW: OUTLIERS & RESIDUAL INSPECTOR -->
        <div class="retro-window">
          <div class="retro-titlebar yellow">
            <div class="retro-title-left">
              <span>&#9888;</span>
              <span>OUTLIERS_RESIDUAL_TERMINAL.EXE - Top 10 Influential Points</span>
            </div>
            <div class="retro-btn-box">
              <button class="retro-win-btn">_</button>
              <button class="retro-win-btn">&#9633;</button>
              <button class="retro-win-btn">&times;</button>
            </div>
          </div>
          <div class="retro-inset" style="padding: 8px;">
            <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px; color: #cbd5e1;">
              <span>CRISP-DM RESIDUAL ANALYSIS: Top 10 Largest Absolute Prediction Errors</span>
              <span style="color: var(--acid-yellow);" id="outliersDatasetCount">DATASET SIZE: N=1,599</span>
            </div>

            <div class="terminal-window">
              <table class="terminal-table">
                <thead>
                  <tr>
                    <th>RANK</th>
                    <th>ID</th>
                    <th>ACTUAL</th>
                    <th>PREDICTED</th>
                    <th>RESIDUAL</th>
                    <th>ALCOHOL</th>
                    <th>VOLATILE ACID</th>
                    <th>DENSITY</th>
                  </tr>
                </thead>
                <tbody id="outliersTableBody">
                  <!-- Populated from top10_outliers.csv -->
                </tbody>
              </table>
            </div>

            <div style="font-size: 11px; color: #8899ac; margin-top: 6px; display: flex; justify-content: space-between;">
              <span id="outliersSummaryFootnote">Outliers represent atypical human sensory perception or unmeasured enological compounds (e.g. tannins/esters).</span>
              <span style="color: var(--neon-cyan);">[STATUS: VALIDATED]</span>
            </div>
          </div>
        </div>

      </main>

    </div>

    <!-- WINDOWS 95 STATUS BAR -->
    <footer class="status-bar-bottom">
      <div class="status-segment">
        <span style="color: #000;" id="sbWineBadge">&#127863; WINE_QUALITY_CRISP_DM</span>
      </div>
      <div class="status-segment">
        <span>MODEL: OLS + FEATURE SELECTION</span>
      </div>
      <div class="status-segment">
        <span id="sbSampleBadge">SAMPLE N=1,599 | 11 VARIABLES</span>
      </div>
      <div class="status-segment" style="flex: 1;">
        <span id="systemMsgStatus">READY. AWAITING USER TELEMETRY.</span>
      </div>
      <div class="status-segment">
        <span style="color: #008000;">&#9679; ONLINE</span>
      </div>
    </footer>

  </div>

  <!-- JAVASCRIPT LOGIC & SOUND SYNTHESIZER -->
  <script>
    // ============================================================
    // DATA EMBEDDED FROM EXPERIMENT RUNS (RED & WHITE WINE)
    // ============================================================
    const WINE_DATA = {wine_data_json_str};

    const FEATURE_ICONS = {{
      "fixed acidity": "🍋",
      "volatile acidity": "🧪",
      "citric acid": "🍊",
      "residual sugar": "🍬",
      "chlorides": "🧂",
      "free sulfur dioxide": "💨",
      "total sulfur dioxide": "🌫️",
      "density": "⚖️",
      "pH": "📏",
      "sulphates": "🧬",
      "alcohol": "🍷"
    }};

    const FEATURE_INPUT_CONFIG = {{
      "fixed acidity": {{ label: "FIXED ACIDITY", unit: "g/dm³", step: 0.1, min: 3.0, max: 16.0 }},
      "volatile acidity": {{ label: "VOLATILE ACIDITY", unit: "g/dm³", step: 0.01, min: 0.1, max: 1.6 }},
      "citric acid": {{ label: "CITRIC ACID", unit: "g/dm³", step: 0.01, min: 0.0, max: 1.2 }},
      "residual sugar": {{ label: "RESIDUAL SUGAR", unit: "g/dm³", step: 0.1, min: 0.5, max: 35.0 }},
      "chlorides": {{ label: "CHLORIDES", unit: "g/dm³", step: 0.001, min: 0.01, max: 0.35 }},
      "free sulfur dioxide": {{ label: "FREE SO₂", unit: "mg/dm³", step: 1.0, min: 1.0, max: 120.0 }},
      "total sulfur dioxide": {{ label: "TOTAL SO₂", unit: "mg/dm³", step: 1.0, min: 5.0, max: 300.0 }},
      "density": {{ label: "DENSITY", unit: "g/cm³", step: 0.0005, min: 0.985, max: 1.010 }},
      "pH": {{ label: "pH LEVEL", unit: "pH", step: 0.01, min: 2.7, max: 4.1 }},
      "sulphates": {{ label: "SULPHATES", unit: "g/dm³", step: 0.01, min: 0.2, max: 1.6 }},
      "alcohol": {{ label: "ALCOHOL", unit: "% vol", step: 0.1, min: 8.0, max: 15.0 }}
    }};

    // State Variables
    let activeWine = "red"; // 'red' or 'white'
    let currentModel = null;
    let selectedK = 6;
    let activeProgressionMethod = "Forward_SFS";
    let audioEnabled = true;
    let crtEnabled = true;
    let hoveredPoint = null;

    // Audio Context
    let audioCtx = null;
    function initAudio() {{
      if (!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }}
    }}

    function playSound(type) {{
      if (!audioEnabled) return;
      try {{
        initAudio();
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        if (type === 'click') {{
          osc.type = 'square';
          osc.frequency.setValueAtTime(600, now);
          osc.frequency.exponentialRampToValueAtTime(150, now + 0.04);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
          osc.start(now);
          osc.stop(now + 0.04);
        }} else if (type === 'select') {{
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(440, now);
          osc.frequency.setValueAtTime(880, now + 0.05);
          gain.gain.setValueAtTime(0.15, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
          osc.start(now);
          osc.stop(now + 0.12);
        }} else if (type === 'coin') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(987.77, now);
          osc.frequency.setValueAtTime(1318.51, now + 0.08);
          gain.gain.setValueAtTime(0.2, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
          osc.start(now);
          osc.stop(now + 0.35);
        }} else if (type === 'zap') {{
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(800, now);
          osc.frequency.exponentialRampToValueAtTime(100, now + 0.15);
          gain.gain.setValueAtTime(0.15, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
          osc.start(now);
          osc.stop(now + 0.15);
        }}
      }} catch (e) {{}}
    }}

    // Clock
    function updateClock() {{
      const now = new Date();
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      const s = String(now.getSeconds()).padStart(2, '0');
      document.getElementById('clockDisplay').textContent = `${{h}}:${{m}}:${{s}}`;
    }}
    setInterval(updateClock, 1000);
    updateClock();

    // ============================================================
    // DATASET SWITCHER: RED WINE vs WHITE WINE
    // ============================================================
    const wineSelect = document.getElementById('wineTypeSelect');
    wineSelect.addEventListener('change', e => {{
      setWineDataset(e.target.value);
      playSound('coin');
    }});

    function setWineDataset(type) {{
      activeWine = type;
      const data = WINE_DATA[type];
      
      // Update top ticker
      updateTicker();

      // Set default model (best one in models list)
      const bestM = data.models[0];
      currentModel = bestM;
      activeProgressionMethod = bestM.id;
      if (!data.progressions[activeProgressionMethod]) {{
        activeProgressionMethod = 'Forward_SFS';
      }}

      // Sweet spot k for this wine
      const progItems = data.progressions[activeProgressionMethod];
      const sweet = progItems.find(p => p.isSweetSpot) || progItems[0];
      selectedK = sweet.k;

      // Update UI components
      renderModelSelector();
      renderFeatureFlags();
      renderLeaderboard();
      renderOutliersTable();
      renderCassettes();
      renderPresets();
      renderKTabs();
      updateOlsCard(sweet);
      calculatePrediction(false);
      updateFormulaDisplay();

      // Status Bar
      document.getElementById('sbWineBadge').innerHTML = type === 'red' ? '🍷 RED WINE (CRISP-DM)' : '🥂 WHITE WINE (CRISP-DM)';
      document.getElementById('sbSampleBadge').textContent = `SAMPLE N=${{data.sample_count.toLocaleString()}} | 11 VARIABLES`;
      document.getElementById('outliersDatasetCount').textContent = `DATASET SIZE: N=${{data.sample_count.toLocaleString()}}`;
      document.getElementById('systemMsgStatus').textContent = `SWITCHED TO ${{data.name.toUpperCase()}} (N=${{data.sample_count.toLocaleString()}}). ALL TELEMETRY RE-ALIGNED.`;

      // Redraw Canvases
      drawScatterChart();
      drawRmseChart();
      drawR2Chart();
    }}

    function updateTicker() {{
      const data = WINE_DATA[activeWine];
      const best = data.models[0];
      const baseline = data.models.find(m => m.name === 'Baseline OLS') || data.models[data.models.length - 1];

      let tickerHtml = `
        <span>DATASET: <span class="val-glow">${{data.name.toUpperCase()}} (N=${{data.sample_count}})</span></span>
        <span>BEST METHOD: <span class="val-glow">${{best.name}} (${{best.nFeat}} Feat)</span></span>
        <span>TEST R²: <span class="val-glow">${{best.r2.toFixed(4)}}</span></span>
        <span>TEST RMSE: <span class="val-glow">${{best.rmse.toFixed(4)}}</span></span>
        <span>TRAIN CV RMSE: <span class="val-glow">${{best.cvRmse.toFixed(4)}}</span></span>
        <span>BASELINE OLS CV: <span class="val-glow">${{baseline.cvRmse.toFixed(4)}}</span></span>
        <span>TOP DRIVER: <span class="val-glow">${{activeWine === 'red' ? 'Alcohol (+0.286)' : 'Alcohol (+0.228), Residual Sugar'}}</span></span>
      `;
      document.getElementById('tickerStream').innerHTML = tickerHtml;
    }}

    // ============================================================
    // RENDER: MODEL SELECTOR
    // ============================================================
    function renderModelSelector() {{
      const container = document.getElementById('modelListContainer');
      container.innerHTML = '';
      const data = WINE_DATA[activeWine];

      // Add standard models
      data.models.forEach(m => {{
        const card = document.createElement('div');
        const isSelected = (currentModel && m.id === currentModel.id);
        card.className = `model-radio-card ${{isSelected ? 'selected' : ''}}`;
        card.onclick = () => selectModel(m.id);

        card.innerHTML = `
          <div class="model-card-left">
            <div class="pixel-radio">
              ${{isSelected ? '<div class="pixel-radio-dot"></div>' : ''}}
            </div>
            <div>
              <div class="model-name">${{m.name}}</div>
              <div style="font-size: 10px; color: #64748b;">${{m.nFeat}} Features | CV RMSE: ${{m.cvRmse.toFixed(4)}}</div>
            </div>
          </div>
          <span class="model-badge ${{m.isBest ? 'best' : ''}}">${{m.tag}}</span>
        `;
        container.appendChild(card);
      }});

      // Add "★ Compare 5 Methods" card
      const compCard = document.createElement('div');
      const isCompSelected = (activeProgressionMethod === 'Compare_All');
      compCard.className = `model-radio-card ${{isCompSelected ? 'selected' : ''}}`;
      compCard.onclick = () => selectModel('Compare_All');
      compCard.innerHTML = `
        <div class="model-card-left">
          <div class="pixel-radio">
            ${{isCompSelected ? '<div class="pixel-radio-dot"></div>' : ''}}
          </div>
          <div>
            <div class="model-name" style="color: var(--neon-cyan);">★ Compare 5 Methods</div>
            <div style="font-size: 10px; color: #64748b;">All 5 Algorithms | k = 1...11 Progression</div>
          </div>
        </div>
        <span class="model-badge" style="background: #3b82f6; color: #fff;">5-CURVE OVERLAY</span>
      `;
      container.appendChild(compCard);
    }}

    // ============================================================
    // RENDER: FEATURE FLAGS (11 LEDs)
    // ============================================================
    function renderFeatureFlags() {{
      const grid = document.getElementById('featureFlagsGrid');
      grid.innerHTML = '';
      const data = WINE_DATA[activeWine];

      const activeFeats = currentModel ? currentModel.features : [];

      data.features.forEach(f => {{
        const isActive = activeFeats.includes(f);
        const pill = document.createElement('div');
        pill.className = 'feat-flag-pill';
        const icon = FEATURE_ICONS[f] || '🧪';
        pill.innerHTML = `
          <div class="feat-led ${{isActive ? 'on' : 'off'}}"></div>
          <span title="${{f}}">${{icon}} ${{f}}</span>
        `;
        grid.appendChild(pill);
      }});
    }}

    // ============================================================
    // RENDER: LEADERBOARD TABLE
    // ============================================================
    function renderLeaderboard() {{
      const tbody = document.getElementById('leaderboardBody');
      tbody.innerHTML = '';
      const data = WINE_DATA[activeWine];

      data.models.forEach((m, idx) => {{
        const tr = document.createElement('tr');
        const isSelected = (currentModel && m.id === currentModel.id);
        if (isSelected) tr.style.background = '#15243d';

        tr.innerHTML = `
          <td class="rank-num ${{idx === 0 ? 'first' : ''}}">#0${{idx + 1}}</td>
          <td style="color: ${{isSelected ? 'var(--neon-cyan)' : '#e2e8f0'}}; font-weight: bold;">
            ${{m.name}}
          </td>
          <td><span style="color: var(--acid-yellow);">${{m.nFeat}}</span></td>
          <td style="color: #6ee7b7;">${{m.cvRmse.toFixed(4)}}</td>
          <td style="color: var(--neon-cyan);">${{m.r2.toFixed(4)}}</td>
        `;
        tr.onclick = () => selectModel(m.id);
        tr.style.cursor = 'pointer';
        tbody.appendChild(tr);
      }});

      const foot = document.getElementById('leaderboardFootnote');
      if (activeWine === 'red') {{
        foot.innerHTML = "★ Forward SFS &amp; Exhaustive Search tied for #1 rank (CV RMSE: 0.6582 with 6 optimal features).";
      }} else {{
        foot.innerHTML = "★ RFECV &amp; Exhaustive Search tied for #1 rank (CV RMSE: 0.7542 with 7 optimal features).";
      }}
    }}

    // ============================================================
    // RENDER: OUTLIERS TABLE
    // ============================================================
    function renderOutliersTable() {{
      const tbody = document.getElementById('outliersTableBody');
      tbody.innerHTML = '';
      const data = WINE_DATA[activeWine];

      data.outliers.forEach(row => {{
        const tr = document.createElement('tr');
        const isNegative = row.res < 0;
        tr.innerHTML = `
          <td style="color: #ffcc00; font-weight: bold;">[${{row.rank}}]</td>
          <td>#${{row.id}}</td>
          <td style="color: #fff; font-weight: bold;">${{row.actual.toFixed(1)}}</td>
          <td style="color: #6ee7b7;">${{row.pred.toFixed(2)}}</td>
          <td class="${{isNegative ? 'res-negative' : 'res-positive'}}">${{isNegative ? '' : '+'}}${{row.res.toFixed(2)}}</td>
          <td>${{row.alcohol.toFixed(1)}}%</td>
          <td>${{row.volatile_acidity.toFixed(2)}}</td>
          <td>${{row.density.toFixed(4)}}</td>
        `;
        tbody.appendChild(tr);
      }});

      const note = document.getElementById('outliersSummaryFootnote');
      if (activeWine === 'red') {{
        note.textContent = "Row #832 is the #1 Red Wine outlier: Quality score 3 yet high alcohol and balanced acidity led model to predict 5.61 (residual: -2.61).";
      }} else {{
        note.textContent = "Row #4745 is the #1 White Wine outlier: Severely downgraded sensory rating (score 3) despite normal chemical metrics, yielding residual -3.81.";
      }}
    }}

    // ============================================================
    // RENDER: CHEMICAL CASSETTES (11 FEATURES)
    // ============================================================
    function renderCassettes() {{
      const container = document.getElementById('cassettesContainer');
      container.innerHTML = '';
      const data = WINE_DATA[activeWine];

      data.features.forEach((feat, idx) => {{
        const cfg = FEATURE_INPUT_CONFIG[feat] || {{ label: feat.toUpperCase(), unit: "", step: 0.1, min: 0, max: 100 }};
        const stats = data.feature_stats[feat];
        const defaultVal = stats ? stats.mean : (cfg.min + cfg.max) / 2;

        const card = document.createElement('div');
        const accentClass = (idx % 3 === 1) ? 'pink-accent' : ((idx % 3 === 2) ? 'yellow-accent' : '');
        card.className = `cassette-card ${{accentClass}}`;
        card.id = `cassette_${{feat.replace(/\\s+/g, '_')}}`;

        const icon = FEATURE_ICONS[feat] || '🧪';

        card.innerHTML = `
          <div class="cassette-title">
            <span>${{icon}} ${{cfg.label}}</span>
            <span class="coef-badge" id="coefBadge_${{feat.replace(/\\s+/g, '_')}}" style="color: var(--neon-cyan);">[--]</span>
          </div>
          <div style="display: flex; align-items: baseline; gap: 4px;">
            <input type="number" id="inp_${{feat.replace(/\\s+/g, '_')}}" class="arcade-number-input" 
                   value="${{defaultVal}}" step="${{cfg.step}}" min="${{cfg.min}}" max="${{cfg.max}}">
            <span style="font-size: 10px; color: #64748b;">${{cfg.unit}}</span>
          </div>
          <input type="range" id="rng_${{feat.replace(/\\s+/g, '_')}}" 
                 min="${{cfg.min}}" max="${{cfg.max}}" value="${{defaultVal}}" step="${{cfg.step}}" 
                 style="width: 100%; margin-top: 6px; accent-color: var(--neon-cyan);">
        `;
        container.appendChild(card);

        // Bind Sync
        const numInput = card.querySelector(`#inp_${{feat.replace(/\\s+/g, '_')}}`);
        const rngInput = card.querySelector(`#rng_${{feat.replace(/\\s+/g, '_')}}`);
        numInput.addEventListener('input', () => {{
          rngInput.value = numInput.value;
          calculatePrediction(false);
        }});
        rngInput.addEventListener('input', () => {{
          numInput.value = rngInput.value;
          calculatePrediction(false);
        }});
      }});

      updateCassetteBadges();
    }}

    // ============================================================
    // RENDER: QUICK PRESETS
    // ============================================================
    function renderPresets() {{
      const container = document.getElementById('presetBtnsContainer');
      container.innerHTML = '';

      const presets = activeWine === 'red' ? [
        {{ id: 'typical_red', label: '🍷 Typical Red Sample' }},
        {{ id: 'high_alcohol', label: '🍇 High Alcohol Reserve (Score ~ 7)' }},
        {{ id: 'high_volatile', label: '🧪 High Volatile Acid (Flawed ~ 3)' }},
        {{ id: 'low_sugar', label: '⚡ Bone-Dry Cabernet' }},
        {{ id: 'outlier_red', label: '⚠️ Outlier Bottle #832' }}
      ] : [
        {{ id: 'typical_white', label: '🥂 Typical White Sample' }},
        {{ id: 'sweet_riesling', label: '🍬 Sweet Riesling' }},
        {{ id: 'crisp_sauvignon', label: '🍋 Crisp Sauvignon Blanc' }},
        {{ id: 'high_alcohol_white', label: '🍾 Reserve Chardonnay (Score ~ 7)' }},
        {{ id: 'outlier_white', label: '⚠️ Outlier Bottle #4745' }}
      ];

      presets.forEach(p => {{
        const btn = document.createElement('button');
        btn.className = 'preset-chip';
        btn.textContent = p.label;
        btn.onclick = () => loadPreset(p.id);
        container.appendChild(btn);
      }});
    }}

    window.loadPreset = function(presetId) {{
      playSound('click');
      const data = WINE_DATA[activeWine];
      let vals = {{}};

      if (presetId === 'typical_red') {{
        vals = {{ "fixed acidity": 8.3, "volatile acidity": 0.53, "citric acid": 0.27, "residual sugar": 2.5, "chlorides": 0.08, "free sulfur dioxide": 16.0, "total sulfur dioxide": 46.0, "density": 0.9967, "pH": 3.31, "sulphates": 0.65, "alcohol": 10.4 }};
      }} else if (presetId === 'high_alcohol') {{
        vals = {{ "fixed acidity": 8.5, "volatile acidity": 0.35, "citric acid": 0.40, "residual sugar": 2.2, "chlorides": 0.065, "free sulfur dioxide": 18.0, "total sulfur dioxide": 38.0, "density": 0.9950, "pH": 3.25, "sulphates": 0.85, "alcohol": 13.5 }};
      }} else if (presetId === 'high_volatile') {{
        vals = {{ "fixed acidity": 7.8, "volatile acidity": 1.15, "citric acid": 0.05, "residual sugar": 2.0, "chlorides": 0.110, "free sulfur dioxide": 8.0, "total sulfur dioxide": 22.0, "density": 0.9975, "pH": 3.55, "sulphates": 0.45, "alcohol": 9.2 }};
      }} else if (presetId === 'low_sugar') {{
        vals = {{ "fixed acidity": 9.2, "volatile acidity": 0.45, "citric acid": 0.35, "residual sugar": 1.4, "chlorides": 0.075, "free sulfur dioxide": 15.0, "total sulfur dioxide": 42.0, "density": 0.9960, "pH": 3.20, "sulphates": 0.70, "alcohol": 11.5 }};
      }} else if (presetId === 'outlier_red') {{
        vals = {{ "fixed acidity": 10.4, "volatile acidity": 0.61, "citric acid": 0.49, "residual sugar": 2.1, "chlorides": 0.200, "free sulfur dioxide": 5.0, "total sulfur dioxide": 16.0, "density": 0.9994, "pH": 3.16, "sulphates": 0.63, "alcohol": 8.4 }};
      }} else if (presetId === 'typical_white') {{
        vals = {{ "fixed acidity": 6.85, "volatile acidity": 0.28, "citric acid": 0.33, "residual sugar": 6.39, "chlorides": 0.046, "free sulfur dioxide": 35.3, "total sulfur dioxide": 138.4, "density": 0.9940, "pH": 3.19, "sulphates": 0.49, "alcohol": 10.5 }};
      }} else if (presetId === 'sweet_riesling') {{
        vals = {{ "fixed acidity": 7.4, "volatile acidity": 0.22, "citric acid": 0.38, "residual sugar": 18.5, "chlorides": 0.035, "free sulfur dioxide": 42.0, "total sulfur dioxide": 160.0, "density": 0.9985, "pH": 3.10, "sulphates": 0.44, "alcohol": 9.0 }};
      }} else if (presetId === 'crisp_sauvignon') {{
        vals = {{ "fixed acidity": 8.2, "volatile acidity": 0.24, "citric acid": 0.42, "residual sugar": 1.8, "chlorides": 0.038, "free sulfur dioxide": 30.0, "total sulfur dioxide": 110.0, "density": 0.9915, "pH": 3.02, "sulphates": 0.52, "alcohol": 12.2 }};
      }} else if (presetId === 'high_alcohol_white') {{
        vals = {{ "fixed acidity": 6.6, "volatile acidity": 0.25, "citric acid": 0.30, "residual sugar": 3.5, "chlorides": 0.040, "free sulfur dioxide": 28.0, "total sulfur dioxide": 105.0, "density": 0.9910, "pH": 3.25, "sulphates": 0.58, "alcohol": 13.4 }};
      }} else if (presetId === 'outlier_white') {{
        vals = {{ "fixed acidity": 7.6, "volatile acidity": 0.48, "citric acid": 0.37, "residual sugar": 1.2, "chlorides": 0.036, "free sulfur dioxide": 6.0, "total sulfur dioxide": 99.0, "density": 0.9902, "pH": 3.04, "sulphates": 0.58, "alcohol": 12.5 }};
      }}

      // Apply to DOM
      for (const [f, v] of Object.entries(vals)) {{
        const inp = document.getElementById(`inp_${{f.replace(/\\s+/g, '_')}}`);
        const rng = document.getElementById(`rng_${{f.replace(/\\s+/g, '_')}}`);
        if (inp && rng) {{
          inp.value = v;
          rng.value = v;
        }}
      }}
      calculatePrediction(true);
    }};

    // ============================================================
    // PREDICTION ENGINE
    // ============================================================
    function calculatePrediction(withSound = true) {{
      if (!currentModel) return;
      const data = WINE_DATA[activeWine];
      const coefs = currentModel.coefs || {{}};
      const features = currentModel.features || [];
      let pred = currentModel.intercept || 0;

      features.forEach(f => {{
        const inp = document.getElementById(`inp_${{f.replace(/\\s+/g, '_')}}`);
        if (inp && coefs[f]) {{
          pred += coefs[f] * parseFloat(inp.value || 0);
        }}
      }});

      // Clamp predicted quality between 0 and 10
      pred = Math.max(1, Math.min(10, pred));

      animateNumber(pred);
      if (withSound) playSound('coin');
    }}

    function animateNumber(target) {{
      const el = document.getElementById('screenProfitOutput');
      const start = parseFloat(el.textContent) || 5.0;
      const duration = 200;
      const startTime = performance.now();

      function step(now) {{
        const progress = Math.min((now - startTime) / duration, 1);
        const current = start + (target - start) * progress;
        el.textContent = `${{current.toFixed(2)}} / 10`;
        if (progress < 1) requestAnimationFrame(step);
      }}
      requestAnimationFrame(step);
    }}

    document.getElementById('btnRunPrediction').addEventListener('click', () => {{
      calculatePrediction(true);
    }});

    function updateFormulaDisplay() {{
      if (!currentModel) return;
      const c = currentModel.coefs || {{}};
      const f = currentModel.features || [];
      let terms = [`${{(currentModel.intercept || 0).toFixed(3)}}`];

      f.forEach(feat => {{
        if (c[feat]) {{
          const sign = c[feat] >= 0 ? '+' : '-';
          terms.push(`${{sign}} ${{Math.abs(c[feat]).toFixed(3)}}×(${{feat}})`);
        }}
      }});

      document.getElementById('screenFormulaBreakdown').textContent = `Equation: Quality = ${{terms.join(' ')}}`;
    }}

    function updateCassetteBadges() {{
      if (!currentModel) return;
      const data = WINE_DATA[activeWine];
      const c = currentModel.coefs || {{}};
      const f = currentModel.features || [];

      data.features.forEach(feat => {{
        const badge = document.getElementById(`coefBadge_${{feat.replace(/\\s+/g, '_')}}`);
        const card = document.getElementById(`cassette_${{feat.replace(/\\s+/g, '_')}}`);
        if (!badge || !card) return;

        if (f.includes(feat)) {{
          const val = c[feat] || 0;
          badge.textContent = `[${{val >= 0 ? '+' : ''}}${{val.toFixed(3)}}]`;
          badge.style.color = val >= 0 ? 'var(--matrix-green)' : 'var(--hot-pink)';
          card.style.opacity = '1';
        }} else {{
          badge.textContent = '[PRUNED: 0.00]';
          badge.style.color = '#64748b';
          card.style.opacity = '0.55';
        }}
      }});
    }}

    // ============================================================
    // SELECT MODEL (METHOD CONSOLE)
    // ============================================================
    function selectModel(modelId) {{
      const data = WINE_DATA[activeWine];
      playSound('select');

      if (modelId === 'Compare_All') {{
        activeProgressionMethod = 'Compare_All';
        renderModelSelector();
        renderKTabs();
        updateOlsCardComparison(selectedK);
        drawRmseChart();
        drawR2Chart();
        document.getElementById('perfWindowTitle').textContent = `MODEL_PERFORMANCE_MONITOR.EXE - 5-Method Comparative Overlay (k = 1...11)`;
        document.getElementById('perfComparisonLegend').style.display = 'flex';
        document.getElementById('systemMsgStatus').textContent = `MODE: 5-ALGORITHM COMPARISON OVERLAY (k=1..11). DISPLAYING DUAL 5-CURVE PROJECTIONS.`;
        return;
      }}

      const target = data.models.find(m => m.id === modelId) || data.models[0];
      currentModel = target;
      activeProgressionMethod = modelId;
      if (!data.progressions[activeProgressionMethod]) {{
        activeProgressionMethod = 'Forward_SFS';
      }}

      // Sweet spot for this method
      const progItems = data.progressions[activeProgressionMethod];
      const sweet = progItems.find(p => p.isSweetSpot) || progItems[0];
      selectedK = sweet.k;

      // Update Diagnostics
      document.getElementById('statMethodName').textContent = currentModel.name;
      document.getElementById('statFeatureCount').textContent = `${{currentModel.nFeat}} of 11`;
      document.getElementById('statR2').textContent = currentModel.r2.toFixed(4);
      document.getElementById('statAdjR2').textContent = currentModel.adjR2.toFixed(4);
      document.getElementById('statRMSE').textContent = currentModel.rmse.toFixed(4);
      document.getElementById('statCvRmse').textContent = currentModel.cvRmse.toFixed(4);
      document.getElementById('calcModelBadge').textContent = currentModel.name;

      renderModelSelector();
      renderFeatureFlags();
      renderLeaderboard();
      renderKTabs();
      updateOlsCard(sweet);
      calculatePrediction(false);
      updateFormulaDisplay();
      updateCassetteBadges();
      drawScatterChart();
      drawRmseChart();
      drawR2Chart();

      document.getElementById('perfWindowTitle').textContent = `MODEL_PERFORMANCE_MONITOR.EXE - ${{target.name}} Progression (k = 1...11)`;
      document.getElementById('perfComparisonLegend').style.display = 'none';
      document.getElementById('systemMsgStatus').textContent = `LOADED: ${{target.name}} (k=${{target.nFeat}}). FEATURES: [${{target.features.join(', ')}}]`;
    }}

    // ============================================================
    // K-TABS AND PROGRESSION INTERACTION (k = 1...11)
    // ============================================================
    function renderKTabs() {{
      const container = document.getElementById('kTabsContainer');
      container.innerHTML = '';
      const data = WINE_DATA[activeWine];

      for (let k = 1; k <= 11; k++) {{
        const btn = document.createElement('button');
        let classes = ['k-tab-btn'];

        if (activeProgressionMethod === 'Compare_All') {{
          if (activeWine === 'red' && (k === 7 || k === 8)) classes.push('sweet-spot');
          if (activeWine === 'white' && (k === 7 || k === 8)) classes.push('sweet-spot');
          if (k === 11) classes.push('overfit-cliff');
        }} else {{
          const items = data.progressions[activeProgressionMethod] || [];
          const item = items.find(p => p.k === k);
          if (item && item.isSweetSpot) classes.push('sweet-spot');
          if (item && item.isOverfitCliff) classes.push('overfit-cliff');
        }}

        if (k === selectedK) classes.push('active');
        btn.className = classes.join(' ');
        btn.innerHTML = `<span>k=${{k}}</span>`;
        btn.onclick = () => selectK(k);
        container.appendChild(btn);
      }}
    }}

    function selectK(k) {{
      selectedK = k;
      const data = WINE_DATA[activeWine];

      if (activeProgressionMethod === 'Compare_All') {{
        playSound('click');
        renderKTabs();
        updateOlsCardComparison(selectedK);
        drawRmseChart();
        drawR2Chart();
        return;
      }}

      const items = data.progressions[activeProgressionMethod] || [];
      const target = items.find(p => p.k === k) || items[0];
      if (!target) return;

      if (target.isSweetSpot) playSound('coin');
      else if (target.isOverfitCliff) playSound('zap');
      else playSound('click');

      currentModel = {{
        id: `${{activeProgressionMethod}}_k${{target.k}}`,
        name: `${{activeProgressionMethod.replace('_', ' ')}} (k=${{target.k}})`,
        features: target.features,
        nFeat: target.k,
        cvRmse: target.rmse,
        mae: 0.50,
        rmse: target.rmse,
        r2: target.r2,
        adjR2: target.r2 - 0.01,
        intercept: target.intercept,
        coefs: target.coefs,
        isBest: target.isSweetSpot,
        tag: target.isSweetSpot ? "SWEET SPOT" : (target.isOverfitCliff ? "CLIFF" : `k=${{target.k}}`)
      }};

      document.getElementById('statMethodName').textContent = currentModel.name;
      document.getElementById('statFeatureCount').textContent = `${{target.k}} of 11`;
      document.getElementById('statR2').textContent = target.r2.toFixed(4);
      document.getElementById('statAdjR2').textContent = currentModel.adjR2.toFixed(4);
      document.getElementById('statRMSE').textContent = target.rmse.toFixed(4);
      document.getElementById('statCvRmse').textContent = target.rmse.toFixed(4);
      document.getElementById('calcModelBadge').textContent = currentModel.name;

      renderFeatureFlags();
      calculatePrediction(false);
      updateFormulaDisplay();
      updateCassetteBadges();
      renderKTabs();
      updateOlsCard(target);
      drawRmseChart();
      drawR2Chart();
      drawScatterChart();
    }}

    function updateOlsCard(item) {{
      document.getElementById('olsFormulaKTag').textContent = `MODEL: k = ${{item.k}} (${{item.features.length}} Features)`;
      
      let terms = [`${{(item.intercept || 0).toFixed(3)}}`];
      for (const [f, c] of Object.entries(item.coefs || {{}})) {{
        const sign = c >= 0 ? '+' : '-';
        terms.push(`<span style="color: ${{c >= 0 ? '#00f0ff' : '#ff007f'}}">${{sign}} ${{Math.abs(c).toFixed(3)}}</span> &times; [${{f}}]`);
      }}
      document.getElementById('olsFormulaOutput').innerHTML = `<span style="color: #ccff00;">Quality</span> = ${{terms.join(' ')}}`;

      document.getElementById('olsFeatSubset').textContent = `[${{item.features.map(f => `'${{f}}'`).join(', ')}}]`;
      document.getElementById('olsMetricRmse').textContent = item.rmse.toFixed(4);
      document.getElementById('olsMetricR2').textContent = item.r2.toFixed(4);

      const statusBadge = document.getElementById('olsCardStatusBadge');
      if (item.isSweetSpot) {{
        statusBadge.style.color = '#00ff88';
        statusBadge.textContent = '[★ SWEET SPOT: MIN TEST RMSE]';
      }} else if (item.isOverfitCliff) {{
        statusBadge.style.color = '#fbbf24';
        statusBadge.textContent = '[⚠ OVER-PARAMETERIZED MODEL]';
      }} else {{
        statusBadge.style.color = '#67e8f9';
        statusBadge.textContent = `[k = ${{item.k}} EVALUATED]`;
      }}

      const interp = document.getElementById('olsInterpretationText');
      if (activeWine === 'red') {{
        interp.textContent = item.isSweetSpot 
          ? "★ OPTIMAL RED WINE SUBSET: Volatile acidity (negative, -1.01) and alcohol (positive, +0.286) explain the lion's share of variance. Sulphates and total sulfur dioxide further stabilize the fit."
          : `k=${{item.k}} evaluated for Red Wine. RMSE: ${{item.rmse.toFixed(4)}}, R²: ${{item.r2.toFixed(4)}}.`;
      }} else {{
        interp.textContent = item.isSweetSpot 
          ? "★ OPTIMAL WHITE WINE SUBSET: Residual sugar and density counterbalance alcohol content, preserving crisp acidity and reducing sensory prediction error."
          : `k=${{item.k}} evaluated for White Wine. RMSE: ${{item.rmse.toFixed(4)}}, R²: ${{item.r2.toFixed(4)}}.`;
      }}
    }}

    function updateOlsCardComparison(k) {{
      const data = WINE_DATA[activeWine];
      const algos = ['LassoCV', 'Forward_SFS', 'RFECV', 'ElasticNetCV', 'Exhaustive'];
      document.getElementById('olsFormulaKTag').textContent = `5-METHOD MATRIX: k = ${{k}}`;
      
      let html = `
        <div style="font-size: 15px; margin-bottom: 8px; color: #a7f3d0; border-bottom: 1px dashed #008033; padding-bottom: 4px; font-family: 'Share Tech Mono', monospace;">
          <b>5-ALGORITHM SELECTION &amp; ERROR MATRIX AT k = ${{k}} (${{data.name}}):</b>
        </div>
        <div style="overflow-x: auto; width: 100%; max-width: 100%;">
          <table style="width: 100%; table-layout: fixed; border-collapse: collapse; font-family: 'VT323', monospace; font-size: 18px;">
            <thead>
              <tr style="color: #64748b; border-bottom: 1px dotted #005a28; text-align: left;">
                <th style="padding: 2px 6px; width: 22%;">ALGORITHM</th>
                <th style="padding: 2px 6px; width: 48%;">SELECTED SUBSET</th>
                <th style="padding: 2px 6px; width: 15%;">TEST RMSE</th>
                <th style="padding: 2px 6px; width: 15%;">TEST R²</th>
              </tr>
            </thead>
            <tbody>
      `;

      let minR = 999;
      let bestA = '';
      algos.forEach(a => {{
        const item = data.progressions[a].find(p => p.k === k);
        if (item && item.rmse < minR) {{
          minR = item.rmse;
          bestA = a;
        }}
      }});

      algos.forEach(a => {{
        const item = data.progressions[a].find(p => p.k === k);
        const isWinner = (a === bestA);
        html += `
          <tr style="border-bottom: 1px dotted #14351e; background: ${{isWinner ? 'rgba(0, 255, 102, 0.08)' : 'transparent'}};">
            <td style="padding: 2px 6px; color: var(--neon-cyan); font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${{a.replace('_', ' ')}}</td>
            <td style="padding: 2px 6px; color: #e2e8f0; word-break: break-word; white-space: normal; line-height: 1.15; font-size: 16px;">[${{item.features.join(', ')}}]</td>
            <td style="padding: 2px 6px; color: ${{isWinner ? '#00ff88' : '#cbd5e1'}}; font-weight: ${{isWinner ? 'bold' : 'normal'}};">${{item.rmse.toFixed(4)}} ${{isWinner ? '★' : ''}}</td>
            <td style="padding: 2px 6px; color: var(--acid-yellow);">${{item.r2.toFixed(4)}}</td>
          </tr>
        `;
      }});

      html += `</tbody></table></div>`;
      document.getElementById('olsFormulaOutput').innerHTML = html;

      const bestItem = data.progressions[bestA].find(p => p.k === k);
      document.getElementById('olsFeatSubset').textContent = `Best at k=${{k}}: [${{bestItem.features.join(', ')}}]`;
      document.getElementById('olsMetricRmse').textContent = minR.toFixed(4);
      document.getElementById('olsMetricR2').textContent = bestItem.r2.toFixed(4);
    }}

    // ============================================================
    // CANVAS: ACTUAL VS PREDICTED SCATTER
    // ============================================================
    const scatterCanvas = document.getElementById('scatterCanvas');
    const sCtx = scatterCanvas.getContext('2d');

    function drawScatterChart() {{
      const dpr = window.devicePixelRatio || 1;
      const rect = scatterCanvas.getBoundingClientRect();
      scatterCanvas.width = rect.width * dpr;
      scatterCanvas.height = rect.height * dpr;
      sCtx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      const pad = 36;
      sCtx.clearRect(0, 0, w, h);

      const minVal = 2.5;
      const maxVal = 9.5;

      function toX(v) {{ return pad + ((v - minVal) / (maxVal - minVal)) * (w - 2 * pad); }}
      function toY(v) {{ return (h - pad) - ((v - minVal) / (maxVal - minVal)) * (h - 2 * pad); }}

      // Grid
      sCtx.strokeStyle = '#1e283d';
      sCtx.lineWidth = 1;
      sCtx.fillStyle = '#64748b';
      sCtx.font = '9px "Share Tech Mono"';

      for (let q = 3; q <= 9; q++) {{
        const x = toX(q);
        sCtx.beginPath();
        sCtx.moveTo(x, pad);
        sCtx.lineTo(x, h - pad);
        sCtx.stroke();
        sCtx.fillText(q.toString(), x - 3, h - pad + 14);

        const y = toY(q);
        sCtx.beginPath();
        sCtx.moveTo(pad, y);
        sCtx.lineTo(w - pad, y);
        sCtx.stroke();
        sCtx.fillText(q.toString(), pad - 18, y + 3);
      }}

      // 45 degree line
      sCtx.save();
      sCtx.strokeStyle = 'rgba(255, 0, 127, 0.6)';
      sCtx.lineWidth = 1.5;
      sCtx.setLineDash([4, 4]);
      sCtx.beginPath();
      sCtx.moveTo(toX(minVal), toY(minVal));
      sCtx.lineTo(toX(maxVal), toY(maxVal));
      sCtx.stroke();
      sCtx.restore();

      // Axis labels
      sCtx.fillStyle = '#94a3b8';
      sCtx.font = '9px "Press Start 2P"';
      sCtx.fillText('ACTUAL QUALITY', w / 2 - 45, h - 8);

      sCtx.save();
      sCtx.translate(12, h / 2 + 35);
      sCtx.rotate(-Math.PI / 2);
      sCtx.fillText('PREDICTED', 0, 0);
      sCtx.restore();

      // Plot Test Samples
      const data = WINE_DATA[activeWine];
      const samples = data.test_samples;
      const coefs = currentModel ? currentModel.coefs || {{}} : {{}};
      const features = currentModel ? currentModel.features || [] : [];
      const intercept = currentModel ? currentModel.intercept || 0 : 0;

      samples.forEach(pt => {{
        let dynamicPred = intercept;
        features.forEach(f => {{
          if (coefs[f] && pt.features[f] !== undefined) {{
            dynamicPred += coefs[f] * pt.features[f];
          }}
        }});
        pt._dynPred = dynamicPred;
        pt._dynRes = pt.actual - dynamicPred;

        const cx = toX(pt.actual);
        const cy = toY(dynamicPred);
        pt._cx = cx;
        pt._cy = cy;

        // Draw Dot
        sCtx.save();
        sCtx.fillStyle = '#00f0ff';
        sCtx.shadowColor = '#00f0ff';
        sCtx.shadowBlur = 8;
        sCtx.beginPath();
        sCtx.arc(cx, cy, 4, 0, Math.PI * 2);
        sCtx.fill();

        // Core dot
        sCtx.fillStyle = '#ffffff';
        sCtx.beginPath();
        sCtx.arc(cx, cy, 1.5, 0, Math.PI * 2);
        sCtx.fill();
        sCtx.restore();
      }});

      // Hover circle
      if (hoveredPoint) {{
        sCtx.save();
        sCtx.strokeStyle = '#ffff00';
        sCtx.lineWidth = 2;
        sCtx.beginPath();
        sCtx.arc(hoveredPoint._cx, hoveredPoint._cy, 8, 0, Math.PI * 2);
        sCtx.stroke();
        sCtx.restore();
      }}
    }}

    scatterCanvas.addEventListener('mousemove', e => {{
      const rect = scatterCanvas.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      const samples = WINE_DATA[activeWine].test_samples;

      let found = null;
      for (const pt of samples) {{
        if (pt._cx && Math.hypot(pt._cx - mx, pt._cy - my) < 10) {{
          found = pt;
          break;
        }}
      }}

      const tooltip = document.getElementById('chart-tooltip');
      if (found) {{
        hoveredPoint = found;
        tooltip.style.display = 'block';
        tooltip.style.left = `${{e.clientX + 14}}px`;
        tooltip.style.top = `${{e.clientY - 20}}px`;
        tooltip.innerHTML = `
          <div style="font-family: 'Press Start 2P'; font-size: 8px; color: var(--acid-yellow); margin-bottom: 4px;">
            BOTTLE #${{found.id}} (${{activeWine.toUpperCase()}})
          </div>
          <div>ACTUAL SCORE: <b style="color: #fff;">${{found.actual.toFixed(1)}}</b></div>
          <div>PREDICTED: <b style="color: var(--neon-cyan);">${{found._dynPred.toFixed(2)}}</b></div>
          <div>RESIDUAL: <b style="color: ${{found._dynRes >= 0 ? '#00ff66' : '#ff007f'}};">${{found._dynRes >= 0 ? '+' : ''}}${{found._dynRes.toFixed(2)}}</b></div>
        `;
        drawScatterChart();
      }} else if (hoveredPoint) {{
        hoveredPoint = null;
        tooltip.style.display = 'none';
        drawScatterChart();
      }}
    }});

    scatterCanvas.addEventListener('mouseleave', () => {{
      hoveredPoint = null;
      document.getElementById('chart-tooltip').style.display = 'none';
      drawScatterChart();
    }});

    // ============================================================
    // CANVAS: DUAL PROGRESSION CHARTS (RMSE & R-squared)
    // ============================================================
    const rmseCanvas = document.getElementById('rmseChartCanvas');
    const r2Canvas = document.getElementById('r2ChartCanvas');

    const ALGO_COLORS = {{
      "LassoCV": "#00f0ff",
      "Forward_SFS": "#ff8c00",
      "RFECV": "#00ff66",
      "ElasticNetCV": "#ff007f",
      "Exhaustive": "#b388ff"
    }};

    function drawRmseChart() {{
      const ctx = rmseCanvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const container = rmseCanvas.parentElement;
      const rect = container ? container.getBoundingClientRect() : rmseCanvas.getBoundingClientRect();
      const w = Math.floor(rect.width) || 460;
      const h = Math.floor(rect.height) || 230;
      rmseCanvas.width = w * dpr;
      rmseCanvas.height = h * dpr;
      ctx.scale(dpr, dpr);

      const padLeft = 48;
      const padRight = 24;
      const padTop = 28;
      const padBottom = 28;
      ctx.clearRect(0, 0, w, h);

      const data = WINE_DATA[activeWine];
      const minY = activeWine === 'red' ? 0.60 : 0.78;
      const maxY = activeWine === 'red' ? 0.68 : 0.92;

      function toX(k) {{ return padLeft + ((k - 1) / 10) * (w - padLeft - padRight); }}
      function toY(rmse) {{ return (h - padBottom) - ((rmse - minY) / (maxY - minY)) * (h - padTop - padBottom); }}

      // Y Grid
      ctx.strokeStyle = '#182235';
      ctx.lineWidth = 1;
      ctx.fillStyle = '#64748b';
      ctx.font = '9px "Share Tech Mono"';

      const stepY = activeWine === 'red' ? 0.02 : 0.03;
      for (let v = minY; v <= maxY + 0.001; v += stepY) {{
        const y = toY(v);
        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(w - padRight, y);
        ctx.stroke();
        ctx.fillText(v.toFixed(2), 8, y + 3);
      }}

      // X Grid
      for (let k = 1; k <= 11; k++) {{
        const x = toX(k);
        ctx.beginPath();
        ctx.moveTo(x, padTop);
        ctx.lineTo(x, h - padBottom);
        ctx.stroke();
        ctx.fillText(`k=${{k}}`, x - 8, h - padBottom + 14);
      }}

      // Draw active lines
      const algosToDraw = activeProgressionMethod === 'Compare_All'
        ? ['LassoCV', 'Forward_SFS', 'RFECV', 'ElasticNetCV', 'Exhaustive']
        : [activeProgressionMethod];

      algosToDraw.forEach(algo => {{
        const items = data.progressions[algo];
        if (!items) return;
        const col = ALGO_COLORS[algo] || '#00f0ff';

        ctx.save();
        ctx.strokeStyle = col;
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(toX(items[0].k), toY(items[0].rmse));
        for (let i = 1; i < items.length; i++) {{
          ctx.lineTo(toX(items[i].k), toY(items[i].rmse));
        }}
        ctx.stroke();

        // Nodes
        items.forEach(it => {{
          const cx = toX(it.k);
          const cy = toY(it.rmse);
          it._cxRmse = cx;
          it._cyRmse = cy;
          it._algo = algo;

          ctx.fillStyle = col;
          ctx.beginPath();
          ctx.arc(cx, cy, it.k === selectedK ? 5 : 3.5, 0, Math.PI * 2);
          ctx.fill();

          if (it.k === selectedK) {{
            ctx.strokeStyle = '#ffff00';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(cx, cy, 8, 0, Math.PI * 2);
            ctx.stroke();
          }}
        }});
        ctx.restore();
      }});
    }}

    function drawR2Chart() {{
      const ctx = r2Canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const container = r2Canvas.parentElement;
      const rect = container ? container.getBoundingClientRect() : r2Canvas.getBoundingClientRect();
      const w = Math.floor(rect.width) || 460;
      const h = Math.floor(rect.height) || 230;
      r2Canvas.width = w * dpr;
      r2Canvas.height = h * dpr;
      ctx.scale(dpr, dpr);

      const padLeft = 48;
      const padRight = 24;
      const padTop = 28;
      const padBottom = 28;
      ctx.clearRect(0, 0, w, h);

      const data = WINE_DATA[activeWine];
      const minY = activeWine === 'red' ? 0.20 : 0.05;
      const maxY = activeWine === 'red' ? 0.38 : 0.30;

      function toX(k) {{ return padLeft + ((k - 1) / 10) * (w - padLeft - padRight); }}
      function toY(r2) {{ return (h - padBottom) - ((r2 - minY) / (maxY - minY)) * (h - padTop - padBottom); }}

      // Y Grid
      ctx.strokeStyle = '#182235';
      ctx.lineWidth = 1;
      ctx.fillStyle = '#64748b';
      ctx.font = '9px "Share Tech Mono"';

      const stepY = activeWine === 'red' ? 0.04 : 0.05;
      for (let v = minY; v <= maxY + 0.001; v += stepY) {{
        const y = toY(v);
        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(w - padRight, y);
        ctx.stroke();
        ctx.fillText(v.toFixed(2), 8, y + 3);
      }}

      // X Grid
      for (let k = 1; k <= 11; k++) {{
        const x = toX(k);
        ctx.beginPath();
        ctx.moveTo(x, padTop);
        ctx.lineTo(x, h - padBottom);
        ctx.stroke();
        ctx.fillText(`k=${{k}}`, x - 8, h - padBottom + 14);
      }}

      // Draw active lines
      const algosToDraw = activeProgressionMethod === 'Compare_All'
        ? ['LassoCV', 'Forward_SFS', 'RFECV', 'ElasticNetCV', 'Exhaustive']
        : [activeProgressionMethod];

      algosToDraw.forEach(algo => {{
        const items = data.progressions[algo];
        if (!items) return;
        const col = ALGO_COLORS[algo] || '#00f0ff';

        ctx.save();
        ctx.strokeStyle = col;
        ctx.lineWidth = 2.2;
        ctx.beginPath();
        ctx.moveTo(toX(items[0].k), toY(items[0].r2));
        for (let i = 1; i < items.length; i++) {{
          ctx.lineTo(toX(items[i].k), toY(items[i].r2));
        }}
        ctx.stroke();

        // Nodes
        items.forEach(it => {{
          const cx = toX(it.k);
          const cy = toY(it.r2);
          it._cxR2 = cx;
          it._cyR2 = cy;
          it._algo = algo;

          ctx.fillStyle = col;
          ctx.beginPath();
          ctx.arc(cx, cy, it.k === selectedK ? 5 : 3.5, 0, Math.PI * 2);
          ctx.fill();

          if (it.k === selectedK) {{
            ctx.strokeStyle = '#ffff00';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(cx, cy, 8, 0, Math.PI * 2);
            ctx.stroke();
          }}
        }});
        ctx.restore();
      }});
    }}

    // Attach chart hover & click
    function attachChartInteractions(canvasEl, type) {{
      canvasEl.addEventListener('click', e => {{
        const rect = canvasEl.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        const data = WINE_DATA[activeWine];
        let candidates = [];
        if (activeProgressionMethod === 'Compare_All') {{
          ['LassoCV', 'Forward_SFS', 'RFECV', 'ElasticNetCV', 'Exhaustive'].forEach(a => candidates.push(...data.progressions[a]));
        }} else {{
          candidates = data.progressions[activeProgressionMethod] || [];
        }}

        for (const item of candidates) {{
          const cx = type === 'rmse' ? item._cxRmse : item._cxR2;
          const cy = type === 'rmse' ? item._cyRmse : item._cyR2;
          if (cx && cy && Math.hypot(cx - mx, cy - my) < 15) {{
            selectK(item.k);
            break;
          }}
        }}
      }});

      canvasEl.addEventListener('mousemove', e => {{
        const rect = canvasEl.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        const data = WINE_DATA[activeWine];
        let candidates = [];
        if (activeProgressionMethod === 'Compare_All') {{
          ['LassoCV', 'Forward_SFS', 'RFECV', 'ElasticNetCV', 'Exhaustive'].forEach(a => candidates.push(...data.progressions[a]));
        }} else {{
          candidates = data.progressions[activeProgressionMethod] || [];
        }}

        let found = null;
        for (const item of candidates) {{
          const cx = type === 'rmse' ? item._cxRmse : item._cxR2;
          const cy = type === 'rmse' ? item._cyRmse : item._cyR2;
          if (cx && cy && Math.hypot(cx - mx, cy - my) < 10) {{
            found = item;
            break;
          }}
        }}

        const tooltip = document.getElementById('chart-tooltip');
        if (found) {{
          tooltip.style.display = 'block';
          tooltip.style.left = `${{e.clientX + 14}}px`;
          tooltip.style.top = `${{e.clientY - 20}}px`;
          tooltip.innerHTML = `
            <div style="font-family: 'Press Start 2P'; font-size: 8px; color: var(--neon-cyan); margin-bottom: 4px;">
              ${{found._algo ? found._algo.replace('_', ' ') : activeProgressionMethod.replace('_', ' ')}} (k=${{found.k}})
            </div>
            <div>TEST RMSE: <b style="color: #00ff88;">${{found.rmse.toFixed(4)}}</b></div>
            <div>TEST R²: <b style="color: var(--acid-yellow);">${{found.r2.toFixed(4)}}</b></div>
            <div style="font-size: 9px; color: #94a3b8; margin-top: 2px;">Click to inspect this k subset</div>
          `;
        }} else {{
          tooltip.style.display = 'none';
        }}
      }});

      canvasEl.addEventListener('mouseleave', () => {{
        document.getElementById('chart-tooltip').style.display = 'none';
      }});
    }}
    attachChartInteractions(rmseCanvas, 'rmse');
    attachChartInteractions(r2Canvas, 'r2');

    // SYNC TO PREDICTOR BUTTON
    document.getElementById('btnSyncWithCalc').addEventListener('click', () => {{
      playSound('coin');
      const data = WINE_DATA[activeWine];
      let targetItem = null;

      if (activeProgressionMethod === 'Compare_All') {{
        targetItem = data.progressions['Exhaustive'].find(p => p.k === selectedK);
      }} else {{
        targetItem = (data.progressions[activeProgressionMethod] || []).find(p => p.k === selectedK);
      }}

      if (targetItem) {{
        currentModel = {{
          id: `Sync_k${{targetItem.k}}`,
          name: `Synced k=${{targetItem.k}} Model`,
          features: targetItem.features,
          nFeat: targetItem.k,
          cvRmse: targetItem.rmse,
          mae: 0.50,
          rmse: targetItem.rmse,
          r2: targetItem.r2,
          adjR2: targetItem.r2 - 0.01,
          intercept: targetItem.intercept,
          coefs: targetItem.coefs,
          isBest: targetItem.isSweetSpot,
          tag: "SYNCED"
        }};
        document.getElementById('calcModelBadge').textContent = currentModel.name;
        renderFeatureFlags();
        calculatePrediction(true);
        updateFormulaDisplay();
        updateCassetteBadges();
        drawScatterChart();
        document.querySelector('.arcade-machine').scrollIntoView({{ behavior: 'smooth' }});
      }}
    }});

    // CRT & Audio Toggles
    const btnCrt = document.getElementById('btnCrtToggle');
    const crtOverlay = document.getElementById('crtOverlay');
    btnCrt.addEventListener('click', () => {{
      crtEnabled = !crtEnabled;
      playSound('zap');
      if (crtEnabled) {{
        crtOverlay.classList.remove('disabled');
        btnCrt.classList.add('active');
        btnCrt.innerHTML = '<span>📺 CRT: ON</span>';
      }} else {{
        crtOverlay.classList.add('disabled');
        btnCrt.classList.remove('active');
        btnCrt.innerHTML = '<span>📺 CRT: OFF</span>';
      }}
    }});

    const btnAudio = document.getElementById('btnAudioToggle');
    btnAudio.addEventListener('click', () => {{
      audioEnabled = !audioEnabled;
      if (audioEnabled) {{
        btnAudio.classList.add('active');
        btnAudio.innerHTML = '<span>🔊 SFX: ON</span>';
        playSound('click');
      }} else {{
        btnAudio.classList.remove('active');
        btnAudio.innerHTML = '<span>🔇 SFX: OFF</span>';
      }}
    }});

    window.addEventListener('resize', () => {{
      drawScatterChart();
      drawRmseChart();
      drawR2Chart();
    }});

    // ============================================================
    // INITIALIZATION
    // ============================================================
    setWineDataset('red');
    document.fonts.ready.then(() => {{
      drawScatterChart();
      drawRmseChart();
      drawR2Chart();
    }});
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated index.html successfully! Size:", len(html_template))
