# Check for changed posts

Jekyll::Hooks.register :documents, :post_init do |post|

  commit_num = `git rev-list --count HEAD "#{ post.path }"`

  if commit_num.to_i > 1
    # Somehow the post date is always the latest commit... :(
    post_date = `git log --reverse --pretty="%ad" --date=iso "#{ post.path }" | head -1`
    post.data['date'] = post_date

    lastmod_date = `git log -1 --pretty="%ad" --date=iso "#{ post.path }"`
    post.data['last_modified_at'] = lastmod_date
  end

end
