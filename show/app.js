const dlIcon =
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M5 21h14"/></svg>';
const playIcon =
  '<svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>';

let scriptOn = true;
let playing = false;
let touchX = 0;

function rel(path) {
  return String(path || "").replace(/^\//, "");
}

function deckOf(show, part) {
  if (!show.split || part === "all") return show.slides;
  const deck = show.slides.filter((slide) => slide.part === part);
  return deck.length ? deck : show.slides;
}

function read() {
  const q = new URLSearchParams(location.search);
  const raw = q.get("part") || "all";
  const n = Number(q.get("n"));
  return {
    id: q.get("id") || "",
    n: Number.isFinite(n) && n > 0 ? Math.floor(n) : 1,
    part: raw === "all" || /^[a-z]{1,4}$/.test(raw) ? raw : "all",
  };
}

function write(next, replace) {
  const url = new URL(location.href);
  url.hash = "";
  if (!next.id) url.search = "";
  else {
    url.searchParams.set("id", next.id);
    url.searchParams.set("n", String(next.n));
    url.searchParams.set("part", next.part);
  }
  history[replace ? "replaceState" : "pushState"]({}, "", url);
  playing = false;
  render();
}

function h(tag, attrs, children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs || {})) {
    if (value == null || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "html") node.innerHTML = value;
    else if (key.startsWith("on") && typeof value === "function") node.addEventListener(key.slice(2), value);
    else if (value === true) node.setAttribute(key, "");
    else node.setAttribute(key, String(value));
  }
  for (const child of children || []) {
    if (child == null || child === false) continue;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  }
  return node;
}

function fileKind(name) {
  return String(name).toLowerCase().endsWith(".pdf") ? "PDF" : "PowerPoint";
}

function renderHome() {
  document.title = "Show";
  const root = document.getElementById("app");
  root.replaceChildren(
    h("main", { class: "mx-auto w-full max-w-5xl px-4 pb-16 pt-8 sm:px-6" }, [
      h("header", { class: "max-w-xl" }, [
        h("p", { class: "text-sm font-semibold text-muted" }, ["Maqsudjon"]),
        h("h1", { class: "mt-1 text-5xl font-semibold tracking-tight" }, ["Show"]),
        h("p", { class: "mt-3 max-w-sm text-base leading-relaxed text-muted" }, [
          "Slaydni oching, matnni baland o‘qing. Kerak bo‘lsa PowerPointni oling.",
        ]),
      ]),
      h(
        "div",
        { class: "mt-8 grid gap-4 sm:grid-cols-2" },
        SHOWS.map((show) =>
          h("article", { class: "glass r-xl p-2" }, [
            h(
              "a",
              {
                class: "block text-inherit no-underline",
                href: `?id=${show.id}&n=1&part=all`,
                onclick: (event) => {
                  event.preventDefault();
                  write({ id: show.id, n: 1, part: "all" });
                },
              },
              [
                h("img", {
                  src: rel(show.slides[0]?.img),
                  alt: "",
                  class: "radius-in aspect-video w-full object-cover",
                }),
                h("div", { class: "px-3 pb-1 pt-3" }, [
                  h("p", { class: "text-xs font-semibold tracking-wide text-faint" }, [show.when]),
                  h("h2", { class: "mt-1 text-2xl font-semibold tracking-tight" }, [show.title]),
                  h("p", { class: "mt-1 text-sm leading-snug text-muted" }, [show.sub]),
                ]),
              ],
            ),
            h("div", { class: "flex items-center justify-between px-3 pb-2 pt-3" }, [
              h("span", { class: "text-sm text-faint" }, [fileKind(show.file)]),
              h(
                "a",
                { class: "btn btn-fill", href: rel(show.file), download: show.fname },
                [h("span", { html: dlIcon }), "Yuklab olish"],
              ),
            ]),
          ]),
        ),
      ),
    ]),
  );
}

