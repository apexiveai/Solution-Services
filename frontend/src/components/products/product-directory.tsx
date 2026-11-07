"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { ArrowRight, ArrowUpRight, Search } from "lucide-react";
import { productFamilies, products, type ProductFamily } from "@/data/products";

export default function ProductDirectory() {
  const [activeFamily, setActiveFamily] = useState<ProductFamily | "All products">("All products");
  const [query, setQuery] = useState("");

  const visibleProducts = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    return products.filter((product) => {
      const matchesFamily = activeFamily === "All products" || product.family === activeFamily;
      const matchesQuery =
        !normalizedQuery ||
        `${product.name} ${product.tagline} ${product.summary}`.toLowerCase().includes(normalizedQuery);

      return matchesFamily && matchesQuery;
    });
  }, [activeFamily, query]);

  return (
    <section className="product-directory-section" id="product-directory">
      <div className="product-content-container">
        <div className="product-directory-toolbar">
          <div className="product-family-tabs" role="tablist" aria-label="Product families">
            {(["All products", ...productFamilies] as const).map((family) => (
              <button
                type="button"
                role="tab"
                aria-selected={activeFamily === family}
                className={activeFamily === family ? "active" : ""}
                key={family}
                onClick={() => setActiveFamily(family)}
              >
                {family}
              </button>
            ))}
          </div>

          <label className="product-search">
            <Search size={17} aria-hidden="true" />
            <span className="sr-only">Search products</span>
            <input
              type="search"
              placeholder="Search products"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </label>
        </div>

        <div className="product-directory-heading">
          <div>
            <span className="eyebrow">APEXIVEAI / MYANMAR-BUILT PRODUCTS</span>
            <h2>
              Local products.
              <br />
              <span>{products.length} ways to move work forward.</span>
            </h2>
          </div>
          <p>
            Explore products developed in Myanmar across AI, data intelligence,
            network infrastructure, connected operations and automation.
          </p>
        </div>

        {visibleProducts.length > 0 ? (
          <div className="product-directory-grid">
            {visibleProducts.map((product) => {
              const Icon = product.icon;

              return (
                <Link
                  href={`/products/${product.slug}`}
                  className="product-directory-card"
                  key={product.slug}
                >
                  <div className="product-card-top">
                    <span>{product.number} / {product.family}</span>
                    <div className="product-card-icon"><Icon size={22} /></div>
                  </div>
                  <h3>{product.name}</h3>
                  <h4>{product.tagline}</h4>
                  <p>{product.summary}</p>
                  <div className="product-card-bottom">
                    <span>Explore product</span>
                    <ArrowUpRight size={17} />
                  </div>
                </Link>
              );
            })}
          </div>
        ) : (
          <div className="product-empty-state">
            <Search size={23} />
            <strong>No products match that search.</strong>
            <span>Try a different product name or capability.</span>
          </div>
        )}

        <div className="product-directory-footnote">
          <span>DESIGNED FOR MYANMAR ORGANIZATIONS</span>
          <Link href="/solutions">
            Explore industry solutions <ArrowRight size={15} />
          </Link>
        </div>
      </div>
    </section>
  );
}
