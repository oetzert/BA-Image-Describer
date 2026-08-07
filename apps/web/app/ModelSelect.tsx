"use client";

import { MODEL_OPTIONS } from "./models";

export function ModelSelect({
  value,
  onChange,
}: {
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <label>
      Model
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        style={{ width: 260, marginLeft: 8 }}
      >
        {MODEL_OPTIONS.map((m) => (
          <option key={m.value} value={m.value}>
            {m.label}
          </option>
        ))}
      </select>
    </label>
  );
}
