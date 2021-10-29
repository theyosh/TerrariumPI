# This is fix/patch for Jekyll-analytics, as this fix will add stats to ALL documents in the site

require "jekyll-analytics"

Jekyll::Hooks.register :documents, :post_render do |page|
  # Posts are done by the original plugin
  unless 'posts' == page.type.to_s
    inject(page)
  end
end
