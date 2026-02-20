# Integrating the Plugin Guide into Vynotes (Glitch)

Your Vynotes frontend lives at **remix-of-remix-of-storymaker-studi** on Glitch. To make the AI layer use Manim plugins correctly, inject the plugin guide into the AI's context.

---

## Where to Add It

1. **Open your Glitch project** → remix-of-remix-of-storymaker-studi
2. **Find where the AI prompt is built** — look for:
   - A file that calls OpenAI/Anthropic/Claude API
   - A `system` or `systemPrompt` variable
   - Serverless functions (e.g. `server/` or `api/`)
   - Environment variables or config for prompts

3. **Inject the guide** — either:
   - **Option A:** Append the contents of `VYNOTES_AI_PLUGIN_GUIDE.md` to the system prompt
   - **Option B:** Add a short instruction + load `plugins-reference.json` and include a summary in the prompt

---

## Option A: Append to System Prompt (Simplest)

Find your system prompt (e.g. in `server.js`, `api/generate.js`, or similar) and add:

```javascript
const PLUGIN_GUIDE = `
When generating Manim code from study notes, use these plugins when content matches:
- Astronomy/space → manim-Astronomy (renderer: opengl)
- Circuits → manim-eng
- Neural networks/ML → ManimML (renderer: opengl)
- Physics → manim-physics
- Stock/finance → manim-stock-visualization
- Timeline → manim-timeline
- CAD/dimensions → manim-CAD_Drawing_Utils
- Meshes → manim-meshes (renderer: opengl)
- Voiceover → manim-voiceover-plus
Default renderer: cairo. Use opengl for 3D plugins.
`;

const systemPrompt = `You are an expert at generating Manim animations from study notes. ${PLUGIN_GUIDE} ...`;
```

---

## Option B: Two-Phase Flow (More Robust)

1. **Phase 1 — Classify:** Ask the AI to scan study notes and return which plugins apply.
2. **Phase 2 — Generate:** Pass the chosen plugins + their imports into the code-generation prompt.

Example:

```javascript
// Phase 1
const classifyPrompt = `Given these study notes, which Manim plugins apply? 
Plugins: manim-Astronomy, manim-eng, ManimML, manim-physics, manim-stock-visualization, 
manim-timeline, manim-CAD_Drawing_Utils, manim-meshes, manim-voiceover-plus.
Return JSON: { "plugins": ["ManimML"], "renderer": "opengl" }`;

// Phase 2 (use result in code gen)
const codePrompt = `Generate Manim code. Use plugin: ${chosenPlugin}. Renderer: ${renderer}. Imports: ${imports}.`;
```

---

## Renderer API Call

Ensure your frontend sends the correct `renderer` when calling the Manim renderer:

```javascript
const response = await fetch(RENDERER_URL + '/render', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: generatedCode,
    scene_name: sceneName,
    quality: 'ql',
    renderer: 'opengl'  // or 'cairo' — must match the plugin!
  })
});
```

---

## Files in This Repo

| File | Use |
|------|-----|
| `VYNOTES_AI_PLUGIN_GUIDE.md` | Full guide — copy into system prompt or reference |
| `plugins-reference.json` | Structured data — use for programmatic plugin selection |
| `VYNOTES_INTEGRATION.md` | This file — integration instructions |
