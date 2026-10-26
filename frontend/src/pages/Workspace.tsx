import { useEffect, useMemo, useState } from "react";
import {
  AlertCircle,
  ArrowRight,
  BarChart3,
  Boxes,
  Check,
  ChevronDown,
  Database,
  Download,
  Layers3,
  LoaderCircle,
  RefreshCcw,
  Search,
  ShieldCheck,
  Sparkles,
  X,
} from "lucide-react";
import Metric from "../components/Metric";
import { api } from "../services/api";
import type {
  CatalogResponse,
  Dataset,
  HealthResponse,
  RecommendationResponse,
} from "../types/api";

const DATASET_LABELS: Record<Dataset, string> = {
  instacart: "Instacart",
  uci: "UCI Online Retail",
};

function percent(value: number | null): string {
  return value === null ? "N/A" : `${(value * 100).toFixed(1)}%`;
}

function numeric(value: number | null): string {
  return value === null ? "N/A" : value.toFixed(3);
}

function downloadResults(result: RecommendationResponse) {
  const blob = new Blob([JSON.stringify(result, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `bundlerecommender-${result.dataset}.json`;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

export default function Workspace() {
  const [dataset, setDataset] = useState<Dataset>("instacart");
  const [catalog, setCatalog] = useState<CatalogResponse | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [selected, setSelected] = useState<string[]>([]);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    void api.health().then(setHealth).catch(() => setHealth(null));
  }, []);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    setCatalog(null);
    setResult(null);
    setSelected([]);
    setQuery("");

    void api.catalog(dataset)
      .then((data) => { if (active) setCatalog(data); })
      .catch((reason: unknown) => {
        if (active) setError(reason instanceof Error ? reason.message : "Cannot read product catalog.");
      })
      .finally(() => { if (active) setLoading(false); });

    return () => { active = false; };
  }, [dataset]);

  const filtered = useMemo(() => {
    const term = query.toLocaleLowerCase();
    return (catalog?.products ?? [])
      .filter((product) => product.toLocaleLowerCase().includes(term))
      .filter((product) => !selected.includes(product))
      .slice(0, 15);
  }, [catalog, selected, query]);

  function add(product: string) {
    setSelected((current) => current.includes(product) || current.length >= 20 ? current : [...current, product]);
    setResult(null);
    setQuery("");
  }

  async function analyze() {
    if (!selected.length || submitting) return;
    setSubmitting(true);
    setError("");
    setResult(null);

    try {
      setResult(await api.recommend(dataset, selected));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Recommendation request failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="/" aria-label="BundleRecommender Home">
          <span className="brand-icon"><Boxes size={23} /></span>
          <span><b>bundle<span>recommender</span></b><small>INTELLIGENCE STUDIO</small></span>
        </a>

        <p className="nav-caption">WORKSPACE</p>
        <div className="nav-item active"><Sparkles size={18} /> Recommendation Studio</div>
        <div className="nav-item"><Database size={18} /> Dataset-driven rules</div>
        <div className="nav-item"><BarChart3 size={18} /> Evidence & metrics</div>

        <div className="sidebar-footer">
          <span className="status-dot" /> RESEARCH PROTOTYPE
          <p>Associations are not purchase probabilities or guaranteed sales uplift.</p>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div><span className="muted">Workspace</span><span className="breadcrumb"> / </span>Recommendations</div>
          <div className="top-actions">
            <button className="icon-button" onClick={() => void api.health().then(setHealth).catch(() => setHealth(null))} title="Refresh model status"><RefreshCcw size={16} /></button>
            <span className={`status ${health?.datasets[dataset]?.available ? "ready" : "missing"}`}>
              <span className="status-dot" /> {health?.datasets[dataset]?.available ? "Artifact available" : "Artifact unavailable"}
            </span>
          </div>
        </header>

        <div className="content">
          <section className="hero">
            <span className="hero-eyebrow"><span className="status-dot" /> ASSOCIATION RULE INTELLIGENCE</span>
            <h1>Find the products that <em>belong together.</em></h1>
            <p>Explore product combinations discovered in real experiment artifacts. Select items from the training-derived catalog, then inspect rule-backed suggestions and their evidence.</p>
            <div className="hero-tags"><span><Layers3 size={15} /> Evidence-based</span><span><ShieldCheck size={15} /> No fabricated results</span><span><Database size={15} /> Local CSV inference</span></div>
          </section>

          <section className="stats">
            <Metric title="ACTIVE DATASET" value={DATASET_LABELS[dataset]} description="Independent recommendation space" />
            <Metric title="AVAILABLE PRODUCTS" value={catalog?.count.toLocaleString() ?? "—"} description="From association-rule CSV" />
            <Metric title="RULES SCANNED" value={result?.scanned_rules.toLocaleString() ?? "—"} description="After executing a query" />
          </section>

          <div className="workspace-grid">
            <section className="panel">
              <div className="panel-header"><div><span className="eyebrow">01 / CONFIGURATION</span><h2>Build your product basket</h2></div><Layers3 size={20} className="secondary-icon" /></div>

              <label className="field-label" htmlFor="dataset">DATA SOURCE</label>
              <div className="select-wrap">
                <select id="dataset" value={dataset} onChange={(event) => setDataset(event.target.value as Dataset)}>
                  <option value="instacart">Instacart — association rules</option>
                  <option value="uci">UCI Online Retail — association rules</option>
                </select><ChevronDown size={16} />
              </div>
              <p className="field-help">Sources are kept separate; we never merge different product namespaces.</p>

              <label className="field-label" htmlFor="product-search">SEARCH PRODUCT CATALOG</label>
              <div className="search-wrap"><Search size={17} /><input id="product-search" placeholder={loading ? "Loading catalog..." : "Search a product name..."} value={query} onChange={(event) => setQuery(event.target.value)} disabled={!catalog || loading} /></div>

              {query && filtered.length > 0 && (
                <div className="search-results">
                  {filtered.map((product) => <button key={product} onClick={() => add(product)}><span>{product}</span><ArrowRight size={15} /></button>)}
                </div>
              )}
              {query && filtered.length === 0 && <p className="field-help">No matching products in this rule catalog.</p>}

              <label className="field-label basket-label">SELECTED BASKET <span>{selected.length}/20</span></label>
              <div className="basket">
                {selected.length === 0 ? <div className="basket-empty"><Boxes size={25}/><p>Add one or more products to start</p></div> : selected.map((product) => <span className="chip" key={product}>{product}<button title={`Remove ${product}`} onClick={() => {setSelected((current) => current.filter((name) => name !== product));setResult(null);}}><X size={14}/></button></span>)}
              </div>
              <button className="primary" onClick={() => void analyze()} disabled={!selected.length || submitting || !catalog}>
                {submitting ? <LoaderCircle className="spin" size={17}/> : <Sparkles size={17}/>} {submitting ? "Finding associations..." : "Generate bundle suggestions"}<ArrowRight size={16}/>
              </button>
            </section>

            <section className="panel">
              <div className="panel-header"><div><span className="eyebrow">02 / RESULTS</span><h2>Recommendation evidence</h2></div>{result && <button className="icon-button" title="Download JSON" onClick={() => downloadResults(result)}><Download size={18}/></button>}</div>
              {!result ? <div className="empty-result"><div className="empty-result-icon"><Boxes size={37}/></div><h3>Suggestions appear here</h3><p>Choose products from the dataset catalog and run the rule engine.</p></div> : <>
                <div className="result-meta"><span><Check size={14}/> {result.matched_rules} matching rules</span><span>{result.suggestions.length} suggestions</span></div>
                {result.suggestions.length === 0 ? <div className="no-result"><AlertCircle size={20}/><b>No matching bundle rule</b><p>The existing rule artifact does not contain a recommendation for this basket. This is a valid result, not a system error.</p></div> : (
                  <div className="suggestions">
                    {result.suggestions.map((suggestion, index) => <article className="suggestion" key={suggestion.product}>
                      <div className="suggestion-top"><span className="rank">{String(index + 1).padStart(2, "0")}</span><h3>{suggestion.product}</h3></div>
                      <div className="evidence"><div><small>SUPPORT</small><b>{percent(suggestion.support)}</b></div><div><small>CONFIDENCE</small><b>{percent(suggestion.confidence)}</b></div><div><small>LIFT</small><b>{numeric(suggestion.lift)}</b></div></div>
                      <p className="matched">Matched: {suggestion.matched_input.join(" + ")} · {suggestion.source}</p>
                    </article>)}
                  </div>
                )}
                <div className="notice"><ShieldCheck size={17}/><p>{result.disclaimer}</p></div>
              </>}
            </section>
          </div>

          {error && <div className="error" role="alert"><AlertCircle size={18}/><span>{error}</span><button onClick={() => setError("")}><X size={16}/></button></div>}
          <footer><span>BUNDLERECOMMENDER · 100 DAYS OF PROJECTS</span><span>Research prototype · Human-reviewed insights</span></footer>
        </div>
      </main>
    </div>
  );
}
