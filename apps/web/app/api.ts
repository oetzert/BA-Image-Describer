export async function describeImage(formData: FormData) {
    const base = process.env.NEXT_PUBLIC_API_BASE!;
    const res = await fetch(`${base}/describe`, { method: "POST", body: formData });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt);
    }
    return res.json() as Promise<{ text: string; model: string; tokens_in?: number; tokens_out?: number }>;
  }

export async function countInputTokens(formData: FormData) {
  const base = process.env.NEXT_PUBLIC_API_BASE!;
  const res = await fetch(`${base}/input_tokens`, { method: "POST", body: formData });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt);
  }
  return res.json() as Promise<{ object: string; input_tokens: number }>;
}

export async function describeImagesBatch(formData: FormData) {
  const base = process.env.NEXT_PUBLIC_API_BASE!;
  const res = await fetch(`${base}/describe_batch`, { method: "POST", body: formData });

  if (!res.ok) {
    throw new Error(await res.text());
  }

  return res.json() as Promise<{
    count: number;
    results: Array<{ filename: string; text: string; model: string; tokens_in?: number; tokens_out?: number }>;
  }>;
}