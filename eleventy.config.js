// Refonte 2026 : toutes les pages sont des gabarits Nunjucks (layout-base.njk et ses dérivés), les ressources sont copiées telles quelles.
export default function (eleventyConfig) {
  eleventyConfig.setInputDirectory(".");
  eleventyConfig.setOutputDirectory("_site");
  eleventyConfig.setIncludesDirectory("_includes");
  eleventyConfig.setDataDirectory("_data");
  eleventyConfig.setTemplateFormats(["njk", "md"]);
  eleventyConfig.setLayoutResolution(false);

  for (const p of ["assets", "admin", "maquettes", "_redirects", "_headers", "robots.txt", "social.json", "favicon.ico"]) {
    eleventyConfig.addPassthroughCopy(p);
  }

  eleventyConfig.addGlobalData("site.buildDate", () => new Date().toISOString().slice(0, 10));
  // empreinte de construction pour forcer le rechargement du CSS et du JS après chaque mise en ligne
  eleventyConfig.addGlobalData("site.buildStamp", () => Date.now().toString(36));
  eleventyConfig.addFilter("isoDate", (d) => new Date(d).toISOString().slice(0, 10));
  eleventyConfig.addFilter("frDate", (d) => new Date(d).toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric", timeZone: "UTC" }));
  eleventyConfig.addFilter("url", (u) => (u || "").replace(/\.html$/, "").replace(/\/index$/, "/"));
  eleventyConfig.addFilter("articleLd", (page, title, description, image, date, updated) => {
    const site = "https://machinebreak.com";
    const iso = (d) => new Date(d).toISOString().slice(0, 10);
    const url = site + page.url.replace(/\.html$/, "");
    return JSON.stringify({
      "@context": "https://schema.org", "@type": "BlogPosting", headline: title, description,
      image: image ? site + image : site + "/assets/img/og-image.jpg",
      datePublished: iso(date), dateModified: iso(updated || date), inLanguage: "fr-FR",
      author: { "@type": "Organization", name: "Machine Break", url: site + "/" },
      publisher: { "@type": "Organization", name: "Machine Break", logo: { "@type": "ImageObject", url: site + "/assets/img/logo.webp" } },
      mainEntityOfPage: url,
    }, null, 2);
  });
  // données structurées des pages migrées (FAQPage, BreadcrumbList) à partir des données de page
  eleventyConfig.addFilter("faqLd", (faq) => JSON.stringify({
    "@context": "https://schema.org", "@type": "FAQPage",
    mainEntity: (faq || []).map((q) => ({ "@type": "Question", name: q.q, acceptedAnswer: { "@type": "Answer", text: q.a } })),
  }));
  eleventyConfig.addFilter("crumbsLd", (crumbs) => JSON.stringify({
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    itemListElement: (crumbs || []).map((c, i) => ({ "@type": "ListItem", position: i + 1, name: c.name, item: "https://machinebreak.com" + c.url })),
  }));
  eleventyConfig.addCollection("articles", (api) => api.getFilteredByTag("articles").sort((a, b) => a.date - b.date));
}
