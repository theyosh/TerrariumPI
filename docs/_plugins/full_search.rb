Jekyll::Hooks.register :site, :post_write do |site|

  include Liquid::StandardFilters

  json_content = '['

  site.collections.each do |collection, posts|

    posts.docs.each do |post|
      json_content += '{'
      json_content += '"title":"' + escape(post.data['title'].gsub(/\s+/, ' ')) + '",'
      json_content += '"url":"' + site.baseurl +  post.url + '",'
      json_content += '"categories":"' + join(post.data['categories'],", ") + '",'
      json_content += '"tags":"' + join(post.data['tags'],", ") + '",'
      json_content += '"date":"' + post.date.to_s + '",'
      json_content += '"content":"' + strip_html(post.content).gsub(/\n+/, ' ').gsub(/"/,'\"') + '"'
      json_content += '}'
      json_content += ','
    end

  end

  json_content = json_content[0...-1]
  json_content += ']'

  # Overwrite template version
  path = site.config['destination'] + '/assets/js/data/search.json'
  FileUtils.mkdir_p(File.dirname(path))
  File.open(path, 'w') do |f|
    f.write(json_content)
  end

end