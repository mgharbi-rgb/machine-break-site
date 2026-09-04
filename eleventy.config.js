// Eleventy ne génère que le blog, le sitemap et copie tout le reste tel quel.
// Les pages HTML existantes ne sont PAS traitées comme des gabarits (templateFormats).
export default function (eleventyConfig) {
  eleventyConfig.setInputDirectory(".");
  eleventyConfig.setOutputDirectory("_site");
  eleventyConfig.setIncludesDirectory("_includes");
  eleventyConfig.setDataDirectory("_data");
  eleventyConfig.setTemplateFormats(["njk", "md"]);
  eleventyConfig.setLayoutResolution(false);

  // Copie fidèle de tout le site statique
  for (const p of ["assets", "admin", "solutions", "zones", "_redirects", "_headers", "robots.txt", "social.json", "favicon.ico"]) {
    eleventyConfig.addPassthroughCopy(p);
  }
  eleventyConfig.addPassthroughCopy("*.html");

  eleventyConfig.addGlobalData("site.buildDate", () => new Date().toISOString().slice(0, 10));
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
  eleventyConfig.addCollection("articles", (api) => api.getFilteredByTag("articles").sort((a, b) => a.date - b.date));
}
