async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }
  return response.json();
}

function pretty(value) {
  return JSON.stringify(value, null, 2);
}

document.querySelector("#ingest-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const output = document.querySelector("#ingest-result");
  output.value = "Indexing...";

  try {
    const result = await postJson("/api/documents", {
      doc_id: form.get("doc_id"),
      language: form.get("language"),
      title: form.get("title"),
      text: form.get("text"),
      metadata: { source: "web-ui" },
    });
    output.value = pretty(result);
  } catch (error) {
    output.value = `Error: ${error.message}`;
  }
});

document.querySelector("#query-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const output = document.querySelector("#query-result");
  output.value = "Retrieving...";

  try {
    const result = await postJson("/api/query", {
      language: form.get("language"),
      query: form.get("query"),
      top_k: Number(form.get("top_k")),
    });
    output.value = pretty(result);
  } catch (error) {
    output.value = `Error: ${error.message}`;
  }
});

document.querySelector("#token-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const output = document.querySelector("#token-result");

  try {
    const result = await postJson("/api/experiments/tokenization", {
      text: form.get("text"),
    });
    output.value = pretty(result);
  } catch (error) {
    output.value = `Error: ${error.message}`;
  }
});

