include Jekyll::Filters

module AllCategoriesAndTags

  class CategoriesAndTagsPageGenerator < Jekyll::Generator
    safe true

    def generate(site)

      all_tags, all_categories = get_all_categories_and_tags(site)

      all_tags.each do |tag, posts|
        site.pages << TagPage.new(site, tag, posts)
      end

      all_categories.each do |category, posts|
        site.pages << CategoryPage.new(site, category, posts)
      end

    end

    def get_all_categories_and_tags(site)
      # Already given by Jekyll: the list of posts for each tag
      all_tags       = site.post_attr_hash('tags')
      # Already given by Jekyll: the list of posts for each category
      all_categories = site.post_attr_hash('categories')

      site.collections.each do |collection, posts|
        # Trick: loop over the pages in reverse order because they are prepend to the hash
        # => end up with the original order
        posts.docs.reverse.each do |page|

          page_tags = page.data['tags']
          unless page_tags.nil?
            page_tags.each do |tag|
              unless all_tags[tag].include?(page)
                # Pages in front of the list
                all_tags[tag].unshift(page)
              end
            end
          end

          page_categories = page.data['categories']
          unless page_categories.nil?
            page_categories.each do |category|
              unless all_categories[category].include?(page)
                # Pages in front of the list
                all_categories[category].unshift(page)
              end
            end
          end

        end

      end

      return all_tags, all_categories
    end

  end

  # Subclass of `Jekyll::Page` with custom method definitions.
  class CategoryPage < Jekyll::Page

    def initialize(site, category, posts)
      @site = site              # the current site instance.
      @base = site.source       # path to the source directory.
      @dir  = slugify(category) # the directory the page will reside in.

      # All pages have the same filename, so define attributes straight away.
      @basename = 'index'      # filename without the extension.
      @ext      = '.html'      # the extension.
      @name     = 'index.html' # basically @basename + @ext.

      # Initialize data hash with a key pointing to all posts under current category.
      # This allows accessing the list in a template via `page.linked_docs`.
      @data = {
        'title' => category.capitalize,
        'posts' => posts,
        'layout' => 'category',
      }

      # Look up front matter defaults scoped to type `categories`, if given key
      # doesn't exist in the `data` hash.
      data.default_proc = proc do |_, key|
        site.frontmatter_defaults.find(relative_path, :categories, key)
      end
    end

    # Placeholders that are used in constructing page URL.
    def url_placeholders
      {
        :name       => @dir,
        :basename   => basename,
        :output_ext => output_ext,
      }
    end
  end

  # Subclass of `Jekyll::Page` with custom method definitions.
  class TagPage < Jekyll::Page

    def initialize(site, tag, posts)
      @site = site              # the current site instance.
      @base = site.source       # path to the source directory.
      @dir  = slugify(tag)      # the directory the page will reside in.

      # All pages have the same filename, so define attributes straight away.
      @basename = 'index'      # filename without the extension.
      @ext      = '.html'      # the extension.
      @name     = 'index.html' # basically @basename + @ext.

      # Initialize data hash with a key pointing to all posts under current category.
      # This allows accessing the list in a template via `page.linked_docs`.
      @data = {
        'title' => tag.capitalize,
        'posts' => posts,
        'layout' => 'tag',
      }

      # Look up front matter defaults scoped to type `tags`, if given key
      # doesn't exist in the `data` hash.
      data.default_proc = proc do |_, key|
        site.frontmatter_defaults.find(relative_path, :tags, key)
      end
    end

    # Placeholders that are used in constructing page URL.
    def url_placeholders
      {
        :name       => @dir,
        :basename   => basename,
        :output_ext => output_ext,
      }
    end
  end
end
