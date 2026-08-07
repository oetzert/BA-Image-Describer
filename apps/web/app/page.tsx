"use client";

import { useState } from "react";
import { describeImage, countInputTokens, describeImagesBatch} from "./api";
import { AGRICULTURAL_IMAGE_PROMPT } from "./prompt";
import { ModelSelect} from "./ModelSelect";


export default function Page() {
  const [files, setFiles] = useState<File[]>([]);
  const [prompt, setPrompt] = useState(AGRICULTURAL_IMAGE_PROMPT);
  const [model, setModel] = useState("gpt-4o-mini");
  const [temperature, setTemperature] = useState(0.1);
  const [maxTokens, setMaxTokens] = useState(400);
  const [result, setResult] = useState<string>("");
  const [usage, setUsage] = useState<string>("");
  const [tokenEstimate, setTokenEstimate] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [estimating, setEstimating] = useState(false);
  const [err, setErr] = useState<string>("");

  async function onRun() {
    setErr("");
    setResult("");
    setUsage("");
    setTokenEstimate("");

    if (files.length === 0) return;

    setLoading(true);
    try {
      if (files.length === 1) {
        const fd = new FormData();
        fd.append("file", files[0]);
        fd.append("prompt", prompt);
        fd.append("project_id", "1");
        fd.append("model", model);
        fd.append("temperature", String(temperature));
        fd.append("max_tokens", String(maxTokens));

        const data = await describeImage(fd);
        setResult(data.text);
      } else {
        const fd = new FormData();
        for (const f of files) {
          fd.append("files", f); // wichtig: plural!
        }

        fd.append("prompt", prompt);
        fd.append("project_id", "1");
        fd.append("model", model);
        fd.append("temperature", String(temperature));
        fd.append("max_tokens", String(maxTokens));

        const data = await describeImagesBatch(fd);

        const combined = data.results
          .map((r, i) => `# ${i + 1}: ${r.filename}\n${(r.text ?? "").trim()}\n`)
          .join("\n");

        setResult(combined);
      }
    } catch (e: any) {
      setErr(e?.message ?? "Error");
    } finally {
      setLoading(false);
    }  
  }

  async function onEstimate() {
    setErr("");
    setTokenEstimate("");
    if (!files || files.length === 0) return;

    const fd = new FormData();
    fd.append("file", files[0]);
    fd.append("prompt", prompt);
    fd.append("model", model);

    setEstimating(true);
    try {
      const data = await countInputTokens(fd);
      setTokenEstimate(`input_tokens=${data.input_tokens}`);
    } catch (e: any) {
      setErr(e?.message ?? "Error");
    } finally {
      setEstimating(false);
    }
  }

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", fontFamily: "system-ui", padding: 16 }}>
      <h1>Image Describer BA 26</h1>

      <div style={{ display: "grid", gap: 12, marginTop: 16 }}>
        <input
          type="file"
          accept="image/png,image/jpeg,image/webp"
          multiple
          onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
        />

        <label>
          Prompt:
          <div style ={{ height : "1rem"}} ></div>
          <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={5} style={{ width: "100%", marginBottom: "1rem" }} />
        </label>

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <label>
            <ModelSelect value={model} onChange={setModel} />
          </label>

          <label>
            Temperature
            <input
              type="number"
              step="0.1"
              value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
              style={{ width: 90, marginLeft: 8 }}
            />
          </label>

          <label>
            Max Tokens
            <input
              type="number"
              value={maxTokens}
              onChange={(e) => setMaxTokens(Number(e.target.value))}
              style={{ width: 110, marginLeft: 8 }}
            />
          </label>
        </div>

        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <button
            onClick={onRun}
            disabled={!files || loading || estimating}
            style={{ padding: "10px 14px", width: 140 }}
          >
            {loading ? "läuft…" : "Run"}
          </button>

          <button
            onClick={onEstimate}
            disabled={!files || loading || estimating}
            style={{ padding: "10px 14px" }}
          >
            {estimating ? "zähle…" : "Estimate tokens"}
          </button>
        </div>

        {err && <pre style={{ whiteSpace: "pre-wrap", color: "crimson" }}>{err}</pre>}
        {tokenEstimate && <div style={{ opacity: 0.7 }}>{tokenEstimate}</div>}
        {usage && <div style={{ opacity: 0.7 }}>{usage}</div>}

        {result && (
          <section>
            <h3>Ergebnis</h3>
            <pre style={{ whiteSpace: "pre-wrap", background: "#f6f6f6", padding: 12, borderRadius: 8 }}>
              {result}
            </pre>
          </section>
        )}
      </div>
    </main>
  );
}
