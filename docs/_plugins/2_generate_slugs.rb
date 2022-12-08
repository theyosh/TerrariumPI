# Plugin that generates 'slug' variables that can be used in permalink urls

Jekyll::Hooks.register :site, :post_read do |site|
  site.collections.each do |collection, posts|
    posts.docs.each do |post|
      post.data['slug'] = slugify(post.data['title'])
    end
  end
end