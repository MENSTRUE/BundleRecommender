type MetricProps = {
  title: string;
  value: string;
  description: string;
};

export default function Metric({ title, value, description }: MetricProps) {
  return (
    <div className="metric">
      <span className="eyebrow">{title}</span>
      <strong>{value}</strong>
      <span className="muted">{description}</span>
    </div>
  );
}
