export type Dataset = "instacart" | "uci";

export type DatasetStatus = {
  available: boolean;
  file: string;
};

export type HealthResponse = {
  status: string;
  research_only: boolean;
  datasets: Record<Dataset, DatasetStatus>;
};

export type CatalogResponse = {
  dataset: Dataset;
  products: string[];
  count: number;
};

export type ProductDetails = {
  id: string;
  name: string;
  has_description: boolean;
};

export type CatalogDetailsResponse = {
  dataset: Dataset;
  products: ProductDetails[];
  count: number;
  named_count: number;
};

export type Suggestion = {
  product: string;
  score: number | null;
  support: number | null;
  confidence: number | null;
  lift: number | null;
  matched_input: string[];
  source: string;
};

export type RecommendationResponse = {
  dataset: Dataset;
  items: string[];
  suggestions: Suggestion[];
  matched_rules: number;
  scanned_rules: number;
  disclaimer: string;
};