function renderStage(show) {
  const view = read();
  const deck = deckOf(show, view.part);
  const index = Math.min(Math.max(view.n - 1, 0), Math.max(deck.length - 1, 0));
  const slide = deck[index];
  if (!slide) return renderMissing();
  document.title = `${show.title} · Show`;
  const who = show.parts?.find((item) => item.id === slide.part)?.who;
  const last = index + 1 === deck.length;
  const pct = Math.round(((index + 1) / deck.length) * 100);

  function go(delta) {
    const next = index + delta;
    if (next < 0) return;
    if (next >= deck.length) {
      write({ id: "" });
      return;
    }
    write({ id: show.id, n: next + 1, part: view.part });
  }

  const tabs = show.parts
    ? h("div", { class: "glass grid flex-1 grid-cols-3 gap-1 rounded-full p-1", role: "tablist" }, [
        h(
          "button",
          {
            type: "button",
            class: `seg ${view.part === "all" ? "on" : ""}`,
            role: "tab",
            onclick: () => write({ id: show.id, n: 1, part: "all" }),
          },
          ["Ikkalasi"],
        ),
        ...show.parts.map((part) =>
          h(
            "button",
            {
              type: "button",
              class: `seg ${view.part === part.id ? "on" : ""}`,
              role: "tab",
              onclick: () => write({ id: show.id, n: 1, part: part.id }),
            },
            [part.label],
          ),
        ),
      ])
    : null;

  const root = document.getElementById("app");
  root.replaceChildren(
    h("main", { class: "mx-auto flex min-h-dvh w-full max-w-6xl flex-col gap-3 px-3 pt-3 sm:px-6 sm:pt-6" }, [
      h("header", { class: "glass flex items-center gap-2 rounded-full p-1.5 pl-1.5 pr-4" }, [
        h(
          "a",
          {
            class: "btn",
            href: "./",
            onclick: (event) => {
              event.preventDefault();
              write({ id: "" });
            },
          },
          ["Kundalik"],
        ),
        h("h1", { class: "min-w-0 flex-1 truncate text-center text-base font-semibold tracking-tight" }, [show.title]),
        h("span", { class: "shrink-0 text-sm font-semibold tabular-nums text-muted" }, [`${index + 1}/${deck.length}`]),
      ]),
      h("div", { class: "flex flex-col gap-2 sm:flex-row" }, [
        tabs,
        h("div", { class: "flex gap-2" }, [
          h(
            "button",
            {
              type: "button",
              class: "btn flex-1",
              onclick: () => {
                scriptOn = !scriptOn;
                render();
              },
            },
            [scriptOn ? "Matnsiz" : "Matn"],
          ),
          h("a", { class: "btn flex-1", href: rel(show.file), download: show.fname }, [
            h("span", { html: dlIcon }),
            "Yuklab olish",
          ]),
        ]),
      ]),
      h("div", { class: `grid items-start gap-3 ${scriptOn ? "lg:grid-cols-5" : ""}` }, [
        h("section", { class: scriptOn ? "lg:col-span-3" : "" }, [
          h("div", { class: "glass r-xl p-2" }, [
            h(
              "div",
              {
                class: "well radius-in relative overflow-hidden",
                ontouchstart: (event) => {
                  touchX = event.changedTouches[0]?.clientX ?? 0;
                },
                ontouchend: (event) => {
                  const dx = (event.changedTouches[0]?.clientX ?? 0) - touchX;
                  if (dx > 48) go(-1);
                  if (dx < -48) go(1);
                },
              },
              [
                h("img", {
                  src: rel(slide.img),
                  alt: "",
                  class: `rise aspect-video w-full object-contain ${playing ? "invisible" : ""}`,
                }),
                slide.video
                  ? h("video", {
                      class: `absolute inset-0 h-full w-full bg-ink object-contain ${playing ? "" : "invisible"}`,
                      src: rel(slide.video),
                      playsinline: true,
                      controls: playing ? true : null,
                      onended: () => {
                        playing = false;
                        render();
                      },
                    })
                  : null,
                slide.video && !playing
                  ? h(
                      "button",
                      {
                        type: "button",
                        class: "play",
                        "aria-label": "Videoni o‘ynat",
                        onclick: async (event) => {
                          const video = event.currentTarget.parentElement.querySelector("video");
                          playing = true;
                          render();
                          const next = document.querySelector("video");
                          try {
                            await next.play();
                          } catch {
                            playing = false;
                            render();
                          }
                        },
                      },
                      [h("span", { html: playIcon })],
                    )
                  : null,
              ],
            ),
          ]),
          h("div", { class: "meter mt-3", role: "progressbar", "aria-valuenow": index + 1, "aria-label": "Slayd" }, [
            h("div", { style: `width:${pct}%` }),
          ]),
        ]),
        scriptOn
          ? h("section", { class: "glass rise r-xl p-5 lg:col-span-2" }, [
              who ? h("p", { class: "mb-2 text-xs font-semibold tracking-widest text-faint uppercase" }, [who]) : null,
              h("p", { class: "say" }, [slide.say]),
              slide.uz ? h("p", { class: "uz" }, [slide.uz]) : null,
              slide.note ? h("p", { class: "note" }, [slide.note]) : null,
            ])
          : null,
      ]),
      h("nav", { class: "dock" }, [
        h("div", { class: "glass mx-auto grid max-w-md grid-cols-2 gap-2 rounded-full p-2" }, [
          h(
            "button",
            { type: "button", class: "btn", disabled: index === 0, onclick: () => go(-1) },
            ["Oldingi"],
          ),
          h(
            "button",
            { type: "button", class: "btn btn-accent", onclick: () => go(1) },
            [last ? "Tugadi" : "Keyingi"],
          ),
        ]),
      ]),
    ]),
  );
  window.__go = go;
}

function renderMissing() {
  document.title = "Show";
  document.getElementById("app").replaceChildren(
    h("main", { class: "mx-auto max-w-lg px-4 py-16" }, [
      h("div", { class: "glass r-xl p-6" }, [
        h("h1", { class: "text-2xl font-semibold tracking-tight" }, ["Topilmadi"]),
        h("p", { class: "mt-2 text-muted" }, ["Bu namoyish kundalikda yo‘q."]),
        h(
          "a",
          {
            class: "btn btn-fill mt-5",
            href: "./",
            onclick: (event) => {
              event.preventDefault();
              write({ id: "" });
            },
          },
          ["Kundalik"],
        ),
      ]),
    ]),
  );
}

function render() {
  const view = read();
  const show = SHOWS.find((item) => item.id === view.id);
  if (!view.id) renderHome();
  else if (!show) renderMissing();
  else renderStage(show);
}

window.addEventListener("popstate", () => {
  playing = false;
  render();
});
window.addEventListener("keydown", (event) => {
  if (!read().id || !window.__go) return;
  if (event.key === "ArrowRight") window.__go(1);
  if (event.key === "ArrowLeft") window.__go(-1);
});
render();
